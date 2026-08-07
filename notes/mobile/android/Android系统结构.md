# Android 系统结构

> 从底层内核到上层应用的完整分层，重点讲清每一层的职责、关键组件，以及层与层之间如何协作。目标：建立一张可长期对照的「Android 全景图」。

## 一、总览

Android 基于 Linux，但在内核之上叠加了专为移动场景设计的运行时与框架。自上而下分为六层：

```
┌─────────────────────────────────────────────┐
│  系统应用层 (System Apps)                      │  Settings / Phone / Launcher …
├─────────────────────────────────────────────┤
│  Java API 框架层 (Application Framework)       │  ActivityManager / WindowManager …
├──────────────────┬──────────────────────────┤
│  Android 运行时     │  原生 C/C++ 库 (Native)   │  ART        |  SQLite / OpenGL …
│  (ART)            │                          │
├──────────────────┴──────────────────────────┤
│  硬件抽象层 (HAL)                             │  Camera HAL / Audio HAL …
├─────────────────────────────────────────────┤
│  Linux 内核层 (Linux Kernel)                   │  进程/内存/网络/驱动/Binder
└─────────────────────────────────────────────┘
```

> 应用开发者日常打交道的，主要是 **Java API 框架层**（SDK 提供的类），以及运行在 **ART** 上的应用进程；其余各层由系统维护。

---

## 二、分层详解

### 1. Linux 内核层（Linux Kernel）

Android 的底座，基于长期支持的 Linux 内核，并打了大量 Android 专有补丁。

**核心职责**
- 进程调度、内存管理、权限（UID/GID）、网络栈
- 设备驱动：显示、相机、音频、蓝牙、USB、Wi-Fi、电池等
- 提供 `Binder` 驱动（IPC 基石）与 `ashmem`（匿名共享内存）

**Android 特有部分**
- **Binder 驱动**：跨进程通信的核心，替代传统 IPC
- **wakelocks**：电源管理，决定 CPU 能否休眠
- **LOW_MEMORY_KILLER**：内存紧张时按优先级杀进程
- **SELinux**：强制访问控制，默认 enforcing 模式

---

### 2. 硬件抽象层（HAL, Hardware Abstraction Layer）

位于内核驱动与框架之间的「接口契约层」，用 C/C++ 实现，以 `.so` 动态库形式存在。

**作用**
- 屏蔽各家芯片/硬件差异，让上层框架无需关心具体实现
- 框架通过 `hwbinder` / `binder` 调用 HAL，HAL 再调内核驱动

**演进**
- **传统 HAL**（旧）：基于 `dlopen` 加载 `module`，如 `camera.default.so`
- **HIDL / AIDL for HAL**（Treble 后，Android 8+）：定义语言描述接口，框架与 HAL 可独立更新、跨进程通信
- **Project Treble**：把 HAL 从 `system` 分区拆出到 `vendor` 分区，实现「框架升级不依赖厂商」

**常见 HAL 模块**：Camera、Audio、Sensors、Graphics (Gralloc/HWC)、蓝牙、NFC。

---

### 3. 原生 C/C++ 库（Native Libraries）

大量底层能力由 C/C++ 编写，通过 JNI 暴露给上层 Java 框架。

| 库 | 职责 |
|---|---|
| **SQLite** | 轻量嵌入式数据库，支撑 `ContentProvider`/`Room` |
| **OpenGL ES / Vulkan / Skia** | 图形渲染；Skia 负责 2D 绘制与 UI 合成 |
| **Webkit / Chromium (WebView)** | 浏览器内核，支撑 `WebView` |
| **OpenSSL / Conscrypt** | 加解密与 TLS |
| **libc (Bionic)** | Android 定制 C 标准库（非 glibc） |
| **Media / Stagefright** | 音视频编解码与播放 |
| **SurfaceFlinger** | 系统图形合成器，把各窗口合成到屏幕 |
| **AudioFlinger** | 音频混合与输出 |

**JNI 桥接**：Java 层方法通过 `native` 关键字调用这些库，例如 `Bitmap`、`AudioTrack`。

---

### 4. Android 运行时（ART, Android Runtime）

每个应用运行在独立的 ART 虚拟机进程中（Android 5.0 起取代 Dalvik）。

**关键机制**
- **AOT 编译**：安装时把 DEX 编译为机器码（OAT），运行更快、更省电
- **JIT 编译**：运行时对热点代码即时编译，配合 Profile 在空闲时做「云配置文件」优化
- **GC**：分代垃圾回收，低暂停；Android 8+ 引入并发 `Concurrent Copying` GC
- **DEX / OAT**：`.dex` 经 `dex2oat` 编译为 `.oat`

**与应用的关系**
- 每个 App 是独立 Linux 进程 + 独立 ART 实例，拥有独立 UID，彼此隔离
- 系统服务（如 `system_server`）也运行在 ART 中，但属于特权进程

---

### 5. Java API 框架层（Application Framework）

开发者通过 SDK 直接调用的「系统服务 + 组件管理」层，绝大多数以 Java 编写，运行在 `system_server` 或各 Binder 服务中。

**核心系统服务**

| 服务 | 职责 |
|---|---|
| **ActivityManagerService (AMS)** | 管理 Activity 生命周期、任务栈、进程调度 |
| **WindowManagerService (WMS)** | 窗口层级、Surface 管理、输入焦点 |
| **PackageManagerService (PMS)** | 应用安装、权限、组件查询 |
| **PowerManagerService** | 唤醒锁、屏幕、休眠策略 |
| **NotificationManagerService** | 通知分发 |
| **LocationManagerService** | 定位 |
| **ConnectivityService** | 网络状态与连接管理 |

**四大组件（应用开发基石）**
- **Activity**：单一屏幕界面，受 AMS 生命周期管理
- **Service**：后台长任务，分启动式与绑定式
- **BroadcastReceiver**：跨应用/系统事件广播
- **ContentProvider**：跨进程结构化数据共享

**关键概念**
- **Context**：全局环境句柄，是访问资源的入口
- **Binder IPC**：跨进程调用四大组件、系统服务均经 Binder
- **Intent**：组件间通信的「信使」

---

### 6. 系统应用层（System Apps）

预装应用与用户安装的应用，位于架构最顶层，完全运行在 ART 之上，调用的全是框架层 API。

- **系统应用**：Launcher、Settings、Phone、Contacts、SystemUI 等，拥有更高权限（signature|privileged）
- **用户应用**：普通 App，沙箱隔离，仅能访问自身数据与被授予的权限

---

## 三、关键跨层机制

### Binder IPC
Android 的跨进程通信 backbone。C/S 模型：Client 经 `ServiceManager` 拿到对端句柄，通过 `ioctl` 与内核 Binder 驱动交互，驱动负责线程调度与数据拷贝（仅一次拷贝）。`AIDL` 是其接口描述语言。

### JNI（Java Native Interface）
连接 Java 框架与原生库的桥。应用层 `native` 方法、系统服务中的性能敏感路径都经此下沉到 C/C++。

### 启动流程（简述）
1. 上电 → Bootloader → 加载 Linux 内核
2. 内核启动 `init` 进程（PID 1），解析 `init.rc`
3. `init` 拉起 `zygote`（ART 孵化器）→ `system_server`（框架服务）
4. `system_server` 启动各系统服务，AMS 拉起 `SystemUI` 与 `Launcher`
5. 用户点击图标 → AMS 通过 Zygote `fork` 出应用进程 → 执行 `ActivityThread`

### 分区（简要）
- `boot`：内核与 ramdisk
- `system`：框架与系统应用（Treble 后框架可独立 OTA）
- `vendor`：厂商 HAL 实现
- `userdata`：用户数据与应用
- `cache` / `recovery` 等辅助分区

---

## 四、一句话记忆

> **Linux 打底 → HAL 屏蔽硬件 → 原生库提供能力 → ART 跑应用 → 框架层管组件与服务 → 应用层落地功能**；层间靠 **Binder（进程间）** 与 **JNI（语言间）** 串联。

---

*参考主线：Android 官方 Architecture 文档 + AOSP 源码结构。建议结合 `adb shell dumpsys` 观察实际运行中的服务与进程。*
