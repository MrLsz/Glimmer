# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
│   ├── java/               # Java 语言
│   ├── kotlin/             # Kotlin 语言
│   ├── objective-c/        # Objective-C 语言
│   ├── swift/              # Swift 语言
│   ├── mobile/             # 客户端开发
│   │   ├── android/        # Android 开发
│   │   └── ios/            # iOS 开发
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

### Java

| 文件 | 说明 |
|------|------|
| [01-Java基础语法.md](notes/java/01-Java基础语法.md) | 数据类型、OOP、泛型、反射、注解、异常、Java 8~21 新特性 |
| [02-Java集合体系.md](notes/java/02-Java集合体系.md) | List/Map/Set/Queue 全实现类、HashMap 源码、并发容器、fail-fast |
| [03-Java并发编程.md](notes/java/03-Java并发编程.md) | 线程、JMM、synchronized、volatile、CAS、AQS、线程池、ThreadLocal |

### Kotlin

| 文件 | 说明 |
|------|------|
| [01-Kotlin基础语法.md](notes/kotlin/01-Kotlin基础语法.md) | 空安全、函数与 Lambda、类与对象、委托、扩展、泛型、作用域函数等 |
| [02-Kotlin协程.md](notes/kotlin/02-Kotlin协程.md) | suspend 原理（CPS+状态机）、调度器、结构化并发、取消、Flow/Channel |

### Objective-C

| 文件 | 说明 |
|------|------|
| [01-OC基础语法.md](notes/objective-c/01-OC基础语法.md) | 类、对象、内存管理、消息、协议/委托、Category/Extension、Block、KVC/KVO、集合等 |
| [02-OC多线程.md](notes/objective-c/02-OC多线程.md) | 多线程基础、NSThread、GCD、NSOperation、线程安全、RunLoop 保活等 |

### Swift

| 文件 | 说明 |
|------|------|
| [01-Swift基础语法.md](notes/swift/01-Swift基础语法.md) | 类型系统、可选类型、集合、控制流、函数闭包、类与结构体、ARC、协议泛型、错误处理等 |
| [02-Swift多线程.md](notes/swift/02-Swift多线程.md) | GCD、锁、async/await、Task、结构化并发、Actor、Sendable、多读单写等 |

### Android

| 文件 | 说明 |
|------|------|
| [01-Android系统结构.md](notes/mobile/android/01-Android系统结构.md) | 六层架构全景：Linux 内核→HAL→运行时→Framework→应用 |
| [02-Android系统启动分析.md](notes/mobile/android/02-Android系统启动分析.md) | 从加电到 Launcher 的完整进程诞生链 |
| [03-init进程分析.md](notes/mobile/android/03-init进程分析.md) | init PID 1：FirstStage/SecondStage、rc 解析、属性服务 |
| [04-Binder系列一-Binder驱动核心概览.md](notes/mobile/android/04-Binder系列一-Binder驱动核心概览.md) | 一次拷贝原理、4 大方法、7 种数据结构、BC_/BR_ 协议 |
| [05-Binder系列二-ServiceManager分析.md](notes/mobile/android/05-Binder系列二-ServiceManager分析.md) | SM 启动三阶段、SET_CONTEXT_MGR、handle 0 获取 |
| [06-Binder系列三-服务注册与获取过程分析.md](notes/mobile/android/06-Binder系列三-服务注册与获取过程分析.md) | flat_binder_object 改写、注册/获取全链路源码 |
| [07-Binder系列四-Framework层分析.md](notes/mobile/android/07-Binder系列四-Framework层分析.md) | Java 层 JNI 注册、ServiceManager 封装、AIDL 调用链 |
| [08-Zygote进程分析.md](notes/mobile/android/08-Zygote进程分析.md) | Zygote：ART 孵化器、fork+COW、preload 机制 |
| [09-system_server进程分析.md](notes/mobile/android/09-system_server进程分析.md) | system_server：三批服务发布、AMS.systemReady、Looper 主循环 |
| [10-Launcher启动分析.md](notes/mobile/android/10-Launcher启动分析.md) | Launcher：HOME 应用、resolveActivity、fork、桌面加载 |
| [11-Activity启动过程分析（上）.md](notes/mobile/android/11-Activity启动过程分析（上）.md) | Activity 上：startActivity→ATMS→ActivityStarter→进程创建 |
| [12-Activity启动过程分析（下）.md](notes/mobile/android/12-Activity启动过程分析（下）.md) | Activity 下：attachApplication→ClientTransaction→生命周期回调 |
| [13-Broadcast基础和注册分析.md](notes/mobile/android/13-Broadcast基础和注册分析.md) | Broadcast：观察者模式、分类、动态注册源码 |
| [14-Broadcast发送和接收过程分析.md](notes/mobile/android/14-Broadcast发送和接收过程分析.md) | Broadcast：sendBroadcast→BroadcastQueue→onReceive 全链路 |

### 算法

| 分类 | 题目 | 实现 | 题解 |
| --- | --- | --- | --- |
| Hash | [#1 两数之和](https://leetcode.cn/problems/two-sum/) | [Leetcode_1.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/hash/Leetcode_1.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/hash/Leetcode-1-两数之和.md) |
| 双指针 | [#11 盛水容器](https://leetcode.cn/problems/container-with-most-water/) | [Leetcode_11.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/double_point/Leetcode_11.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/double_point/Leetcode-11-盛水容器.md) |
| 双指针 | [#141 环形链表](https://leetcode.cn/problems/linked-list-cycle/) | [Leetcode_141.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/double_point/Leetcode_141.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/double_point/Leetcode-141-环形链表.md) |
| 双指针 | [#344 反转字符串](https://leetcode.cn/problems/reverse-string/) | [Leetcode_344.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/double_point/Leetcode_344.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/double_point/Leetcode-344-反转字符串.md) |
| Stack | [#20 有效括号](https://leetcode.cn/problems/valid-parentheses/) | [Leetcode_20.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/stack/Leetcode_20.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/stack/Leetcode-20-有效括号.md) |
| 回溯 | [#46 全排列](https://leetcode.cn/problems/permutations/) | [Leetcode_46.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/backtrack/Leetcode_46.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/backtrack/Leetcode-46-全排列.md) |
| 排序/区间 | [#56 合并区间](https://leetcode.cn/problems/merge-intervals/) | [Leetcode_56.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/greedy/Leetcode_56.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/greedy/Leetcode-56-合并区间.md) |
| DP | [#62 不同路径](https://leetcode.cn/problems/unique-paths/) | [Leetcode_62.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/dp/Leetcode_62.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/dp/Leetcode-62-不同路径.md) |
| Tree | [#102 层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | [Leetcode_102.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/tree/Leetcode_102.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/tree/Leetcode-102-层序遍历.md) |
| Tree | [#104 最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | [Leetcode_104.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/tree/Leetcode_104.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/tree/Leetcode-104-最大深度.md) |
| 位运算 | [#137 只出现一次的数字 II](https://leetcode.cn/problems/single-number-ii/) | [Leetcode_137.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/bit_operator/Leetcode_137.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/bit_operator/Leetcode-137-只出现一次的数字%20II.md) |
| DFS/BFS | [#200 岛屿数量](https://leetcode.cn/problems/number-of-islands/) | [Leetcode_200.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/dfs_bfs/Leetcode_200.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/dfs_bfs/Leetcode-200-岛屿数量.md) |
| 堆 | [#215 第K大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) | [Leetcode_215.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/heap/Leetcode_215.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/heap/Leetcode-215-第K大元素.md) |
| Queue | [#225 用队列实现栈](https://leetcode.cn/problems/implement-stack-using-queues/) | [Leetcode_225.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/queue/Leetcode_225.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/queue/Leetcode-225-用队列实现栈.md) |
| 前缀和 | [#303 区域和检索](https://leetcode.cn/problems/range-sum-query-immutable/) | [Leetcode_303.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/prefix_sum/Leetcode_303.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/prefix_sum/Leetcode-303-区域和检索.md) |
| Greedy | [#455 分发饼干](https://leetcode.cn/problems/assign-cookies/) | [Leetcode_455.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/greedy/Leetcode_455.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/greedy/Leetcode-455-分发饼干.md) |
| 二分 | [#704 二分查找](https://leetcode.cn/problems/binary-search/) | [Leetcode_704.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/binary_search/Leetcode_704.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/binary_search/Leetcode-704-二分查找.md) |
| 单调栈 | [#739 每日温度](https://leetcode.cn/problems/daily-temperatures/) | [Leetcode_739.java](https://github.com/MrLsz/GLDailyCode/blob/main/code/src/main/java/gldailycode/stack/Leetcode_739.java) | [题解](https://github.com/MrLsz/GLDailyCode/blob/main/solutions/stack/Leetcode-739-每日温度.md) |

---

*Stay hungry, stay foolish.*
