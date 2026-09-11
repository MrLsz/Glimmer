# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
│   │  【Android 开发体系】
│   ├── java/               # Java 语言
│   ├── kotlin/             # Kotlin 语言
│   ├── jvm/                # JVM 原理
│   ├── mobile/android/     # Android 系统开发
│   │  【iOS 开发体系】
│   ├── objective-c/        # Objective-C 语言
│   ├── swift/              # Swift 语言
│   ├── mobile/ios/         # iOS 开发
│   ├── framework-design/   # 框架设计与原理
│   ├── algorithm/          # 算法与数据结构
│   └── ai-ml/              # AI / 机器学习
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
| 1 | [Java基础语法](notes/java/Java基础语法.md) | 数据类型、OOP、泛型、反射、注解、异常、新特性 |
| 2 | [Java集合体系](notes/java/Java集合体系.md) | List/Map/Set/Queue、HashMap 源码、并发容器 |
| 3 | [Java集合-List](notes/java/Java集合-List.md) | List 继承体系、ArrayList/LinkedList/Vector/Stack、CopyOnWriteArrayList |
| 4 | [Java并发编程](notes/java/Java并发编程.md) | 线程、JMM、synchronized、volatile、CAS、AQS、线程池 |

#### Kotlin

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Kotlin基础语法](notes/kotlin/Kotlin基础语法.md) | 空安全、Lambda、类与对象、委托、扩展、泛型 |
| 2 | [Kotlin协程](notes/kotlin/Kotlin协程.md) | suspend 原理、调度器、结构化并发、Flow/Channel |

#### JVM

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [JVM整体结构概述](notes/jvm/JVM整体结构概述.md) | JDK/JRE/JVM 关系、运行全流程、架构图、版本演进 |
| 2 | [类加载机制一-class文件分析](notes/jvm/类加载机制一-class文件分析.md) | .java→.class 编译、Class 文件结构 |
| 3 | [类加载机制二-类加载过程分析](notes/jvm/类加载机制二-类加载过程分析.md) | 加载→连接→初始化、clinit vs init、主动/被动引用 |
| 4 | [类加载机制三-双亲委派机制](notes/jvm/类加载机制三-双亲委派机制.md) | 类加载器层次、双亲委派、loadClass 源码、类卸载 |
| 5 | [程序计数器分析](notes/jvm/程序计数器分析.md) | 运行时数据区总览、程序计数器、字节码指令速查 |
| 6 | [虚拟机栈和本地方法栈分析](notes/jvm/虚拟机栈和本地方法栈分析.md) | 虚拟机栈与栈帧、本地方法栈与 JNI |
| 7 | [堆分析](notes/jvm/堆分析.md) | 堆、存活判定、垃圾收集算法、对象布局、TLAB、逃逸分析 |
| 8 | [方法区(元空间)分析](<notes/jvm/方法区(元空间)分析.md>) | 方法区与常量池、永久代→元空间、元空间结构、类卸载 |
| 9 | [JVM核心流程总结](notes/jvm/JVM核心流程总结.md) | 源码→字节码→加载→执行全流程、Animal/Dog/Main 例子、7 图 |

#### Android

##### 系统架构与启动

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Android系统结构](notes/mobile/android/Android系统结构.md) | 六层架构：Linux 内核→HAL→运行时→Framework→应用 |
| 2 | [Android系统启动分析](notes/mobile/android/Android系统启动分析.md) | 加电到 Launcher 的完整进程诞生链 |
| 3 | [init进程分析](notes/mobile/android/init进程分析.md) | init PID 1：rc 解析、属性服务 |
| 4 | [Zygote进程分析](notes/mobile/android/Zygote进程分析.md) | Zygote：fork+COW、preload 机制 |
| 5 | [SystemServer进程分析](notes/mobile/android/system_server进程分析.md) | system_server：三批服务发布、systemReady |
| 6 | [Launcher启动分析](notes/mobile/android/Launcher启动分析.md) | Launcher：HOME 应用、桌面加载 |

##### Binder IPC 机制

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Binder系列一-Binder驱动核心概览](notes/mobile/android/Binder系列一-Binder驱动核心概览.md) | 一次拷贝原理、4 大方法、7 种结构、BC\_/BR\_ 协议 |
| 2 | [Binder系列二-ServiceManager分析](notes/mobile/android/Binder系列二-ServiceManager分析.md) | SM 启动三阶段、SET\_CONTEXT\_MGR、handle 0 |
| 3 | [Binder系列三-服务注册与获取过程分析](notes/mobile/android/Binder系列三-服务注册与获取过程分析.md) | flat\_binder\_object 改写、注册/获取全链路 |
| 4 | [Binder系列四-Framework层分析](notes/mobile/android/Binder系列四-Framework层分析.md) | JNI 注册、ServiceManager 封装、AIDL 调用链 |

##### 四大组件

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Activity启动过程分析（上）](notes/mobile/android/Activity启动过程分析（上）.md) | Activity 上：startActivity→ATMS→进程创建 |
| 2 | [Activity启动过程分析（下）](notes/mobile/android/Activity启动过程分析（下）.md) | Activity 下：attachApplication→生命周期回调 |
| 3 | [Broadcast基础和注册分析](notes/mobile/android/Broadcast基础和注册分析.md) | Broadcast：观察者模式、动态注册 |
| 4 | [Broadcast发送和接收过程分析](notes/mobile/android/Broadcast发送和接收过程分析.md) | Broadcast：sendBroadcast→onReceive 全链路 |
| 5 | [Service基础与startService分析](notes/mobile/android/Service基础与startService分析.md) | Service：生命周期、startService 全链路 |
| 6 | [Service的bindService分析](notes/mobile/android/Service的bindService分析.md) | Service：bindService 全链路、IBinder 回传 |
| 7 | [ContentProvider基础与启动流程分析](notes/mobile/android/ContentProvider基础与启动流程分析.md) | ContentProvider：概念与启动安装全链路 |
| 8 | [ContentProvider调用流程分析](notes/mobile/android/ContentProvider调用流程分析.md) | ContentProvider：query 调用全链路 |

##### Window 与输入体系

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Window体系分析](notes/mobile/android/Window体系分析.md) | Window 层级、addView 全流程、Dialog/Toast |
| 2 | [Context体系分析](notes/mobile/android/Context体系分析.md) | Context 继承体系、ContextWrapper、组件 Context 创建 |
| 3 | [输入事件分析一-获取过程](<notes/mobile/android/输入事件分析一-获取过程.md>) | 输入系统总览、IMS、InputReader 主循环、InputMapper、点击读取 |
| 4 | [输入事件分析二-派发过程](<notes/mobile/android/输入事件分析二-派发过程.md>) | 三队列、InputChannel、窗口同步、命中测试、派发执行、ANR |
| 5 | [输入事件分析三-应用层处理](<notes/mobile/android/输入事件分析三-应用层处理.md>) | InputStage 七级责任链、View 树分发、FINISHED 闭环 |

##### View 绘制与渲染

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [View绘制的三个流程](notes/mobile/android/View绘制的三个流程.md) | measure/layout/draw、requestLayout/invalidate |
| 2 | [绘制原理深度剖析](notes/mobile/android/绘制原理深度剖析.md) | 软硬绘制、RenderNode、RenderThread、SurfaceFlinger |

### iOS 开发体系

#### Objective-C

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [OC基础语法](notes/objective-c/OC基础语法.md) | 类、对象、内存管理、消息、Category、Block、KVC/KVO |
| 2 | [OC多线程](notes/objective-c/OC多线程.md) | NSThread、GCD、NSOperation、线程安全、RunLoop |

#### Swift

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [Swift基础语法](notes/swift/Swift基础语法.md) | 类型系统、可选类型、闭包、ARC、协议泛型 |
| 2 | [Swift多线程](notes/swift/Swift多线程.md) | GCD、async/await、Task、Actor、多读单写 |

#### iOS

| 序号 | 文件 | 说明 |
| :---: | ---- | ---- |
| 1 | [iOS内存管理](notes/mobile/ios/iOS内存管理.md) | 内存分区、引用计数、ARC、weak、AutoreleasePool |
| 2 | [类的底层分析](notes/mobile/ios/类的底层分析.md) | objc_class 存储结构、方法调用原理 |
| 3 | [Runtime机制分析](notes/mobile/ios/Runtime机制分析.md) | 消息发送转发、Method Swizzling、关联对象 |
| 4 | [RunLoop机制分析](notes/mobile/ios/RunLoop机制分析.md) | 事件循环、Mode、Source/Timer/Observer、线程保活 |
| 5 | [KVC机制分析](notes/mobile/ios/KVC机制分析.md) | 键值编码、setValue/valueForKey 查找链路、KeyPath 集合运算符 |
| 6 | [KVO机制分析](notes/mobile/ios/KVO机制分析.md) | isa-swizzling、重写 setter、观察者存储、手动 KVO |
| 7 | [Block底层分析](notes/mobile/ios/Block底层分析.md) | Block 本质、__block_impl 结构体、三种类型、copy/捕获/循环引用 |
| 8 | [NSObject底层分析](notes/mobile/ios/NSObject底层分析.md) | objc_object、isa 位域、元类闭环、Tagged Pointer、alloc |

### 算法

LeetCode :  [GLDailyCode](https://github.com/MrLsz/GLDailyCode) 项目，内容与题解可前往该项目查看。

---

*Stay hungry, stay foolish.*
