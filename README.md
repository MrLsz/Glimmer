# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
│   │  【Android 开发体系】
│   ├── mobile/android/     # Android 系统开发
│   │   ├── platform/       # Android 平台相关文档
│   │   │   ├── boot/         # 系统架构与启动
│   │   │   ├── binder/       # Binder IPC 机制
│   │   │   ├── component/    # 四大组件
│   │   │   ├── window-input/ # Window 与输入体系
│   │   │   ├── view-render/  # View 绘制与渲染
│   │   │   └── build-system/ # 构建与编译体系
│   │   ├── java/           # Java 语言
│   │   ├── kotlin/         # Kotlin 语言
│   │   ├── jvm/            # JVM 原理
│   │   └── matrix/         # Matrix APM 源码分析
│   │  【iOS 开发体系】
│   ├── objective-c/        # Objective-C 语言
│   ├── swift/              # Swift 语言
│   ├── mobile/ios/         # iOS 开发
│   │   ├── runtime/        # 语言与运行时
│   │   ├── foundation/     # 系统底层机制
│   │   ├── uikit/          # UIKit 框架
│   │   └── startup/        # 启动与构建
│   │  【HarmonyOS 开发体系】
│   ├── mobile/harmonyos/   # ArkTS / ArkUI / Ability
│   │  【通用】
│   ├── framework-design/   # 框架设计与原理
│   ├── algorithm/          # 算法与数据结构
│   └── ai-ml/              # Python / AI / 机器学习
├── experience/             # 经验积累
│   ├── troubleshooting/    # 踩坑记录 & 故障排查
│   ├── best-practices/     # 最佳实践
│   └── code-snippets/      # 实用代码片段
└── projects/               # 项目复盘 & 总结
```

## 文章索引

### Android 开发体系

#### Java

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Java基础语法](notes/mobile/android/java/01-Java基础语法.md) | 数据类型、OOP、泛型、反射、注解、异常、新特性 |
| 2 | [Java集合体系](notes/mobile/android/java/02-Java集合体系.md) | List/Map/Set/Queue、HashMap 源码、并发容器 |
| 3 | [Java集合-List](notes/mobile/android/java/03-Java集合-List.md) | List 的继承体系、ArrayList/LinkedList/Vector/ Stack、CopyOnWriteArrayList 内容 |
| 4 | [Java并发编程](notes/mobile/android/java/04-Java并发编程.md) | 线程、JMM、synchronized、volatile、CAS、AQS、线程池 |

#### Kotlin

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Kotlin基础语法](notes/mobile/android/kotlin/01-Kotlin基础语法.md) | 空安全、Lambda 、类与对象、委托、扩展、泛型、作用域、集合、其他高级特性 |
| 2 | [Kotlin协程原理](notes/mobile/android/kotlin/02-Kotlin协程.md) | suspend 原理、调度器、结构化并发、Flow/Channel |

#### JVM

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [JVM整体结构](notes/mobile/android/jvm/01-JVM整体结构概述.md) | JDK/JRE/JVM 关系、运行全流程、架构图、版本演进 |
| 2 | [类加载机制一-class文件分析](notes/mobile/android/jvm/02-类加载机制一-class文件分析.md) | .java→.class 编译、Class 文件结构 |
| 3 | [类加载机制二-类加载过程分析](notes/mobile/android/jvm/03-类加载机制二-类加载过程分析.md) | 加载→连接→初始化、clinit vs init、主动/被动引用 |
| 4 | [类加载机制三-双亲委派机制](notes/mobile/android/jvm/04-类加载机制三-双亲委派机制.md) | 类加载器层次、双亲委派、loadClass 源码、类卸载 |
| 5 | [程序计数器](notes/mobile/android/jvm/05-程序计数器分析.md) | 运行时数据区总览、程序计数器、字节码指令速查 |
| 6 | [虚拟机栈和本地方法栈](notes/mobile/android/jvm/06-虚拟机栈和本地方法栈分析.md) | 虚拟机栈与栈帧、本地方法栈与 JNI |
| 7 | [堆分析](notes/mobile/android/jvm/07-堆分析.md) | 堆、存活判定、垃圾收集算法、对象布局、TLAB、逃逸分析 |
| 8 | [方法区(元空间)](<notes/mobile/android/jvm/08-方法区(元空间)分析.md>) | 方法区与常量池、永久代→元空间、元空间结构、类卸载 |
| 9 | [JVM核心流程总结](notes/mobile/android/jvm/09-JVM核心流程总结.md) | 源码→字节码→加载→执行全流程概括、Animal/Dog/Main 的总结 |

#### Matrix

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Matrix总体架构与插件体系](notes/mobile/android/matrix/01-Matrix总体架构与插件体系.md) | 整体架构、Plugin状态机与生命周期、Issue上报链路、多进程生命周期 |

#### Android

##### 系统架构与启动

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Android系统结构](notes/mobile/android/platform/boot/01-Android系统结构.md) | 六层架构：Linux 内核→ HAL →运行时→Framework → 应用的整体结构概览 |
| 2 | [Android系统启动原理](notes/mobile/android/platform/boot/02-Android系统启动分析.md) | 加电到 Launcher 的完整进程诞生链 |
| 3 | [init进程](notes/mobile/android/platform/boot/03-init进程分析.md) | init PID 1：rc 解析、属性服务 |
| 4 | [Zygote进程](notes/mobile/android/platform/boot/04-Zygote进程分析.md) | Zygote：fork+COW、preload 机制 |
| 5 | [SystemServer进程](notes/mobile/android/platform/boot/05-system_server进程分析.md) | system_server：三批服务发布、systemReady |
| 6 | [Launcher启动原理](notes/mobile/android/platform/boot/06-Launcher启动分析.md) | Launcher：HOME 应用、桌面加载 |

##### Binder IPC 机制

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Binder系列一-Binder驱动核心概览](notes/mobile/android/platform/binder/01-Binder系列一-Binder驱动核心概览.md) | 一次拷贝原理、4 大方法、7种结构、BC\_/BR\_ 协议的概览 |
| 2 | [Binder系列二-ServiceManager分析](notes/mobile/android/platform/binder/02-Binder系列二-ServiceManager分析.md) | SM 启动三阶段、SET\_CONTEXT\_MGR、handle 0 |
| 3 | [Binder系列三-服务注册与获取过程分析](notes/mobile/android/platform/binder/03-Binder系列三-服务注册与获取过程分析.md) | flat\_binder\_object 改写、注册/获取全链路 |
| 4 | [Binder系列四-Framework层分析](notes/mobile/android/platform/binder/04-Binder系列四-Framework层分析.md) | JNI 注册、ServiceManager 封装、AIDL 调用链 |

##### 四大组件

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Activity启动过程分析（上）](notes/mobile/android/platform/component/01-Activity启动过程分析（上）.md) | Activity 上：startActivity→ATMS→进程创建的详细过程分析 |
| 2 | [Activity启动过程分析（下）](notes/mobile/android/platform/component/02-Activity启动过程分析（下）.md) | Activity 下：attachApplication→生命周期回调 |
| 3 | [Broadcast基础和注册](notes/mobile/android/platform/component/03-Broadcast基础和注册分析.md) | Broadcast：观察者模式、动态注册 |
| 4 | [Broadcast发送和接收过程](notes/mobile/android/platform/component/04-Broadcast发送和接收过程分析.md) | Broadcast：sendBroadcast→onReceive 全链路 |
| 5 | [Service基础与startService分析](notes/mobile/android/platform/component/05-Service基础与startService分析.md) | Service：生命周期、startService 全链路 |
| 6 | [Service的bindService分析](notes/mobile/android/platform/component/06-Service的bindService分析.md) | Service：bindService 全链路、IBinder 回传 |
| 7 | [ContentProvider基础与启动流程分析](notes/mobile/android/platform/component/07-ContentProvider基础与启动流程分析.md) | ContentProvider：概念与启动安装全链路 |
| 8 | [ContentProvider调用流程](notes/mobile/android/platform/component/08-ContentProvider调用流程分析.md) | ContentProvider：query 调用全链路 |

##### Window 与输入体系

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Window体系](notes/mobile/android/platform/window-input/01-Window体系分析.md) | Window 层级、addView 全流程、Dialog/Toast |
| 2 | [Context体系](notes/mobile/android/platform/window-input/02-Context体系分析.md) | Context 继承体系、ContextWrapper、组件 Context 创建 |
| 3 | [输入事件分析一-获取过程](<notes/mobile/android/platform/window-input/03-输入事件分析一-获取过程.md>) | 输入系统总览、IMS、InputReader 主循环、InputMapper、点击读取 |
| 4 | [输入事件分析二-派发过程](<notes/mobile/android/platform/window-input/04-输入事件分析二-派发过程.md>) | 三队列、InputChannel、窗口同步、命中测试、派发执行、ANR |
| 5 | [输入事件分析三-应用层处理](<notes/mobile/android/platform/window-input/05-输入事件分析三-应用层处理.md>) | InputStage 七级责任链、View 树分发、FINISHED 闭环 |

##### View 绘制与渲染

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [View绘制的三大流程](notes/mobile/android/platform/view-render/01-View绘制的三个流程.md) | measure/layout/draw、requestLayout/ nvalidate详细过程分析，源码学习 |
| 2 | [View绘制原理深度剖析](notes/mobile/android/platform/view-render/02-绘制原理深度剖析.md) | 软硬绘制、RenderNode、RenderThread、SurfaceFlinger |

##### 构建与编译体系

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Android编译流程解析](notes/mobile/android/platform/build-system/01-Android编译流程解析.md) | Gradle/AGP、AAPT2 两阶段、d8/R8、签名对齐、Soong/Ninja、APK打包等 |

### iOS 开发体系

#### Objective-C

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [OC基础语法](notes/objective-c/01-OC基础语法.md) | 类、对象、内存管理、消息、Category 、Block、KVC/KVO、常用集合类、错误处理 |
| 2 | [OC多线程总结](notes/objective-c/02-OC多线程.md) | NSThread、GCD、NSOperation、线程安全、RunLoop |

#### Swift

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Swift基础语法](notes/swift/01-Swift基础语法.md) | 类型系统、字符串、可选类型、集合与 COW、闭包、高阶函数、类与结构体、 |
| 2 | [Swift多线程语法总结](notes/swift/02-Swift多线程.md) | GCD、async/await、Task、Actor、多读单写 |

#### iOS

##### 语言与运行时

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [NSObject底层原理](notes/mobile/ios/runtime/01-NSObject底层分析.md) | objc_object 、isa 位域、字节对齐与优化、元类闭环、Tagged Pointer、alloc等 |
| 2 | [类的底层存储](notes/mobile/ios/runtime/02-类的底层分析.md) | objc_class 存储结构、方法调用原理 |
| 3 | [Runtime机制总结](notes/mobile/ios/runtime/03-Runtime机制分析.md) | 消息发送转发、Method Swizzling、关联对象 |
| 4 | [KVC机制总结分析](notes/mobile/ios/runtime/04-KVC机制分析.md) | 键值编码、setValue/valueForKey 查找链路、KeyPath 集合运算符 |
| 5 | [KVO机制分析总结](notes/mobile/ios/runtime/05-KVO机制分析.md) | isa-swizzling、重写 setter、观察者存储、手动 KVO |
| 6 | [Block底层分析](notes/mobile/ios/runtime/06-Block底层分析.md) | Block 本质、__block_impl 结构体、三种类型、copy/捕获/循环引用 |
| 7 | [反射机制](notes/mobile/ios/runtime/07-反射机制分析.md) | OC Runtime 内省与动态操作、Swift Mirror、类型编码、应用场景 |
| 8 | [load与initialize区别](notes/mobile/ios/runtime/08-load与initialize分析.md) | 调用时机与底层源码、直调 vs消息发送、Category/继承行为差异、Swizzling时机 |

##### 系统底层机制

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [iOS内存管理机制](notes/mobile/ios/foundation/01-iOS内存管理.md) | 内存分区、堆内存分配、引用计数、ARC、weak、循环引用、AutoreleasePool、等 |
| 2 | [RunLoop机制详解](notes/mobile/ios/foundation/02-RunLoop机制分析.md) | 事件循环、Mode、Source/Timer/Observer、线程保活 |

##### UIKit 框架

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [UIWindow体系结构](notes/mobile/ios/uikit/01-UIWindow体系分析.md) | UIScene/UIWindow/VC/NVC 层级关系、keyWindow、VC栈管理等 |
| 2 | [UIView体系分析](notes/mobile/ios/uikit/02-UIView体系分析.md) | 三重身份、几何坐标、视图树、布局渲染、UIWindow、hit-test  |
| 3 | [UIViewController机制](notes/mobile/ios/uikit/03-UIViewController机制分析.md) | view 懒加载、loadView、生命周期、容器控制器、present |
| 4 | [UINavigationController机制](notes/mobile/ios/uikit/04-UINavigationController机制分析.md) | 导航栈、push / pop 流程、UINavigationBar、侧滑返回手势、转场动画等 |
| 5 | [事件响应链机制分析](notes/mobile/ios/uikit/05-事件响应链机制分析.md) | 触摸全链路、hit-test、手势分发、UIControl、响应者链 |
| 6 | [布局方法详解](notes/mobile/ios/uikit/06-布局方法详解.md) | Frame/Auto Layout/StackView、Cassowary 求解、更新三阶段 |
| 7 | [UI渲染机制原理分析](notes/mobile/ios/uikit/07-UI渲染机制原理分析.md) | VSync、三棵图层树、渲染管线、布局标记、RunLoop 提交、 |

##### 启动与构建

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [App启动过程分析](notes/mobile/ios/startup/01-App启动过程分析.md) | 冷/热/预热启动、Pre-main 七步、dyld 演进、main 阶段、启动优化 |
| 2 | [import背后的机制要点](notes/mobile/ios/startup/02-import详解.md) | OC查找机制、Header Map、Clang Modules、Swift模块系统、混编操作 |
| 3 | [Mach-O文件格式](notes/mobile/ios/startup/03-Mach-O文件格式分析.md) | Mach-O 格式、Segment/Section、静态与动态库、Rebase/Bind、dyld 装载 |
| 4 | [Framework详解](notes/mobile/ios/runtime/09-Framework详解.md) | 目录结构与Umbrella/Module、静态 / 动态与LTO、链接加载dyld、CocoaPods |

### HarmonyOS 开发体系

#### ArkTS

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [ArkTS基础语法](notes/mobile/harmonyos/01-ArkTS基础语法.md) | 类型系统、类与泛型、模块命名空间、流程控制、类型断言、空安全、并发、TS 差异等 |
| 2 | [ArkUI基础语法](notes/mobile/harmonyos/02-ArkUI基础语法.md) | 组件结构、布局容器、基础组件、渲染控制、状态装饰器 V1/V2、UI 复用 |

### 框架设计与原理

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [移动端主流架构思想概览](notes/framework-design/01-移动端主流架构思想概览.md) | MVC/MVP/MVVM/MVI、Flux/Redux/Elm/TCA、Clean/洋葱、VIPER/RIBs |

### AI 开发

#### Python

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Python基础语法](notes/ai-ml/01-Python基础语法.md) | 对象模型、可变/ 不可变、深浅拷贝、序列与切片、推导式、装饰器、多继承MRO、 |

#### 学习Hello-Agents框架

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Hello-Agents：智能体及其发展史](notes/ai-ml/02-学习Hello-Agents：智能体及其发展史.md) | 智能体定义与类型、Agent Loop、智能体演进、现代 LLM |
| 2 | [Hello-Agents：大语言模型基础](notes/ai-ml/03-学习Hello-Agents：大语言模型基础.md) | N-gram→Transformer 演进、自/多头注意力、Prompt |
| 3 | [Hello-Agents：智能体经典范式](notes/ai-ml/04-学习Hello-Agents：智能体经典范式.md) | ReAct / Plan-and-Solve / Reflection 三大范式原理、工具调用 |
| 4 | [Hello-Agents：低代码平台与Agent框架](notes/ai-ml/05-学习Hello-Agents：低代码平台与Agent框架.md) | 低代码平台、、AutoGen/AgentScope/CAMEL/LangGraph |
| 5 | [Hello-Agents：Memory](notes/ai-ml/06-学习Hello-Agents：Memory.md) | 记忆维度、三种形态、四类记忆、RAG实现形式、记忆评估 |

### 算法

LeetCode :  [GLDailyCode](https://github.com/MrLsz/GLDailyCode) 项目，内容与题解可前往该项目查看。

---

*Stay hungry, stay foolish.*
