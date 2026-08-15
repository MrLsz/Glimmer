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
| [Android系统结构.md](notes/mobile/android/Android系统结构.md) | 六层架构全景：Linux 内核→HAL→运行时→Framework→应用 |
| [Android系统启动分析.md](notes/mobile/android/Android系统启动分析.md) | 从加电到 Launcher 的完整进程诞生链 |
| [init进程启动分析.md](notes/mobile/android/init进程启动分析.md) | init PID 1：FirstStage/SecondStage、rc 解析、属性服务 |
| [zygote进程启动分析.md](notes/mobile/android/zygote进程启动分析.md) | Zygote：ART 孵化器、fork+COW、preload 机制 |
| [Binder驱动核心概览.md](notes/mobile/android/Binder驱动核心概览.md) | 一次拷贝原理、4 大方法、7 种数据结构、BC_/BR_ 协议 |
| [Binder ServiceManager的启动与获取分析.md](notes/mobile/android/Binder%20ServiceManager的启动与获取分析.md) | SM 启动三阶段、SET_CONTEXT_MGR、handle 0 获取 |
| [Binder 服务注册与获取过程分析.md](notes/mobile/android/Binder%20服务注册与获取过程分析.md) | flat_binder_object 改写、注册/获取全链路源码 |
| [Binder Framework层分析.md](notes/mobile/android/Binder%20Framework层分析.md) | Java 层 JNI 注册、ServiceManager 封装、AIDL 调用链 |

### 算法

| 文件 | 类别 | 说明 |
|------|------|------|
| [leetcode-1-two-sum.md](notes/algorithm/hash/leetcode-1-two-sum.md) | Hash | #1 两数之和 |
| [leetcode-11-container-with-most-water.md](notes/algorithm/double-point/leetcode-11-container-with-most-water.md) | 双指针 | #11 盛水容器 |
| [leetcode-20-valid-parentheses.md](notes/algorithm/stack/leetcode-20-valid-parentheses.md) | Stack | #20 有效括号 |
| [leetcode-46-permutations.md](notes/algorithm/backtracking/leetcode-46-permutations.md) | 回溯 | #46 全排列 |
| [leetcode-62-unique-paths.md](notes/algorithm/dp/leetcode-62-unique-paths.md) | DP | #62 不同路径 |
| [leetcode-102-binary-tree-level-order-traversal.md](notes/algorithm/tree/leetcode-102-binary-tree-level-order-traversal.md) | Tree | #102 层序遍历 |
| [leetcode-104-maximum-depth-of-binary-tree.md](notes/algorithm/tree/leetcode-104-maximum-depth-of-binary-tree.md) | Tree | #104 最大深度 |
| [leetcode-200-number-of-islands.md](notes/algorithm/dfs_bfs/leetcode-200-number-of-islands.md) | DFS/BFS | #200 岛屿数量 |
| [leetcode-225-implement-stack-using-queues.md](notes/algorithm/queue/leetcode-225-implement-stack-using-queues.md) | Queue | #225 用队列实现栈 |
| [leetcode-455-assign-cookies.md](notes/algorithm/greedy/leetcode-455-assign-cookies.md) | Greedy | #455 分发饼干 |
| [leetcode-704-binary-search.md](notes/algorithm/binary-search/leetcode-704-binary-search.md) | 二分 | #704 二分查找 |

---

*Stay hungry, stay foolish.*
