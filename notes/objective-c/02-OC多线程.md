# 02. Objective-C 多线程

> 多线程是 iOS / macOS 开发绕不开的核心能力：从最底层的 `NSThread`，到抽象度更高的 GCD 与 `NSOperationQueue`，再到保证数据一致性的锁与「多读单写」方案，构成了完整的并发编程技术栈。本文按「为什么 → 是什么 → 怎么用 → 踩什么坑」的脉络，覆盖原理、API、对比与易错点。

## 目录

- [一、多线程基础](#一多线程基础)
- [二、NSThread](#二nsthread)
- [三、GCD（Grand Central Dispatch）](#三gcdgrand-central-dispatch)
- [四、NSOperation / NSOperationQueue](#四nsoperation--nsoperationqueue)
- [五、锁与线程安全](#五锁与线程安全)
- [六、多读单写](#六多读单写)
- [七、RunLoop 与线程保活](#七runloop-与线程保活)
- [八、常见问题与最佳实践](#八常见问题与最佳实践)
- [附：高频速记](#附高频速记)

---

## 一、多线程基础

### 1. 进程与线程

| 概念 | 说明 | 关键点 |
|------|------|--------|
| 进程（Process） | 资源分配的基本单位，有独立地址空间 | 进程间内存隔离，通信需 IPC |
| 线程（Thread） | CPU 调度的基本单位，共享进程地址空间 | 同进程线程共享堆、全局变量，**栈私有** |

iOS 中每个 App 是一个进程，主线程（Main Thread）负责 UI，也叫 UI 线程。**所有 UIKit 操作必须在主线程执行**，这是 iOS 开发的第一条铁律。

### 2. 并发与并行

这两个词常被混用，本质不同：

| 概念 | 含义 | 类比 |
|------|------|------|
| 并发（Concurrency） | 逻辑上「同时」处理多件事，宏观并行、微观可能串行 | 一个人同时接多个项目，来回切换 |
| 并行（Parallelism） | 物理上真正同时执行，需要多核 CPU | 多个人各自做各自的事 |

> 单核 CPU 只有并发没有并行；多核 CPU 才能真并行。GCD 让你只关心「并发」，至于是否「并行」由系统按核数调度。

### 3. 同步 / 异步、串行 / 并发

这是 GCD 的两个正交维度，必须彻底分清：

- **同步（sync）**：调用方必须等任务执行完才能继续；阻塞当前线程。
- **异步（async）**：任务提交后立即返回，调用方不等待；不阻塞当前线程。
- **串行（Serial）**：同一时刻只执行一个任务，前一个完成才执行下一个。
- **并发（Concurrent）**：可以同时执行多个任务。

两两组合出四种行为，见下文「三、GCD」的组合矩阵。

### 4. 线程开销与上下文切换

创建线程不是免费的：

- 每开一个线程都要占用内核栈空间（iOS 主线程约 1MB，子线程默认 512KB）；
- **上下文切换（Context Switch）**：CPU 在多个线程间切换时，要保存/恢复寄存器、栈指针等现场，切换本身有成本；
- 线程过多会导致「切换开销 > 实际计算」，性能反而下降。

这也是为什么不推荐大量使用 `NSThread` 手动管理线程，而应使用 GCD 的线程池复用机制。

### 5. 多线程带来的三大问题

| 问题 | 表现 | 解决思路 |
|------|------|---------|
| 竞态条件（Race Condition） | 多线程同时读写共享变量，结果不确定 | 加锁、原子操作、串行队列 |
| 死锁（Deadlock） | 线程互相等待对方释放资源，永久阻塞 | 按序加锁、避免嵌套 sync |
| 资源消耗 / 线程爆炸 | 线程数过多拖垮性能 | 用 GCD 队列、限制并发数 |

---

## 二、NSThread

`NSThread` 是 OC 对 POSIX 线程（`pthread`）的面向对象封装，是**最底层、最原始**的多线程方案。一般只有需要精细控制线程生命周期时才用，日常开发优先 GCD / NSOperation。

### 1. 三种创建方式

```objc
// 方式一：alloc / init + start（可拿到 thread 对象，最常用）
NSThread *thread = [[NSThread alloc] initWithTarget:self
                                           selector:@selector(doWork:)
                                             object:nil];
thread.name = @"com.demo.worker";   // 便于调试
[thread start];

// 方式二：类方法直接分离出一个线程（拿不到对象）
[NSThread detachNewThreadSelector:@selector(doWork:)
                         toTarget:self
                       withObject:nil];

// 方式三：NSObject 分类方法（隐式创建后台线程）
[self performSelectorInBackground:@selector(doWork:) withObject:nil];
```

### 2. 生命周期与状态

线程有创建、就绪、运行、阻塞、死亡等状态，`NSThread` 提供几个常用属性：

| 属性 / 方法 | 说明 |
|------------|------|
| `thread.isExecuting` | 是否正在执行 |
| `thread.isFinished` | 是否已结束 |
| `thread.isCancelled` | 是否被标记取消（**只是标记，不会真正停止线程**） |
| `+[NSThread mainThread]` | 主线程对象 |
| `+[NSThread currentThread]` | 当前线程对象 |
| `+[NSThread isMainThread]` | 当前是否主线程 |
| `+[NSThread sleepForTimeInterval:]` | 让当前线程休眠 |

> `cancel` 只置标志位，线程代码必须自己检查 `isCancelled` 来配合退出，这是与 `NSOperation.cancel` 一样的「协作式取消」模型。

### 3. 线程间通信

```objc
// 子线程做完事，回到主线程更新 UI
- (void)doWork:(id)sender {
    @autoreleasepool {                    // 子线程必须手动管理自动释放池
        // ... 耗时操作
        [self performSelectorOnMainThread:@selector(updateUI:)
                               withObject:result
                            waitUntilDone:NO];   // NO = 异步，不阻塞子线程
    }
}

// 也可以往任意线程发消息
[self performSelector:@selector(handle) onThread:otherThread withObject:nil waitUntilDone:NO];
```

### 4. NSThread 的局限

- 需要手动管理线程生命周期与 `@autoreleasepool`；
- 无法控制并发数量，容易线程爆炸；
- 无任务依赖、取消、优先级队列等高级能力。

结论：**NSThread 只适合需要显式持有线程、或做线程保活（配合 RunLoop）的场景**，其余用 GCD / NSOperation。

---

## 三、GCD（Grand Central Dispatch）

GCD 是 Apple 官方力推的并发方案，基于 C 语言、以 **队列 + 任务** 为模型，底层用**线程池**自动复用线程，屏蔽了线程创建/销毁的开销。

### 1. 核心概念：队列与任务

- **任务**：一段要执行的代码，即一个 `block`。
- **队列（Dispatch Queue）**：遵循 FIFO 规则管理任务的数据结构。

GCD 把「要做什么」（任务）与「怎么调度」（队列 + 同步/异步）解耦，你只需决定两件事：**任务放哪个队列、同步还是异步执行**。

### 2. 四种队列

| 队列 | 获取方式 | 性质 | 用途 |
|------|---------|------|------|
| 主队列 | `dispatch_get_main_queue()` | **串行**，与主线程绑定 | UI 更新、需要在主线程执行的任务 |
| 全局并发队列 | `dispatch_get_global_queue(优先级, 0)` | **并发**，系统提供 | 大多数后台任务 |
| 自定义串行队列 | `dispatch_queue_create("id", DISPATCH_QUEUE_SERIAL)` | 串行 | 顺序执行、做「锁」、隔离数据 |
| 自定义并发队列 | `dispatch_queue_create("id", DISPATCH_QUEUE_CONCURRENT)` | 并发 | 配合 barrier 实现多读单写 |

> `dispatch_queue_create` 的队列标签（第一个参数）建议用**反向域名**命名，便于崩溃日志 / Instruments 里定位。iOS 6+ 用 ARC 管理，无需 `dispatch_release`。

### 3. 同步 sync 与异步 async

```objc
// 同步：阻塞当前线程，等 block 执行完才继续
dispatch_sync(queue, ^{
    NSLog(@"sync 任务");
});
NSLog(@"这行一定在 sync 任务之后执行");

// 异步：立即返回，block 在队列调度后执行
dispatch_async(queue, ^{
    NSLog(@"async 任务");
});
NSLog(@"这行通常先执行");
```

### 4. 队列 × 同步/异步 组合矩阵（重点）

这是 GCD 面试与实战的核心，必须滚瓜烂熟：

| 队列类型 | `dispatch_sync`（同步） | `dispatch_async`（异步） |
|---------|------------------------|------------------------|
| **串行队列** | 阻塞当前线程，任务在**当前线程**执行；逐个串行 | 不阻塞，任务在**新线程**逐个串行执行 |
| **并发队列** | 阻塞当前线程，任务在**当前线程**执行（此时退化为串行，无并发意义） | 不阻塞，任务在**多个线程**并发执行 |
| **主队列** | 若在**主线程**调用 → **死锁**；若在子线程调用 → 阻塞子线程、任务回到主线程执行 | 不阻塞，任务排到主线程队列末尾，等主线程空闲执行 |

记忆要点：

1. **sync 不开启新线程**：同步任务直接在当前线程执行（并发队列下 sync 也因此退化为串行）。
2. **async 是否开新线程取决于队列**：串行队列 async 最多开一个子线程；并发队列 async 会开多个子线程；主队列 async 不开新线程（回到主线程）。
3. **「死锁」只发生在 sync 到当前线程正在执行的串行队列**（见下文）。

### 5. dispatch_sync 与死锁（必考）

`dispatch_sync` 的本质是「在队列 A 上等待队列 B 的任务执行完成」。当 A 与 B 是**同一个串行队列**（含主队列）时，形成「自己等自己」，必然死锁。

**死锁场景一：主线程 sync 主队列**

```objc
- (void)viewDidLoad {
    [super viewDidLoad];
    // 主线程执行到这里，主队列正在被主线程占用
    dispatch_sync(dispatch_get_main_queue(), ^{
        // sync 要求主线程「停下来等 block 执行完」
        // 但 block 要排到主队列，必须等主线程「空出来」才能执行
        // 互相等待 → 死锁
        NSLog(@"永远不会执行");
    });
}
```

**死锁场景二：串行队列内 sync 自己**

```objc
dispatch_queue_t q = dispatch_queue_create("com.demo.serial", DISPATCH_QUEUE_SERIAL);
dispatch_async(q, ^{
    // 队列 q 此刻正在串行执行本 block
    dispatch_sync(q, ^{
        // 又往 q 提交一个同步任务，要求等它执行完
        // 但 q 要等当前 block 执行完才会轮到新任务 → 死锁
        NSLog(@"永远不会执行");
    });
});
```

**不会死锁的情况**：子线程 sync 主队列、sync 到「非当前」的队列、sync 到并发队列，都不会死锁。

```objc
// 子线程 sync 主队列：安全（子线程阻塞等待，主线程能执行 block）
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    dispatch_sync(dispatch_get_main_queue(), ^{
        NSLog(@"在主线程执行，安全");
    });
});
```

> 死锁的本质是「**串行队列上的相互等待**」。避免口诀：**不要在同一个串行队列里 sync 它自己；主线程别 sync 主队列**。

### 6. 常用 API

```objc
// dispatch_once：保证 block 只执行一次，线程安全（单例经典用法）
static dispatch_once_t onceToken;
dispatch_once(&onceToken, ^{
    // 只执行一次
});

// dispatch_after：延迟执行（不是精确的定时器，是「延迟提交到队列」）
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)),
               dispatch_get_main_queue(), ^{
    NSLog(@"2 秒后在主线程执行");
});

// dispatch_apply：并发迭代（类似 for 循环，但并发执行，顺序不保证）
dispatch_apply(10, dispatch_get_global_queue(0, 0), ^(size_t idx) {
    NSLog(@"处理第 %zu 个", idx);
});
// 注意：dispatch_apply 是同步的，会等所有迭代完成才返回
```

> `dispatch_after` 的 2 秒不是「精确 2 秒后执行」，而是「2 秒后把任务提交到队列」，实际执行时间取决于队列繁忙程度。

### 7. dispatch_group：任务编组

用于「多个异步任务全部完成后」再执行某件事，解决「并发任务汇总」问题。

```objc
dispatch_group_t group = dispatch_group_create();
dispatch_queue_t q = dispatch_get_global_queue(0, 0);

// 方式一：dispatch_group_async（自动 enter/leave）
dispatch_group_async(group, q, ^{ [self task1]; });
dispatch_group_async(group, q, ^{ [self task2]; });

// 方式二：enter / leave（手动配对，适合任务里有异步回调的场景）
dispatch_group_enter(group);
[self asyncRequestWithCompletion:^{
    dispatch_group_leave(group);
}];

// 全部完成后通知（可指定回到主线程）
dispatch_group_notify(group, dispatch_get_main_queue(), ^{
    NSLog(@"所有任务完成，刷新 UI");
});

// 或同步等待（阻塞当前线程，慎用）
// dispatch_group_wait(group, DISPATCH_TIME_FOREVER);
```

**易错点**：`enter` 与 `leave` 必须**严格配对**。`leave` 次数多于 `enter` 会导致崩溃（`Unbalanced call to dispatch_group_leave`）；少了则 `notify` 永不触发。

### 8. dispatch_barrier：栅栏（多读单写基石）

`dispatch_barrier_async` 提交到**并发队列**时，会等待「已提交的任务」全部执行完，再**独占**执行栅栏任务，执行完才继续后续任务：

```objc
dispatch_queue_t q = dispatch_queue_create("com.demo.concurrent", DISPATCH_QUEUE_CONCURRENT);

dispatch_async(q, ^{ /* 读 1 */ });
dispatch_async(q, ^{ /* 读 2 */ });
dispatch_barrier_async(q, ^{
    // 栅栏：等读 1、读 2 都执行完，独占执行写操作
    // 写操作期间，不会有其他任务并发
    NSLog(@"写操作");
});
dispatch_async(q, ^{ /* 读 3，等写操作完成才执行 */ });
```

**易错点**：

- `dispatch_barrier_*` **必须用在自定义并发队列**上；用在串行队列上退化为普通串行任务，用在全局并发队列上**不生效**（因为全局队列可能被系统内部共用，不能保证独占）；
- `dispatch_barrier_sync` 会阻塞当前线程；`dispatch_barrier_async` 不阻塞，优先用 async。

### 9. dispatch_semaphore：信号量

信号量用于**控制并发数量**、**实现线程同步**、**把异步变同步**。

```objc
// 创建信号量，初始值 = 最大并发数
dispatch_semaphore_t sem = dispatch_semaphore_create(3);

for (int i = 0; i < 10; i++) {
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        dispatch_semaphore_wait(sem, DISPATCH_TIME_FOREVER); // 信号量 -1，为 0 则等待
        // 最多 3 个任务同时进入这里
        [self doTask:i];
        dispatch_semaphore_signal(sem);                     // 信号量 +1，唤醒等待者
    });
}
```

```objc
// 信号量把异步操作变成同步等待（常用于依赖时序）
dispatch_semaphore_t sem = dispatch_semaphore_create(0);
[self asyncRequestWithCompletion:^{
    dispatch_semaphore_signal(sem);
}];
dispatch_semaphore_wait(sem, DISPATCH_TIME_FOREVER); // 阻塞直到回调完成
```

> `dispatch_semaphore_wait` 会阻塞当前线程，若在主线程调用且信号量始终不被 signal，会卡死 UI。

### 10. 队列底层：线程池与 target queue

GCD 的并发队列底层共享一个**线程池**，系统按任务数量与 CPU 核数动态增减线程，所以「并发队列 + async」能避免线程爆炸。所有队列内部通过 `target queue` 串成树状结构，最终汇入根队列（如 `com.apple.root.default-qos`），这是理解 QoS 优先级如何生效的关键。

---

## 四、NSOperation / NSOperationQueue

`NSOperation` 是**面向对象**的并发抽象，底层封装了 GCD，但额外提供 GCD 没有的高级能力：**依赖、取消、优先级、最大并发数、KVO 状态监听**。

### 1. 与 GCD 对比

| 维度 | GCD | NSOperation |
|------|-----|-------------|
| 抽象层级 | C 语言 API，轻量 | OC 对象，重量 |
| 依赖关系 | 无（需手动用 group/semaphore 模拟） | `addDependency:` 原生支持 |
| 取消 | 无（block 无法取消） | `cancel`（协作式） |
| 最大并发数 | 无（信号量模拟） | `maxConcurrentOperationCount` 直接设置 |
| 优先级 | 队列 QoS | `queuePriority` + `qualityOfService` |
| 状态监听 | 无 | KVO 监听 `isExecuting/isFinished/isCancelled` |

**结论**：简单一次性任务用 GCD；需要**依赖、取消、控制并发数、监控状态**的复杂任务用 NSOperation。

### 2. NSOperation 的三种子类

```objc
// ① NSInvocationOperation：调用一个方法（已不推荐，功能弱）
NSInvocationOperation *inv = [[NSInvocationOperation alloc]
                              initWithTarget:self selector:@selector(doWork) object:nil];

// ② NSBlockOperation：执行 block，可用 addExecutionBlock 追加任务
NSBlockOperation *op = [NSBlockOperation blockOperationWithBlock:^{
    NSLog(@"主 block");
}];
[op addExecutionBlock:^{ NSLog(@"追加 block 1"); }];
// 注意：NSBlockOperation 的多个 block 会「并发」执行（非串行）

// ③ 自定义子类：重写 main 或 start（见下）
```

### 3. 自定义 NSOperation

```objc
@interface MyOperation : NSOperation
@end

@implementation MyOperation
- (void)main {
    // 只适合「同步任务」：重写 main，自动管理 isExecuting/isFinished
    // 必须主动检查取消标志
    if (self.isCancelled) return;
    // ... 执行任务
    if (self.isCancelled) return;   // 任务较长时，中途多次检查
}
@end
```

若要封装「异步任务」（如网络请求），需重写 `start` 并手动维护 `isExecuting / isFinished / isCancelled` 的 KVO，复杂度较高，一般用 `NSBlockOperation` + 信号量，或直接 GCD 更省事。

### 4. NSOperationQueue 关键属性

```objc
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
queue.maxConcurrentOperationCount = 3;   // 最大并发数；=1 时退化为串行队列
queue.qualityOfService = NSQualityOfServiceUserInitiated; // QoS

[queue addOperation:op];                          // 加入即开始调度
[queue addOperationWithBlock:^{ /* 快速任务 */ }];
[queue addOperations:@[op1, op2] waitUntilFinished:NO];
```

`maxConcurrentOperationCount` 设 1 即可当串行队列用；设大值可并发。注意它限制的是「同时执行的操作数」，不是线程数。

### 5. 依赖（Dependency）

```objc
NSOperation *op1 = [NSBlockOperation blockOperationWithBlock:^{ NSLog(@"1"); }];
NSOperation *op2 = [NSBlockOperation blockOperationWithBlock:^{ NSLog(@"2"); }];
NSOperation *op3 = [NSBlockOperation blockOperationWithBlock:^{ NSLog(@"3"); }];

[op3 addDependency:op1];   // op3 依赖 op1：op1 完成才执行 op3
[op3 addDependency:op2];

[queue addOperations:@[op1, op2, op3] waitUntilFinished:NO];
// op1、op2 并发执行，都完成后 op3 才执行
```

**易错点**：`addDependency:` 是单向的，**小心循环依赖**（A 依赖 B、B 依赖 A → 两者永远不执行）。

### 6. 取消（Cancel）

```objc
[op cancel];                    // 标记取消，不会强制停止
[queue cancelAllOperations];    // 取消队列里所有操作
```

取消是**协作式**的：正在执行的操作不会被打断，必须自己检查 `isCancelled` 来决定是否提前退出；尚未开始的操作被取消后，队列会直接跳过不执行。

### 7. KVO 监听状态

```objc
[op addObserver:self forKeyPath:@"isFinished"
         options:NSKeyValueObservingOptionNew context:nil];

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object
                        change:(NSDictionary *)change context:(void *)context {
    if ([keyPath isEqualToString:@"isFinished"] && [(NSOperation *)object isFinished]) {
        // 操作完成
    }
}
```

> `NSOperation` 的状态属性（`isReady/isExecuting/isFinished/isCancelled`）都支持 KVO，这是它能做「完成回调」「依赖驱动」的底层机制。

---

## 五、锁与线程安全

### 1. 为什么需要锁

多线程同时读写共享资源（如 `NSMutableArray`、对象属性）会产生**竞态条件**，导致数据错乱甚至崩溃。锁的作用是**把临界区串行化**，保证同一时刻只有一个线程访问共享资源。

### 2. 各类锁对比总览

| 锁 | 类型 | 是否递归 | 特点 |
|----|------|---------|------|
| `@synchronized` | 互斥锁 | 是 | 语法简洁，自动加/解锁，性能较差 |
| `NSLock` | 互斥锁 | 否 | 简单易用；重复 lock 会死锁 |
| `NSRecursiveLock` | 递归锁 | 是 | 允许同一线程重复加锁 |
| `NSCondition` | 条件锁 | 是 | 生产者-消费者模型 |
| `NSConditionLock` | 条件锁 | 否 | 带条件值（如按序执行） |
| `pthread_mutex` | 互斥锁 | 可选 | 底层 C 锁，性能好 |
| `pthread_rwlock` | 读写锁 | 否 | 读可并发、写独占，多读单写首选 |
| `os_unfair_lock` | 互斥锁 | 否 | 取代 OSSpinLock，性能优秀，不可递归 |
| `dispatch_semaphore` | 信号量 | 否 | 可当锁用，性能好 |

### 3. @synchronized

```objc
- (void)addObject:(id)obj {
    @synchronized (self) {
        [self.array addObject:obj];
    }
}
```

- 加锁对象可以是任意对象，通常用 `self` 或专门的数据对象；
- 底层是一个「对象 → 递归锁」的哈希表，同一对象重入不会死锁；
- 语法糖，自动 `lock/unlock`，异常时也能正确解锁；
- **性能最差**，适合低频、简单场景。

### 4. NSLock 与 NSRecursiveLock

```objc
NSLock *lock = [[NSLock alloc] init];
[lock lock];
// 临界区
[lock unlock];
```

```objc
NSRecursiveLock *lock = [[NSRecursiveLock alloc] init];

- (void)methodA {
    [lock lock];
    [self methodB];   // 递归锁：同一线程可重复加锁
    [lock unlock];
}
- (void)methodB {
    [lock lock];
    // ...
    [lock unlock];
}
```

**易错点**：`NSLock` **不可递归**——同一线程对同一个 `NSLock` 连续 `lock` 两次会**死锁**。有递归调用场景必须用 `NSRecursiveLock` 或 `@synchronized`。

### 5. NSCondition 与 NSConditionLock

`NSCondition` 适合**生产者-消费者**：一个线程生产数据，另一个线程等待数据。

```objc
NSCondition *cond = [[NSCondition alloc] init];
NSMutableArray *products = [NSMutableArray array];

// 生产者
- (void)produce {
    [cond lock];
    [products addObject:@1];
    [cond signal];       // 唤醒一个等待线程
    [cond unlock];
}

// 消费者
- (void)consume {
    [cond lock];
    while (products.count == 0) {
        [cond wait];     // 等待条件满足（会释放锁，被唤醒后重新加锁）
    }
    [products removeLastObject];
    [cond unlock];
}
```

**易错点**：`wait` 后要用 `while` 判断条件而不是 `if`，因为线程被唤醒时条件可能已被其他线程改变（虚假唤醒）。

`NSConditionLock` 带一个整数条件，适合**按序执行**：

```objc
NSConditionLock *lock = [[NSConditionLock alloc] initWithCondition:0];

// 线程 A：等条件变为 1
[lock lockWhenCondition:1];
// ... 执行
[lock unlockWithCondition:2];

// 主线程：满足条件 1
[lock lock];
[lock unlockWithCondition:1];   // 释放并让条件 = 1，唤醒 A
```

### 6. pthread_mutex 与 pthread_rwlock

C 层锁，性能好、可控性强，多读单写常用 `pthread_rwlock`：

```objc
#import <pthread.h>

// 互斥锁
pthread_mutex_t mutex;
pthread_mutex_init(&mutex, NULL);
pthread_mutex_lock(&mutex);
// 临界区
pthread_mutex_unlock(&mutex);
pthread_mutex_destroy(&mutex);

// 读写锁
pthread_rwlock_t rwlock;
pthread_rwlock_init(&rwlock, NULL);
pthread_rwlock_rdlock(&rwlock);    // 读锁：多个线程可同时持有
// 读操作
pthread_rwlock_unlock(&rwlock);
pthread_rwlock_wrlock(&rwlock);    // 写锁：独占，等所有读锁释放
// 写操作
pthread_rwlock_unlock(&rwlock);
pthread_rwlock_destroy(&rwlock);
```

### 7. os_unfair_lock（自旋锁的继任者）

`OSSpinLock` 是经典自旋锁（忙等，不睡眠），但因**优先级反转**问题已被废弃，iOS 10 起用 `os_unfair_lock` 替代：

```objc
#import <os/lock.h>

os_unfair_lock lock = OS_UNFAIR_LOCK_INIT;
os_unfair_lock_lock(&lock);
// 临界区
os_unfair_lock_unlock(&lock);
```

- 性能接近 OSSpinLock，但等待时会睡眠而非忙等，避免优先级反转；
- **不可递归**，重复 lock 会死锁；
- 适合极短临界区、高频加解锁。

### 8. dispatch_semaphore 当锁用

信号量初始值为 1 时，就是一个高效的互斥锁：

```objc
dispatch_semaphore_t sem = dispatch_semaphore_create(1);
dispatch_semaphore_wait(sem, DISPATCH_TIME_FOREVER);
// 临界区
dispatch_semaphore_signal(sem);
```

### 9. atomic 与 nonatomic（属性原子性）

| 修饰符 | 行为 | 代价 |
|--------|------|------|
| `atomic` | 属性的 getter/setter 内部加锁，保证单次读写原子性 | 有性能开销，iOS 默认 atomic |
| `nonatomic` | 不加锁，读写最快 | iOS 开发**通常用 nonatomic** |

**关键误区**：`atomic` 只保证「单次 get/set 的原子性」，**不能保证线程安全**。比如「先读再改」这种复合操作（`self.count++`），`atomic` 依然会竞态。真正的线程安全要靠上文的各种锁 + 正确的临界区设计。

```objc
@property (atomic, assign) NSInteger count;   // 单次读写安全
// self.count = self.count + 1;  // 读+算+写 三步，仍不安全！
```

### 10. 死锁

**死锁产生的四个必要条件**：

1. **互斥**：资源一次只能被一个线程占用；
2. **占有并等待**：持有资源的同时等待其他资源；
3. **不可剥夺**：资源只能被持有者主动释放；
4. **循环等待**：线程间形成「A 等 B、B 等 C、C 等 A」的环。

只要破坏其一即可避免。常见死锁场景与对策：

| 场景 | 原因 | 对策 |
|------|------|------|
| 主线程 `dispatch_sync` 主队列 | 串行队列自己等自己 | 改用 `dispatch_async` |
| 串行队列内 `sync` 自己 | 同上 | 改用 async，或换队列 |
| 嵌套加锁顺序不一致 | 循环等待 | **全局统一加锁顺序** |
| `NSLock` 重复 lock | 不可重入 | 用 `NSRecursiveLock` |
| 依赖成环 | A 等 B、B 等 A | 检查依赖图，避免环 |

---

## 六、多读单写

**场景**：一个数据（如缓存字典）被频繁读、偶尔写。若读也加互斥锁，读读之间也会被串行化，浪费并发能力。多读单写（Multiple Readers, Single Writer）的目标是：**读可以并发，写必须独占，且写时不能有读**。

### 1. 方案一：dispatch_barrier（推荐，最简洁）

用自定义并发队列 + 栅栏：

```objc
@interface DataStore : NSObject
@property (nonatomic, strong) dispatch_queue_t queue;
@property (nonatomic, strong) NSMutableDictionary *dict;
@end

@implementation DataStore
- (instancetype)init {
    if (self = [super init]) {
        // 关键：必须是「自定义并发队列」
        _queue = dispatch_queue_create("com.demo.datastore", DISPATCH_QUEUE_CONCURRENT);
        _dict = [NSMutableDictionary dictionary];
    }
    return self;
}

// 读：并发执行，多个读可同时进行
- (id)objectForKey:(NSString *)key {
    __block id obj = nil;
    dispatch_sync(self.queue, ^{
        obj = [self.dict objectForKey:key];
    });
    return obj;
}

// 写：栅栏，独占执行
- (void)setObject:(id)obj forKey:(NSString *)key {
    dispatch_barrier_async(self.queue, ^{
        [self.dict setObject:obj forKey:key];
    });
}
@end
```

**要点**：

- 读用 `dispatch_sync` 是为了「读操作有返回值，需要阻塞等待拿到结果」；
- 写用 `dispatch_barrier_async`：写不需要立即返回，异步 + 栅栏独占；
- 队列必须是 `DISPATCH_QUEUE_CONCURRENT`，否则 barrier 失效。

### 2. 方案二：pthread_rwlock（性能更优）

```objc
pthread_rwlock_t rwlock;
pthread_rwlock_init(&rwlock, NULL);

- (id)objectForKey:(NSString *)key {
    pthread_rwlock_rdlock(&rwlock);
    id obj = [self.dict objectForKey:key];
    pthread_rwlock_unlock(&rwlock);
    return obj;
}

- (void)setObject:(id)obj forKey:(NSString *)key {
    pthread_rwlock_wrlock(&rwlock);
    [self.dict setObject:obj forKey:key];
    pthread_rwlock_unlock(&rwlock);
}
```

### 3. 方案对比

| 维度 | dispatch_barrier | pthread_rwlock |
|------|-----------------|----------------|
| 实现复杂度 | 低（纯 GCD API） | 低（C API） |
| 性能 | 略低于 rwlock | 更高 |
| 易用性 | 高，无配对风险 | 需手动 init/destroy |
| 适用 | 日常项目首选 | 对性能极致追求时 |

---

## 七、RunLoop 与线程保活

### 1. RunLoop 与线程的关系

- 每个线程**默认没有 RunLoop**，主线程除外（系统自动创建）；
- RunLoop 与线程一一对应，线程结束后 RunLoop 也随之销毁；
- 有了 RunLoop，线程才能「在有任务时处理、无任务时休眠」，而不是跑完就退出。

### 2. 常驻线程实现

```objc
@interface ResidentThread : NSObject
@property (nonatomic, strong) NSThread *thread;
@end

@implementation ResidentThread
- (instancetype)init {
    if (self = [super init]) {
        self.thread = [[NSThread alloc] initWithTarget:self
                                              selector:@selector(run)
                                                object:nil];
        [self.thread start];
    }
    return self;
}

- (void)run {
    @autoreleasepool {
        // 为线程创建并开启 RunLoop
        [[NSRunLoop currentRunLoop] addPort:[NSPort port]
                                    forMode:NSDefaultRunLoopMode]; // 关键：必须加 source/port，否则 RunLoop 立即退出
        [[NSRunLoop currentRunLoop] run];
    }
}

- (void)doSomething {
    [self performSelector:@selector(action) onThread:self.thread
               withObject:nil waitUntilDone:NO];
}
- (void)action {
    NSLog(@"在常驻线程执行");
}
@end
```

**易错点**：`[[NSRunLoop currentRunLoop] run]` 之前**必须给 RunLoop 添加至少一个输入源（port/timer/source）**，否则 RunLoop 没有「事做」会立刻退出，线程保活失败。

---

## 八、常见问题与最佳实践

### 1. 常见崩溃与坑

| 坑 | 说明 |
|----|------|
| 子线程操作 UIKit | 必须在主线程更新 UI，否则崩溃或渲染异常 |
| `dispatch_group` enter/leave 不配对 | leave 多于 enter 直接崩溃 |
| barrier 用在全局队列 | 不生效，写操作可能与其他读写并发 |
| `NSLock` 重复 lock | 死锁 |
| 循环依赖（NSOperation / 信号量） | 任务永不执行 / 永久等待 |
| 子线程忘写 `@autoreleasepool` | 内存暴涨（大量临时对象不释放） |
| 在 dealloc 里用锁/队列 | 对象即将释放，可能访问已释放内存 |

### 2. 最佳实践清单

1. **UI 永远主线程**：子线程完成工作后 `dispatch_async` 回主队列刷新；
2. **优先 GCD/NSOperation，少用 NSThread**；
3. **需要依赖/取消/并发控制 → NSOperation**，其余 → GCD；
4. **共享可变数据 → 加锁或串行队列隔离**，属性用 `nonatomic` + 显式锁，别迷信 `atomic`；
5. **多读单写 → dispatch_barrier + 自定义并发队列**；
6. **避免嵌套 sync**，尤其主线程 sync 主队列；
7. **锁的粒度尽量小**，临界区代码越短越好；
8. **统一加锁顺序**，避免死锁；
9. **子线程长任务记得 `@autoreleasepool`**；
10. **控制并发数量**：用 `dispatch_semaphore` 或 `maxConcurrentOperationCount`。

---

## 附：高频速记

- **并发 vs 并行**：并发是逻辑同时（切换），并行是物理同时（多核）。
- **sync 不开新线程**，阻塞当前线程；**async 是否开线程看队列**。
- **串行队列**：一个接一个；**并发队列**：可同时执行。
- **主线程 sync 主队列 → 死锁**；串行队列内 sync 自己 → 死锁。
- **barrier 只对自定义并发队列生效**，用于多读单写。
- **信号量**：`wait` 减一、`signal` 加一；初始值 = 最大并发数。
- **enter/leave 必须配对**。
- **atomic 只保证单次读写原子，不保证线程安全**。
- **NSLock 不可重入**；递归用 `NSRecursiveLock` 或 `@synchronized`。
- **NSOperation 强于 GCD 的三点**：依赖、取消、最大并发数。
- **NSOperation 取消是协作式**：要自己检查 `isCancelled`。
- **线程保活**：RunLoop + 至少一个 port/source。
