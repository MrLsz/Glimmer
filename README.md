# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
│   │  【Android 开发体系】
│   ├── java/               # Java 语言
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

| 文件                                       | 说明                                                   |
| ---------------------------------------- | ---------------------------------------------------- |
| [01-Java基础语法](notes/java/01-Java基础语法.md) | 数据类型、OOP、泛型、反射、注解、异常、Java 8~21 新特性                   |
| [02-Java集合体系](notes/java/02-Java集合体系.md) | List/Map/Set/Queue 全实现类、HashMap 源码、并发容器、fail-fast    |
| [03-Java并发编程](notes/java/03-Java并发编程.md) | 线程、JMM、synchronized、volatile、CAS、AQS、线程池、ThreadLocal |

#### JVM

| 文件 | 说明 |
| ---- | ---- |
| [01-运行时数据区域](notes/jvm/01-运行时数据区域.md) | 五大部分（程序计数器、虚拟机栈、本地方法栈、堆、方法区）、线程共享/私有划分、分代/元空间演进 |

#### Kotlin

| 文件                                             | 说明                                            |
| ---------------------------------------------- | --------------------------------------------- |
| [01-Kotlin基础语法](notes/kotlin/01-Kotlin基础语法.md) | 空安全、函数与 Lambda、类与对象、委托、扩展、泛型、作用域函数等           |
| [02-Kotlin协程](notes/kotlin/02-Kotlin协程.md)     | suspend 原理（CPS+状态机）、调度器、结构化并发、取消、Flow/Channel |

#### Android

| 文件                                                                                     | 说明                                                    |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [01-Android系统结构](notes/mobile/android/01-Android系统结构.md)                               | 六层架构全景：Linux 内核→HAL→运行时→Framework→应用                  |
| [02-Android系统启动分析](notes/mobile/android/02-Android系统启动分析.md)                           | 从加电到 Launcher 的完整进程诞生链                                |
| [03-init进程分析](notes/mobile/android/03-init进程分析.md)                                     | init PID 1：FirstStage/SecondStage、rc 解析、属性服务          |
| [04-Binder系列一-Binder驱动核心概览](notes/mobile/android/04-Binder系列一-Binder驱动核心概览.md)         | 一次拷贝原理、4 大方法、7 种数据结构、BC\_/BR\_ 协议                     |
| [05-Binder系列二-ServiceManager分析](notes/mobile/android/05-Binder系列二-ServiceManager分析.md) | SM 启动三阶段、SET_CONTEXT_MGR、handle 0 获取                  |
| [06-Binder系列三-服务注册与获取分析](notes/mobile/android/06-Binder系列三-服务注册与获取过程分析.md)             | flat_binder_object 改写、注册/获取全链路源码                      |
| [07-Binder系列四-Framework层分析](notes/mobile/android/07-Binder系列四-Framework层分析.md)         | Java 层 JNI 注册、ServiceManager 封装、AIDL 调用链              |
| [08-Zygote进程分析](notes/mobile/android/08-Zygote进程分析.md)                                 | Zygote：ART 孵化器、fork+COW、preload 机制                    |
| [09-SystemServer进程分析](notes/mobile/android/09-system_server进程分析.md)                    | system_server：三批服务发布、AMS.systemReady、Looper 主循环       |
| [10-Launcher启动分析](notes/mobile/android/10-Launcher启动分析.md)                             | Launcher：HOME 应用、resolveActivity、fork、桌面加载            |
| [11-Activity启动过程分析（上）](notes/mobile/android/11-Activity启动过程分析（上）.md)                   | Activity 上：startActivity→ATMS→ActivityStarter→进程创建    |
| [12-Activity启动过程分析（下）](notes/mobile/android/12-Activity启动过程分析（下）.md)                   | Activity 下：attachApplication→ClientTransaction→生命周期回调 |
| [13-Broadcast基础和注册分析](notes/mobile/android/13-Broadcast基础和注册分析.md)                     | Broadcast：观察者模式、分类、动态注册源码                             |
| [14-Broadcast发送和接收过程分析](notes/mobile/android/14-Broadcast发送和接收过程分析.md)                 | Broadcast：sendBroadcast→BroadcastQueue→onReceive 全链路  |

### iOS 开发体系

#### Objective-C

| 文件                                          | 说明                                                      |
| ------------------------------------------- | ------------------------------------------------------- |
| [01-OC基础语法](notes/objective-c/01-OC基础语法.md) | 类、对象、内存管理、消息、协议/委托、Category/Extension、Block、KVC/KVO、集合等 |
| [02-OC多线程](notes/objective-c/02-OC多线程.md)   | 多线程基础、NSThread、GCD、NSOperation、线程安全、RunLoop 保活等         |

#### Swift

| 文件                                          | 说明                                                |
| ------------------------------------------- | ------------------------------------------------- |
| [01-Swift基础语法](notes/swift/01-Swift基础语法.md) | 类型系统、可选类型、集合、控制流、函数闭包、类与结构体、ARC、协议泛型等             |
| [02-Swift多线程](notes/swift/02-Swift多线程.md)   | GCD、锁、async/await、Task、结构化并发、Actor、Sendable、多读单写等 |

#### iOS

| 文件                                                   | 说明                                             |
| ---------------------------------------------------- | ---------------------------------------------- |
| [01-iOS内存管理](notes/mobile/ios/01-iOS内存管理.md)         | 内存分区、堆分配机制、引用计数、ARC、weak 底层、AutoreleasePool 等  |
| [02-类的底层分析](notes/mobile/ios/02-类的底层分析.md)           | objc_class 存储结构逐字段拆解、方法调用原理、协议/分类/扩展的存储与原理     |
| [03-Runtime机制分析](notes/mobile/ios/03-Runtime机制分析.md) | 消息发送与转发（含 NSProxy）、Method Swizzling、关联对象、动态创建类 |

### 算法

LeetCode :  [GLDailyCode](https://github.com/MrLsz/GLDailyCode) 项目，内容与题解可前往该项目查看。

---

*Stay hungry, stay foolish.*
