# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
│   │  【Android 开发体系】
│   ├── java/               # Java 语言
│   ├── jvm/                # JVM 原理
│   ├── kotlin/             # Kotlin 语言
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

| 文件 | 说明 |
| ---- | ---- |
| [01-Java基础语法](notes/java/01-Java基础语法.md) | 数据类型、OOP、泛型、反射、注解、异常、新特性 |
| [02-Java集合体系](notes/java/02-Java集合体系.md) | List/Map/Set/Queue、HashMap 源码、并发容器 |
| [03-Java并发编程](notes/java/03-Java并发编程.md) | 线程、JMM、synchronized、volatile、CAS、AQS、线程池 |

#### JVM

| 文件 | 说明 |
| ---- | ---- |
| [01-JVM整体结构概述](notes/jvm/01-JVM整体结构概述.md) | JDK/JRE/JVM 关系、运行全流程、架构图、版本演进 |
| [03-类加载机制一-class文件分析](notes/jvm/03-类加载机制一-class文件分析.md) | .java→.class 编译、Class 文件结构 |
| [04-类加载机制二-类加载过程分析](notes/jvm/04-类加载机制二-类加载过程分析.md) | 加载→连接→初始化、clinit vs init、主动/被动引用 |
| [05-类加载机制三-双亲委派机制](notes/jvm/05-类加载机制三-双亲委派机制.md) | 类加载器层次、双亲委派、loadClass 源码、类卸载 |
| [06-运行时数据区一-程序计数器](notes/jvm/06-运行时数据区一-程序计数器.md) | 运行时数据区总览、程序计数器、字节码指令速查 |
| [07-运行时数据区二-虚拟机栈和本地方法栈](notes/jvm/07-运行时数据区二-虚拟机栈和本地方法栈.md) | 虚拟机栈与栈帧、本地方法栈与 JNI |
| [08-运行时数据区三-堆](notes/jvm/08-运行时数据区三-堆.md) | 堆、存活判定、垃圾收集算法、对象布局、TLAB、逃逸分析 |
| [09-运行时数据区四-方法区(元空间)](<notes/jvm/09-运行时数据区四-方法区(元空间).md>) | 方法区与常量池、永久代→元空间、元空间结构、类卸载 |
| [10-JVM核心流程总结](notes/jvm/10-JVM核心流程总结.md) | 源码→字节码→加载→执行全流程、Animal/Dog/Main 例子、7 图 |

#### Kotlin

| 文件 | 说明 |
| ---- | ---- |
| [01-Kotlin基础语法](notes/kotlin/01-Kotlin基础语法.md) | 空安全、Lambda、类与对象、委托、扩展、泛型 |
| [02-Kotlin协程](notes/kotlin/02-Kotlin协程.md) | suspend 原理、调度器、结构化并发、Flow/Channel |

#### Android

| 文件 | 说明 |
| ---- | ---- |
| [01-Android系统结构](notes/mobile/android/01-Android系统结构.md) | 六层架构：Linux 内核→HAL→运行时→Framework→应用 |
| [02-Android系统启动分析](notes/mobile/android/02-Android系统启动分析.md) | 加电到 Launcher 的完整进程诞生链 |
| [03-init进程分析](notes/mobile/android/03-init进程分析.md) | init PID 1：rc 解析、属性服务 |
| [04-Binder系列一-Binder驱动核心概览](notes/mobile/android/04-Binder系列一-Binder驱动核心概览.md) | 一次拷贝原理、4 大方法、7 种结构、BC\_/BR\_ 协议 |
| [05-Binder系列二-ServiceManager分析](notes/mobile/android/05-Binder系列二-ServiceManager分析.md) | SM 启动三阶段、SET\_CONTEXT\_MGR、handle 0 |
| [06-Binder系列三-服务注册与获取分析](notes/mobile/android/06-Binder系列三-服务注册与获取过程分析.md) | flat\_binder\_object 改写、注册/获取全链路 |
| [07-Binder系列四-Framework层分析](notes/mobile/android/07-Binder系列四-Framework层分析.md) | JNI 注册、ServiceManager 封装、AIDL 调用链 |
| [08-Zygote进程分析](notes/mobile/android/08-Zygote进程分析.md) | Zygote：fork+COW、preload 机制 |
| [09-SystemServer进程分析](notes/mobile/android/09-system_server进程分析.md) | system_server：三批服务发布、systemReady |
| [10-Launcher启动分析](notes/mobile/android/10-Launcher启动分析.md) | Launcher：HOME 应用、桌面加载 |
| [11-Activity启动过程分析（上）](notes/mobile/android/11-Activity启动过程分析（上）.md) | Activity 上：startActivity→ATMS→进程创建 |
| [12-Activity启动过程分析（下）](notes/mobile/android/12-Activity启动过程分析（下）.md) | Activity 下：attachApplication→生命周期回调 |
| [13-Broadcast基础和注册分析](notes/mobile/android/13-Broadcast基础和注册分析.md) | Broadcast：观察者模式、动态注册 |
| [14-Broadcast发送和接收过程分析](notes/mobile/android/14-Broadcast发送和接收过程分析.md) | Broadcast：sendBroadcast→onReceive 全链路 |
| [15-Service基础与startService分析](notes/mobile/android/15-Service基础与startService分析.md) | Service：生命周期、startService 全链路 |
| [16-Service的bindService分析](notes/mobile/android/16-Service的bindService分析.md) | Service：bindService 全链路、IBinder 回传 |
| [17-ContentProvider基础与启动流程分析](notes/mobile/android/17-ContentProvider基础与启动流程分析.md) | ContentProvider：概念与启动安装全链路 |
| [18-ContentProvider调用流程分析](notes/mobile/android/18-ContentProvider调用流程分析.md) | ContentProvider：query 调用全链路 |

### iOS 开发体系

#### Objective-C

| 文件 | 说明 |
| ---- | ---- |
| [01-OC基础语法](notes/objective-c/01-OC基础语法.md) | 类、对象、内存管理、消息、Category、Block、KVC/KVO |
| [02-OC多线程](notes/objective-c/02-OC多线程.md) | NSThread、GCD、NSOperation、线程安全、RunLoop |

#### Swift

| 文件 | 说明 |
| ---- | ---- |
| [01-Swift基础语法](notes/swift/01-Swift基础语法.md) | 类型系统、可选类型、闭包、ARC、协议泛型 |
| [02-Swift多线程](notes/swift/02-Swift多线程.md) | GCD、async/await、Task、Actor、多读单写 |

#### iOS

| 文件 | 说明 |
| ---- | ---- |
| [01-iOS内存管理](notes/mobile/ios/01-iOS内存管理.md) | 内存分区、引用计数、ARC、weak、AutoreleasePool |
| [02-类的底层分析](notes/mobile/ios/02-类的底层分析.md) | objc_class 存储结构、方法调用原理 |
| [03-Runtime机制分析](notes/mobile/ios/03-Runtime机制分析.md) | 消息发送转发、Method Swizzling、关联对象 |
| [04-RunLoop机制分析](notes/mobile/ios/04-RunLoop机制分析.md) | 事件循环、Mode、Source/Timer/Observer、12 步流程、线程保活 |

### 算法

LeetCode :  [GLDailyCode](https://github.com/MrLsz/GLDailyCode) 项目，内容与题解可前往该项目查看。

---

*Stay hungry, stay foolish.*
