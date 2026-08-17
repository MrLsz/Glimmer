# Glimmer

> 个人 IT 学习笔记与经验积累仓库。点滴积累，聚微光成星河。

## 目录结构

```
Glimmer/
├── notes/                  # 学习笔记
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

| 文件 | 类别 | 说明 |
|------|------|------|
| [leetcode-1-two-sum.md](notes/algorithm/hash/leetcode-1-two-sum.md) | Hash | #1 两数之和 |
| [leetcode-11-container-with-most-water.md](notes/algorithm/double-point/leetcode-11-container-with-most-water.md) | 双指针 | #11 盛水容器 |
| [leetcode-20-valid-parentheses.md](notes/algorithm/stack/leetcode-20-valid-parentheses.md) | Stack | #20 有效括号 |
| [leetcode-46-permutations.md](notes/algorithm/backtracking/leetcode-46-permutations.md) | 回溯 | #46 全排列 |
| [leetcode-56-merge-intervals.md](notes/algorithm/sort/leetcode-56-merge-intervals.md) | 排序/区间 | #56 合并区间 |
| [leetcode-62-unique-paths.md](notes/algorithm/dp/leetcode-62-unique-paths.md) | DP | #62 不同路径 |
| [leetcode-102-binary-tree-level-order-traversal.md](notes/algorithm/tree/leetcode-102-binary-tree-level-order-traversal.md) | Tree | #102 层序遍历 |
| [leetcode-104-maximum-depth-of-binary-tree.md](notes/algorithm/tree/leetcode-104-maximum-depth-of-binary-tree.md) | Tree | #104 最大深度 |
| [leetcode-141-linked-list-cycle.md](notes/algorithm/double-point/leetcode-141-linked-list-cycle.md) | 双指针 | #141 环形链表 |
| [leetcode-200-number-of-islands.md](notes/algorithm/dfs_bfs/leetcode-200-number-of-islands.md) | DFS/BFS | #200 岛屿数量 |
| [leetcode-215-kth-largest-element.md](notes/algorithm/sort/leetcode-215-kth-largest-element.md) | 堆 | #215 第K大元素 |
| [leetcode-225-implement-stack-using-queues.md](notes/algorithm/queue/leetcode-225-implement-stack-using-queues.md) | Queue | #225 用队列实现栈 |
| [leetcode-303-range-sum-query-immutable.md](notes/algorithm/sort/leetcode-303-range-sum-query-immutable.md) | 前缀和 | #303 区域和检索 |
| [leetcode-344-reverse-string.md](notes/algorithm/double-point/leetcode-344-reverse-string.md) | 双指针 | #344 反转字符串 |
| [leetcode-455-assign-cookies.md](notes/algorithm/greedy/leetcode-455-assign-cookies.md) | Greedy | #455 分发饼干 |
| [leetcode-704-binary-search.md](notes/algorithm/binary-search/leetcode-704-binary-search.md) | 二分 | #704 二分查找 |
| [leetcode-739-daily-temperatures.md](notes/algorithm/stack/leetcode-739-daily-temperatures.md) | 单调栈 | #739 每日温度 |

---

*Stay hungry, stay foolish.*
