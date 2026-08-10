# Android 系统启动分析

> 从按下电源键到 Launcher 桌面的完整进程诞生链。按启动顺序逐组件详解，图示为主，文字为辅，关键源码逐一拆解。

## 目录

- [一、总览](#一总览)
- [二、Bootloader 详解](#二bootloader-详解)
- [三、Linux Kernel 详解](#三linux-kernel-详解)
- [四、init 进程启动详解](#四init-进程启动详解)
- [五、Zygote 详解](#五zygote-详解)
- [六、ServiceManager 详解](#六servicemanager-详解)
- [七、system_server 详解](#七system_server-详解)
- [八、Launcher 详解](#八launcher-详解)

## 一、总览

<img src="./images/boot-overview.png" width="340" alt="Android 启动总链路">

**各阶段速览**

| 阶段                 | 关键动作                                       | 产出            | 调试关键字              |
| ------------------ | ------------------------------------------ | ------------- | ------------------ |
| **Bootloader**     | 硬件初始化、签名校验（AVB）、载入内核+ramdisk               | 跳转内核          | —                  |
| **Kernel**         | 解压、架构初始化、挂载 rootfs、exec `/init`            | PID 1 → init  | `dmesg`            |
| **init (1st)**     | 挂载 /system /vendor、加载 sepolicy             | SELinux 生效    | `init:`            |
| **init (2nd)**     | 解析 `init.rc`、触发 action、启动 service          | native 服务就绪   | `init:`            |
| **servicemanager** | init 拉起，提供 Binder 服务注册/查询                  | Binder 注册中心就绪 | —                  |
| **Zygote**         | 启动 ART、预加载、注册 socket 监听                    | 进入 fork 等待    | `Zygote:`          |
| **system_server**  | 三批发布系统服务、注册 ServiceManager                 | AMS 就绪        | `SystemServer:`    |
| **Launcher**       | AMS 查 HOME → fork Launcher                 | 桌面可见          | `ActivityManager:` |
| **App 启动**         | 点图标→AMS 请求 Zygote fork→ActivityThread.main | App 进程+界面     | `ActivityManager:` |

---

## 二、Bootloader 详解

Bootloader 是设备上电后运行的**第一段软件**，固化在芯片 Boot ROM 或专用闪存分区，职责是把可信的 Linux 内核安全加载进内存。

### 1. 启动链（以高通平台为例）

| 阶段      | 名称                                | 职责                    |
| ------- | --------------------------------- | --------------------- |
| PBL     | Primary Boot Loader（Boot ROM，不可改） | 最小硬件初始化，加载并验证下一级      |
| SBL/XBL | Secondary/eXtensible Boot Loader  | 初始化 DRAM、时钟、电源，加载 ABL |
| ABL     | Android Boot Loader（含 fastboot）   | 验证并加载 boot 镜像，跳转内核    |

> 不同厂商命名不同（MTK 用 Preloader + LK），但「逐级加载 + 逐级验证」的思路一致。

### 2. 核心职责

Bootloader 的核心任务分三类——硬件初始化、启动模式选择、安全校验，每一步不可跳过。

- 初始化最基础硬件：DRAM、时钟、电源管理、最小存储/调试接口
- 决定启动模式：正常启动 / Recovery / Fastboot（Download）
- 安全校验：通过 AVB 验证 boot/vendor/system 等镜像
- 加载内核：把 kernel、ramdisk、dtb（设备树）读入内存并跳转

### 3. 安全启动链（Chain of Trust）

从硬件 ROM 到最终加载内核，每一级固件都对下一级的签名做校验——任何一环失败即中止启动，信任根在芯片 Boot ROM。

```text
Boot ROM(不可改，eFuse 存公钥哈希)
  → 验证 PBL 签名
    → 验证 SBL 签名
      → 验证 ABL 签名
        → AVB 验证 boot 镜像
          → 进入 Kernel
```

信任根在芯片 Boot ROM，每一级验证下一级签名；任何一级验签失败即拒绝启动。

### 4. AVB（Android Verified Boot）

AVB（Android Verified Boot）是 Google 的完整性校验体系——通过 vbmeta、dm-verity 和 rollback index 保证启动链路中每一分区未被篡改。

| 机制                       | 作用                                                 |
| ------------------------ | -------------------------------------------------- |
| **vbmeta**               | 存各分区哈希/签名的元数据分区                                    |
| **hashtree / dm-verity** | 保证 system/vendor 只读分区完整性                           |
| **rollback index**       | 防止回滚到有漏洞的旧版本                                       |
| **locked / unlocked**    | locked 只接受厂商签名；`fastboot flashing unlock` 后可刷自定义镜像 |

### 5. A/B（无缝）更新相关

A/B 分区允许系统保留两套完整镜像——OTA 时更新「非活跃槽」，重启后自动切换，失败可自动回退。

- Bootloader 依据 `slot`（A/B）标记选择启动哪套分区
- 依据 `bootable` / `successful` 标记判断上次启动是否成功，失败自动回切到另一槽位

---

## 三、Linux Kernel 详解

> **一句话概述**：Linux Kernel 是启动的第二个阶段——完成硬件与内核子系统初始化、挂载根文件系统，并启动第一个用户态进程 init，把系统从裸机带入用户空间。

### 1. 内核启动主流程

Linux Kernel 从自解压开始，经 start_kernel() 完整初始化所有子系统，最终通过 rest_init() 拉出 kernel_init 线程——由它来 exec init，把系统从内核态带入用户空间。

```text
自解压 → start_kernel() → rest_init()
  → kernel_init 线程
    → 挂载 rootfs（initramfs）
      → exec("/init")   ← 第一个用户态进程
```

- `start_kernel()`：初始化内存管理、调度器、中断、定时器等核心子系统
- `rest_init()`：创建 `kernel_init`（未来 PID 1）与 `kthreadd`（PID 2）
- `kernel_init`：执行各级 `initcall`（驱动初始化），挂载 rootfs，最后 `exec` 成用户态 `init`

### 2. initcall 级别（驱动加载顺序）

内核用 `initcall` 分级保证初始化顺序：

```text
early → core → postcore → arch → subsys → fs → device → late
```

驱动按级别依次 `probe`，依赖未就绪的进入 deferred probe 稍后重试。

### 3. Android 特有的内核改动

相比主线 Linux，Android 内核打了大量专有补丁——Binder 驱动、ashmem、wakelocks、LOW_MEMORY_KILLER 等，均为移动场景定制。

| 特性                    | 作用                   |
| --------------------- | -------------------- |
| **Binder**            | 进程间通信核心驱动            |
| **ashmem**            | 匿名共享内存，跨进程共享大块数据     |
| **wakelock**          | 电源管理，阻止 CPU 休眠       |
| **Low Memory Killer** | 内存不足时按优先级回收进程        |
| **logger**            | 内核态日志环形缓冲（logcat 后端） |
| **ION / dma-buf**     | 图形/多媒体内存分配与共享        |

### 4. 设备树（DTB）

设备树（Device Tree）让硬件描述与内核代码解耦——Bootloader 传递 dtb/dto 给内核，内核根据描述初始化对应驱动，无需硬编码。

- 硬件信息不硬编码进内核，而用**设备树**描述
- Bootloader 把 dtb 传给内核，内核据此初始化对应驱动
- Android 用 **DTBO** 分区叠加厂商差异

### 5. rootfs 与分区挂载

内核启动 init 之前必须挂载根文件系统——从 initramfs 临时根到 system-as-root 的演进，决定了 rootfs 的挂载方式和 dm-verity 的介入时机。

- 内核先挂载 **initramfs**（ramdisk 里的临时根），含 `init`、`fstab`、`sepolicy`
- system-as-root 后 `/` 直接是 system 分区
- 通过 **dm-verity** 挂载只读分区（完整性校验）
- 后续由 init 挂载 `/vendor`、`/data` 等

### 6. GKI（通用内核镜像，Android 11+）

GKI 将通用内核与厂商模块彻底解耦——内核由 Google 统一构建分发，厂商通过内核模块提供硬件支持，根治碎片化。

- 把通用内核（GKI）与厂商模块（vendor modules）分离
- 提升内核一致性，简化 OTA 与安全更新

---

## 四、init 进程启动详解

init 是 Android 用户态**第一个进程（PID 1）**，所有用户态进程的祖先，负责拉起整个用户空间。

### 1. init 启动总流程（源码视角）

init 的启动分为 FirstStage 和 SecondStage 两个阶段——前者挂载分区、加载 sepolicy，后者解析 init.rc、拉起所有 native 服务、进入 epoll 主循环。以下是源码级调用链：

```text
kernel → /init main()
  → FirstStageMain()     # 第一阶段：基础文件系统
  → SetupSelinux()       # 加载 SELinux 策略
  → SecondStageMain()    # 第二阶段：属性服务 + 解析 rc + 事件循环
```

源码路径：`system/core/init/`（`main.cpp` → `first_stage_init.cpp` → `selinux.cpp` → `init.cpp`）

### 2. 两个阶段

init 分为 FirstStage 和 SecondStage 两个阶段——FirstStage 运行在最小化环境（挂载分区+SELinux），SecondStage 才进入完整的用户空间初始化。

| 阶段           | 入口                  | 职责                                                     |
| ------------ | ------------------- | ------------------------------------------------------ |
| First stage  | `FirstStageMain()`  | 创建/挂载 `/dev`、`/proc`、`/sys`、`/system`、`/vendor`，准备早期环境 |
| Second stage | `SecondStageMain()` | 初始化属性服务、解析 rc、启动所有 service、进入 epoll 主循环                |

### 3. init.rc 与 init 语言

init 不硬编码启动逻辑，而是解析 `.rc` 脚本——解析器把 rc 文本转化为 `Action` 和 `Service` 对象，再由主循环按 trigger 顺序执行。

**RC 脚本的核心语法**

- **service**：定义一个服务（可执行文件、user/group、权限、重启策略）
- **on `<trigger>`**：在某触发点执行一组 command
- **import**：引入其他 rc 文件

#### 解析器工作流程：以 Zygote 的 service 块为例

以下面这段 Zygote 的 rc 配置为例，拆解解析器如何逐行识别：

```rc
service zygote /system/bin/app_process64 -Xzygote /system/bin --zygote --start-system-server
    class main
    socket zygote stream 660 root system
    onrestart restart audioserver
    critical
```

**解析过程**：

```text
① Parser 逐行读取 rc 文件
② 遇到 "service zygote /system/bin/app_process64 ..." 
   → 匹配 ServiceParser，进入 service 段落模式
   → 创建 Service 对象：name="zygote", path="/system/bin/app_process64"
   → 第一行剩余部分作为启动参数 args
③ 缩进行逐条解析：
   "class main"          → 设置 class_ = "main"
   "socket zygote stream 660 root system"
                         → 创建 /dev/socket/zygote，权限 660
   "onrestart restart audioserver"
                         → 记录到 onrestart_ 列表（重启时级联重启）
   "critical"            → 设置 flags_ |= SVC_CRITICAL
④ 空行或新 "on"/"service" 关键字结束当前 service 段落
   → Service 对象被注册到全局 ServiceList
```

**核心源码与类图**

解析涉及的核心类关系如下——Parser 按关键字将解析委托给各 SectionParser，最终产出 Service 和 Action 对象：

<img src="./images/init-rc-parser-class.png" width="510" alt="init.rc 解析器类图">

```cpp
// system/core/init/action_manager.cpp — 解析入口
bool ActionManager::LoadBootScripts(
    const std::vector<std::string>& paths) {
    Parser parser;
    parser.AddSectionParser("service",
        std::make_unique<ServiceParser>(&service_list, ...));
    parser.AddSectionParser("on",
        std::make_unique<ActionParser>(this, ...));
    parser.AddSectionParser("import",
        std::make_unique<ImportParser>(&parser));
    for (auto& path : paths) {
        parser.ParseConfig(path);  // 逐行解析
    }
    return true;
}

// system/core/init/service.cpp — ServiceParser::ParseSection
Result<void> ServiceParser::ParseSection(
    std::vector<std::string>&& args, ...) {
    // args[0] = "service", args[1] = "zygote",
    // args[2] = "/system/bin/app_process64", ...
    service_ = std::make_unique<Service>(args[1], ...);
    return {};
}
```

> 整条链路：`LoadBootScripts` 注册三种解析器 → `ParseConfig` 逐行读 rc → 遇到 `service` 关键字交给 `ServiceParser` → `ParseSection` 创建 Service 对象 → `EndSection` 注册到全局列表。类似的，`on <trigger>` 交给 `ActionParser` 生成 Action。解析完成后 `ActionManager::QueueEventTrigger` 按序触发执行。

**解析后的触发时机**：

```
ActionManager 执行 action:
  on late-init
    trigger zygote-start       ← 触发名为 "zygote-start" 的 trigger

  on zygote-start && property:ro.crypto.state=unencrypted
    class_start main           ← 启动 class="main" 的所有 service（含 zygote）

  → ServiceList::FindByClass("main") → 找到 zygote 的 Service 对象
    → Service::Start() → fork() + execve("/system/bin/app_process64")
      → 子进程进入 ZygoteInit.main()
```

**关键源码路径**：`system/core/init/parser.cpp`（词法/语法解析）、`system/core/init/service.cpp`（Service 对象）、`system/core/init/builtins.cpp`（`class_start` 等内建命令）。

### 4. action 触发顺序

action 是 init.rc 中 `on <trigger>` 定义的一组命令集合——init 按先后顺序逐个触发，从 early-init 一直走到 sys.boot_completed=1。下图是标准的 action 触发链：

<img src="./images/init-chain.png" width="220" alt="init 触发链">

### 5. 属性服务（Property Service）

- init 维护一块共享内存存放键值对
- 进程通过 unix socket `/dev/socket/property_service` 读写
- 命名空间：`ro.*`（只读）、`sys.*`（运行时）、`persist.*`（持久化到 `/data/property`）
- 关键属性：`sys.boot_completed`、`ro.build.*`、`init.svc.<service>`（服务运行状态）
- 属性变化可触发 action，如 `on property:sys.boot_completed=1`

### 6. 关键 native 服务

| 关键 service       | 何时启动       | 职责              |
| ---------------- | ---------- | --------------- |
| `ueventd`        | early-init | 创建设备节点 `/dev/*` |
| `servicemanager` | init       | Binder 名字服务     |
| `logd`           | init       | 系统日志守护          |
| `vold`           | late-fs    | 卷管理、SD 卡挂载      |
| `zygote`         | late-init  | ART 孵化器         |
| `netd`           | boot       | 网络守护            |

### 7. ueventd：设备节点管理

ueventd 负责监听内核 uevent 事件并管理 /dev 设备节点——包括启动时的 coldboot 和运行时的热插拔响应。

- 监听内核 uevent（设备热插拔事件）
- **coldboot**：启动时遍历 `/sys`，为已存在设备补发 uevent
- 按 `ueventd.rc` 规则创建 `/dev` 节点并设置权限

### 8. SELinux 加载

SELinux 是 Android 安全的基础防线——在 FirstStage 加载 sepolicy，所有后续进程的权限边界都受其管控，默认 enforcing 模式。

- first stage 加载 `sepolicy`（`/system/etc/selinux` 或 `/vendor/etc/selinux`）
- init 早期 `setenforce` 进入 enforcing
- 服务以各自安全上下文运行，越权操作被 avc 拒绝（`dmesg | grep avc`）

### 9. 服务重启与看门狗

init 通过 SIGCHLD 感知子进程退出并自动重启，critical 服务连续崩溃则触发 recovery——这是 Android 防止 bootloop 的最后防线。

- service 可声明 `oneshot`（退出不重启）/ `critical`（崩溃多次触发重启进 recovery）
- `onrestart`：服务重启时执行的命令
- init 通过 `SIGCHLD` 回收子进程并按策略重启，防止关键服务静默退出

---

## 五、Zygote 详解

Zygote 是 Android 的 **ART 孵化器**，由 init 通过 `app_process` 启动，是所有 Java 进程（system_server 与 App）的「母体」。

### 1. 启动流程（源码视角）

```text
init → app_process
  → ZygoteInit.main()
    → preload()            # 预加载类/资源/共享库
    → 注册 zygote socket    # 监听 fork 请求
    → forkSystemServer()   # 先孵化 system_server
    → runSelectLoop()      # 进入循环等待 AMS 的 fork 请求
```

源码：`frameworks/base/core/java/com/android/internal/os/ZygoteInit.java`

### 2. 预加载（preload）

- **preload-classes**：~1800+ framework 常用类
- **preload-resources**：framework 公共资源（图片、布局、drawable）
- **共享库**：libandroid_runtime 等
- 目的：把「公共部分」先在 Zygote 加载好，子进程直接继承

### 3. fork + COW（核心）

<img src="./images/zygote-cow.png" width="500" alt="Zygote fork 与 COW">

- 子进程继承 Zygote 地址空间与已加载类
- 只读页共享，写入时才复制（Copy-On-Write）
- 结果：App 启动快、内存省

### 4. Zygote 进程变体

| 进程                 | 用途                               |
| ------------------ | -------------------------------- |
| `zygote64`         | 主孵化器（64 位），产 system_server + App |
| `zygote`           | 辅助（32 位），兼容旧 App                 |
| `zygote_secondary` | 隔离进程池（USAP，WebView 等）            |

### 5. 为什么不直接新建进程

新建进程要重新加载 ART + framework（慢、费内存）；fork Zygote 则复用已加载内容，几乎零成本。

---

## 六、ServiceManager 详解

ServiceManager 是 **Binder 服务的注册中心（名字服务）**，由 init 最早拉起的 native 进程之一，负责让各进程「按名字找到服务」。

### 1. 它解决什么问题

Android 系统服务（AMS/WMS/PMS…）运行在不同进程，客户端要调用必须先拿到对方的 Binder 句柄。ServiceManager 维护一张「服务名 → Binder 句柄」映射表，充当全局查询入口。

### 2. 工作原理

```text
服务端：publishBinderService("activity", binder) → 注册到 ServiceManager
客户端：getService("activity") → ServiceManager 返回 binder 句柄
        → 之后客户端直接与服务端 Binder 通信（不再经过 ServiceManager）
```

<img src="./images/binder-hub.png" width="340" alt="Binder 与 ServiceManager">

### 3. 关键点

- **handle 0**：ServiceManager 在 Binder 驱动中固定为 context manager（句柄 0），任何进程无需查询即可找到它
- 通过 `BINDER_SET_CONTEXT_MGR` 向驱动注册自己
- 只负责「找对象」，真正的数据传输经 Binder 驱动直达
- 普通服务走 `binder` 域，HAL 服务走独立的 `hwbinder` / `vndservicemanager`

### 4. 源码

`frameworks/native/cmds/servicemanager/`

---

## 七、system_server 详解

system_server 是 Zygote fork 出的**第一个 Java 系统进程**，承载绝大多数系统服务（AMS/WMS/PMS 等），是 framework 层的核心。

### 1. 启动流程

```text
Zygote.forkSystemServer()
  → SystemServer.main()
    → createSystemContext()      # 创建系统上下文
    → startBootstrapServices()   # 引导服务
    → startCoreServices()        # 核心服务
    → startOtherServices()       # 其他服务
    → Looper.loop()              # 进入消息循环
```

源码：`frameworks/base/services/java/com/android/server/SystemServer.java`

### 2. 三批服务

<img src="./images/system-server.png" width="340" alt="system_server 三批服务">

| 批次            | 特征      | 核心服务                                  |
| ------------- | ------- | ------------------------------------- |
| **Bootstrap** | 最优先、互依赖 | AMS, PMS, PowerMS, DisplayMS          |
| **Core**      | 基础设施    | BatteryS, UsageStatsS, WebViewUpdateS |
| **Other**     | 上层功能    | WMS, NotificationMS, LocationMS       |

### 3. 关键服务职责

| 服务          | 职责                     |
| ----------- | ---------------------- |
| **AMS**     | Activity、任务栈、进程与生命周期管理 |
| **WMS**     | 窗口、Surface、焦点          |
| **PMS**     | 应用安装、包信息、权限            |
| **PowerMS** | 亮灭屏、休眠、唤醒锁             |

### 4. 收尾：systemReady()

- 各服务启动后 `publishBinderService()` 注册到 ServiceManager
- AMS 调 `systemReady()`：启动看门狗、发 `BOOT_COMPLETED`、启动 Launcher
- 此时系统服务全部就绪

---

## 八、Launcher 详解

Launcher 是系统的 **HOME 应用（桌面）**，本质上是一个普通 App，但承担系统桌面角色。

### 1. 启动过程

**（1）AMS 决策：启动哪个 Launcher**

```text
AMS.systemReady()
  → startHomeOnAllDisplays()
    → 构造 Intent(ACTION_MAIN, CATEGORY_HOME)
    → resolveActivity() 查询 PMS 中匹配的 Activity
    → 有多个 HOME 时：
        - 若用户已选默认 → 直接用
        - 若无默认 → 弹出选择框（ResolverActivity）
    → 取到目标 Launcher 的 ComponentName
```

**（2）Launcher 进程创建**

```text
AMS.startActivity(intent, LauncherComponentName)
  → 目标进程不存在 → Zygote socket 请求 fork
  → Zygote fork() 出 Launcher 进程
  → 子进程 exec ActivityThread.main()
    → attachApplication() 向 AMS 注册
    → 创建 Application（回调 onCreate）
    → AMS 调度 Activity 生命周期
```

<img src="./images/app-launch.png" width="300" alt="App / Launcher 启动流程">

**（3）Launcher 桌面加载**

```text
LauncherActivity 启动后：
  → 通过 PMS 查询所有 CATEGORY_LAUNCHER 的 Activity
  → 按应用分组生成快捷方式列表
  → inflate workspace 布局（桌面网格）
  → 逐个加载图标（异步，减轻主线程压力）
  → 恢复已有的 AppWidget（RemoteViews 跨进程渲染）
  → 监听应用安装/卸载广播，实时更新桌面图标
```

### 2. 关键点

- Launcher 与普通 App 一样由 Zygote fork、运行 ActivityThread
- 通过 `CATEGORY_HOME` 标识自身为桌面；系统可装多个 Launcher
- 有多个 HOME 时 RESOLVE 机制弹出选择框，用户选默认后记录到 PMS
- 职责：显示桌面图标、管理 widget、响应点击 launch 其他 App
- 按 Home 键回到已运行的 Launcher（Resume，不重新创建）
