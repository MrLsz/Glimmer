# 02. Swift 多线程与并发

> Swift 的并发能力横跨两代：以 GCD 为代表的「C 时代工具」仍在大量使用，而 Swift 5.5 引入的 async/await、Actor、结构化并发则把「数据竞争检查」从运行时纪律升级成了编译器保证。本文按「为什么 → 是什么 → 怎么用 → 踩什么坑」的脉络，逐个技术点展开，覆盖原理、API、对比与易错点。

## 目录

- [一、多线程基础](#一多线程基础)
- [二、GCD（Grand Central Dispatch）](#二gcdgrand-central-dispatch)
- [三、锁与线程安全](#三锁与线程安全)
- [四、Swift 现代并发 async/await](#四swift-现代并发-asyncawait)
- [五、多读单写](#五多读单写)
- [六、常见问题与最佳实践](#六常见问题与最佳实践)
- [附：高频速记](#附高频速记)

---

## 一、多线程基础

### 1. 进程与线程

| 概念 | 说明 | 关键点 |
|------|------|--------|
| 进程（Process） | 资源分配的基本单位，有独立地址空间 | 进程间内存隔离，通信需 IPC |
| 线程（Thread） | CPU 调度的基本单位，共享进程地址空间 | 同进程线程共享堆、全局变量，**栈私有** |

iOS 中每个 App 是一个进程，主线程（Main Thread）负责 UI。**所有 UI 操作必须在主线程执行**，这是 iOS 开发的第一条铁律。

### 2. 并发与并行

这两个词常被混用，本质不同：

| 概念 | 含义 | 类比 |
|------|------|------|
| 并发（Concurrency） | 逻辑上「同时」处理多件事，宏观并行、微观可能串行 | 一个人同时接多个项目，来回切换 |
| 并行（Parallelism） | 物理上真正同时执行，需要多核 CPU | 多个人各自做各自的事 |

> 单核 CPU 只有并发没有并行；多核 CPU 才能真并行。GCD / async-await 让你只关心「并发」，是否「并行」由系统按核数调度。

### 3. 同步 / 异步、串行 / 并发

这是两个正交维度，必须彻底分清：

- **同步（sync）**：调用方必须等任务执行完才能继续；阻塞当前线程。
- **异步（async）**：任务提交后立即返回，调用方不等待；不阻塞当前线程。
- **串行（Serial）**：同一时刻只执行一个任务，前一个完成才执行下一个。
- **并发（Concurrent）**：可以同时执行多个任务。

两两组合出四种行为，见下文「二、GCD」的组合矩阵。

### 4. 线程开销与上下文切换

创建线程不是免费的：

- 每开一个线程都要占用内核栈空间（iOS 主线程约 1MB，子线程默认 512KB）；
- **上下文切换（Context Switch）**：CPU 在多个线程间切换时，要保存/恢复寄存器、栈指针等现场，切换本身有成本；
- 线程过多会导致「切换开销 > 实际计算」，性能反而下降。

这也是为什么不推荐手动管理线程，而应使用 GCD 的线程池复用机制。

### 5. 多线程带来的三大问题

| 问题 | 表现 | 解决思路 |
|------|------|---------|
| 竞态条件（Race Condition） | 多线程同时读写共享变量，结果不确定 | 加锁、Actor、串行队列 |
| 死锁（Deadlock） | 线程互相等待对方释放资源，永久阻塞 | 按序加锁、避免嵌套 sync |
| 资源消耗 / 线程爆炸 | 线程数过多拖垮性能 | 用 GCD 队列、限制并发数 |

---

## 二、GCD（Grand Central Dispatch）

GCD 是 Apple 的并发框架，基于 C 语言、以 **队列 + 任务** 为模型，底层用**线程池**自动复用线程，屏蔽了线程创建/销毁的开销。Swift 中通过 `DispatchQueue` 等 API 使用。

### 1. 核心概念：队列与任务

- **任务**：一段要执行的代码，即一个闭包。
- **队列（Dispatch Queue）**：遵循 FIFO 规则管理任务的数据结构。

GCD 把「要做什么」（任务）与「怎么调度」（队列 + 同步/异步）解耦，你只需决定两件事：**任务放哪个队列、同步还是异步执行**。

### 2. 四种队列

| 队列 | 获取方式 | 性质 | 用途 |
|------|---------|------|------|
| 主队列 | `DispatchQueue.main` | **串行**，与主线程绑定 | UI 更新 |
| 全局并发队列 | `DispatchQueue.global()` | **并发**，系统提供 | 大多数后台任务 |
| 自定义串行队列 | `DispatchQueue(label: "id")` | 串行 | 顺序执行、做「锁」、隔离数据 |
| 自定义并发队列 | `DispatchQueue(label: "id", attributes: .concurrent)` | 并发 | 配合 barrier 实现多读单写 |

> 队列标签（label）建议用**反向域名**命名，便于崩溃日志 / Instruments 里定位。Swift 中队列由 ARC 管理，无需手动 release。

### 3. 同步 sync 与异步 async

```swift
let queue = DispatchQueue(label: "com.demo.serial")

// 同步：阻塞当前线程，等闭包执行完才继续
queue.sync {
    print("sync 任务")
}
print("这行一定在 sync 任务之后执行")

// 异步：立即返回，闭包在队列调度后执行
queue.async {
    print("async 任务")
}
print("这行通常先执行")
```

### 4. 队列 × 同步/异步 组合矩阵（重点）

这是 GCD 的核心，必须滚瓜烂熟：

| 队列类型 | `sync`（同步） | `async`（异步） |
|---------|----------------|----------------|
| **串行队列** | 阻塞当前线程，任务在**当前线程**执行；逐个串行 | 不阻塞，任务在**新线程**逐个串行执行 |
| **并发队列** | 阻塞当前线程，任务在**当前线程**执行（退化为串行，无并发意义） | 不阻塞，任务在**多个线程**并发执行 |
| **主队列** | 主线程调用 → **死锁**；子线程调用 → 阻塞子线程、任务回主线程执行 | 不阻塞，任务排到主队列末尾，等主线程空闲执行 |

记忆要点：

1. **sync 不开启新线程**：同步任务直接在当前线程执行（并发队列下 sync 也因此退化为串行）。
2. **async 是否开新线程取决于队列**：串行队列 async 最多开一个子线程；并发队列 async 会开多个子线程；主队列 async 不开新线程。
3. **「死锁」只发生在 sync 到当前线程正在执行的串行队列**（见下文）。

### 5. dispatch_sync 与死锁（必考）

`sync` 的本质是「在队列 A 上**等待**队列 B 的任务执行完成」。当 A 与 B 是**同一个串行队列**（含主队列）时，形成「自己等自己」，必然死锁。

**死锁场景一：主线程 sync 主队列**

```swift
override func viewDidLoad() {
    super.viewDidLoad()
    // 主线程执行到这里，主队列正在被主线程占用
    DispatchQueue.main.sync {
        // sync 要求主线程「停下来等闭包执行完」
        // 但闭包要排到主队列，必须等主线程「空出来」才能执行
        // 互相等待 → 死锁
        print("永远不会执行")
    }
}
```

**死锁场景二：串行队列内 sync 自己**

```swift
let q = DispatchQueue(label: "com.demo.serial")
q.async {
    // 队列 q 此刻正在串行执行本闭包
    q.sync {
        // 又往 q 提交一个同步任务，要求等它执行完
        // 但 q 要等当前闭包执行完才会轮到新任务 → 死锁
        print("永远不会执行")
    }
}
```

**不会死锁的情况**：子线程 sync 主队列、sync 到「非当前」的队列、sync 到并发队列，都不会死锁。

```swift
// 子线程 sync 主队列：安全（子线程阻塞等待，主线程能执行闭包）
DispatchQueue.global().async {
    DispatchQueue.main.sync {
        print("在主线程执行，安全")
    }
}
```

> 死锁的本质是「**串行队列上的相互等待**」。避免口诀：**不要在同一个串行队列里 sync 它自己；主线程别 sync 主队列**。

### 6. dispatch_group：任务编组

用于「多个异步任务全部完成后」再执行某件事，解决「并发任务汇总」问题。

```swift
let group = DispatchGroup()
let q = DispatchQueue.global()

// 方式一：直接关联任务
q.async(group: group) { self.task1() }
q.async(group: group) { self.task2() }

// 方式二：enter / leave（手动配对，适合任务里有异步回调的场景）
group.enter()
asyncRequest { _ in
    group.leave()      // 回调里才 leave
}

// 全部完成后通知（可指定回主线程）
group.notify(queue: .main) {
    print("所有任务完成，刷新 UI")
}

// 或同步等待（阻塞当前线程，慎用）
// group.wait()
```

**易错点**：`enter` 与 `leave` 必须**严格配对**。`leave` 次数多于 `enter` 会导致崩溃（`Unbalanced call to dispatch_group_leave`）；少了则 `notify` 永不触发。

### 7. dispatch_barrier：栅栏（多读单写基石）

`barrier` 提交到**并发队列**时，会等待「已提交的任务」全部执行完，再**独占**执行栅栏任务，执行完才继续后续任务：

```swift
let q = DispatchQueue(label: "com.demo.concurrent", attributes: .concurrent)

q.async { /* 读 1 */ }
q.async { /* 读 2 */ }
q.async(flags: .barrier) {
    // 栅栏：等读 1、读 2 都执行完，独占执行写操作
    // 写操作期间，不会有其他任务并发
    print("写操作")
}
q.async { /* 读 3，等写操作完成才执行 */ }
```

**易错点**：

- `barrier` **必须用在自定义并发队列**上；用在串行队列上退化为普通串行任务，用在全局并发队列上**不生效**（全局队列可能被系统内部共用，不能保证独占）；
- 优先用 `async(flags: .barrier)`（不阻塞）；`sync(flags: .barrier)` 会阻塞当前线程。

### 8. dispatch_semaphore：信号量

信号量用于**控制并发数量**、**实现线程同步**、**把异步变同步**。

```swift
// 创建信号量，初始值 = 最大并发数
let sem = DispatchSemaphore(value: 3)

for i in 0..<10 {
    DispatchQueue.global().async {
        sem.wait()      // 信号量 -1，为 0 则等待
        // 最多 3 个任务同时进入这里
        self.doTask(i)
        sem.signal()    // 信号量 +1，唤醒等待者
    }
}
```

```swift
// 信号量把异步操作变成同步等待（常用于依赖时序）
let sem = DispatchSemaphore(value: 0)
asyncRequest { _ in
    sem.signal()
}
sem.wait()   // 阻塞直到回调完成
```

> `sem.wait()` 会阻塞当前线程，若在主线程调用且信号量始终不被 signal，会卡死 UI。

### 9. 队列底层：线程池与 target queue

GCD 的并发队列底层共享一个**线程池**，系统按任务数量与 CPU 核数动态增减线程，所以「并发队列 + async」能避免线程爆炸。所有队列内部通过 `target queue` 串成树状结构，最终汇入根队列（如 `com.apple.root.default-qos`），这是理解 QoS 优先级如何生效的关键。

---

## 三、锁与线程安全

### 1. 为什么需要锁

多线程同时读写共享资源会产生**竞态条件**，导致数据错乱甚至崩溃。锁的作用是**把临界区串行化**，保证同一时刻只有一个线程访问共享资源。

```swift
var count = 0   // 两个线程同时 count += 1，结果不确定
```

`count += 1` 看似一句，实则是「读 → 加 → 写」三步，线程可能在任意一步被打断。

### 2. 各类锁对比总览

| 锁 | 类型 | 是否递归 | 特点 |
|----|------|---------|------|
| `NSLock` | 互斥锁 | 否 | 简单易用；重复 lock 会死锁 |
| `NSRecursiveLock` | 递归锁 | 是 | 允许同一线程重复加锁 |
| `os_unfair_lock` | 互斥锁 | 否 | 性能优秀，不可递归 |
| `DispatchSemaphore` | 信号量 | 否 | 值 1 时可当锁用，可设超时 |
| `pthread_mutex` | 互斥锁 | 可选 | 底层 C 锁，性能好 |
| `pthread_rwlock` | 读写锁 | 否 | 读可并发、写独占，多读单写首选 |

> 注意：OC 的 `@synchronized` 在 Swift 里**不能直接用**（那是 OC 语法），等价实现是 `objc_sync_enter/exit`，但日常更推荐直接用 `NSLock`。Swift 的属性也**没有 atomic/nonatomic 修饰符**——属性默认就是非原子的，需要线程安全时必须自己加锁。

### 3. NSLock 与 NSRecursiveLock

```swift
let lock = NSLock()
lock.lock()
// 临界区
lock.unlock()
```

```swift
let lock = NSRecursiveLock()

func methodA() {
    lock.lock()
    methodB()      // 递归锁：同一线程可重复加锁
    lock.unlock()
}
func methodB() {
    lock.lock()
    // ...
    lock.unlock()
}
```

**易错点**：`NSLock` **不可递归**——同一线程对同一个 `NSLock` 连续 `lock` 两次会**死锁**。有递归调用场景必须用 `NSRecursiveLock`。

### 4. os_unfair_lock（自旋锁的继任者）

`OSSpinLock` 是经典自旋锁（忙等，不睡眠），但因**优先级反转**问题已被废弃，iOS 10 起用 `os_unfair_lock` 替代：

```swift
import os

var lock = os_unfair_lock_s()
os_unfair_lock_lock(&lock)
// 临界区
os_unfair_lock_unlock(&lock)
```

- 等待时会睡眠而非忙等，避免优先级反转；
- **不可递归**，重复 lock 会死锁；
- 适合极短临界区、高频加解锁。

### 5. dispatch_semaphore 当锁用

信号量初始值为 1 时，就是一个高效的互斥锁：

```swift
let sem = DispatchSemaphore(value: 1)
sem.wait()
// 临界区
sem.signal()
```

### 6. 死锁

**死锁产生的四个必要条件**：

1. **互斥**：资源一次只能被一个线程占用；
2. **占有并等待**：持有资源的同时等待其他资源；
3. **不可剥夺**：资源只能被持有者主动释放；
4. **循环等待**：线程间形成「A 等 B、B 等 C、C 等 A」的环。

只要破坏其一即可避免。常见死锁场景与对策：

| 场景 | 原因 | 对策 |
|------|------|------|
| 主线程 `sync` 主队列 | 串行队列自己等自己 | 改用 `async` |
| 串行队列内 `sync` 自己 | 同上 | 改用 async，或换队列 |
| 嵌套加锁顺序不一致 | 循环等待 | **全局统一加锁顺序** |
| `NSLock` 重复 lock | 不可重入 | 用 `NSRecursiveLock` |

---

## 四、Swift 现代并发 async/await

Swift 5.5 引入的并发体系是范式级变革，核心四件事：**async/await**（把异步写成同步）、**Task**（任务与结构化并发）、**Actor**（数据隔离）、**Sendable**（编译器级数据竞争检查）。

### 1. 为什么需要 async/await

GCD 好用，但有四个结构性缺陷：

1. **数据竞争无法检查**：闭包里访问共享变量有没有加锁，编译器一无所知；
2. **回调地狱**：层层嵌套的 completion handler，可读性差、错误处理散乱；
3. **线程爆炸**：大量并发 block 会撑爆线程池，阻塞系统；
4. **取消与错误处理困难**：想取消排队的 block、在回调里优雅抛错，都很别扭。

async/await、Actor、Sendable 正是针对这些痛点的系统性解法。

### 2. async 函数与 await

```swift
func fetchUser() async throws -> User {
    let data = try await download()     // await 挂起，但不阻塞线程
    let user = try decode(data)
    return user
}
```

对比 GCD 的回调版本，async/await 的杀手锏是**消灭了回调嵌套**：异步代码读起来和同步代码一样线性，错误用 `try` 统一处理。

### 3. 挂起 ≠ 阻塞（关键理解）

这是理解 async/await 的钥匙：

| 操作 | 行为 | 线程 |
|------|------|------|
| `await`（挂起） | 函数暂停，等结果就绪后恢复 | **释放线程**去做别的事 |
| `sync`（阻塞） | 线程卡死干等 | 占着线程不干活 |

- **挂起（suspend）**：线程让出来，资源高效利用；
- **阻塞（block）**：线程占着不干活，是资源浪费。

编译器会把 async 函数翻译成**状态机**：每个 `await` 都是一个挂起点，挂起时保存局部状态，恢复时接着跑。这与 Kotlin 协程的 `suspend` 是同一套「CPS 转换 + 状态机」思想。

### 4. Task：任务的载体

async 函数不能凭空运行，必须放进一个 **Task**：

```swift
Task {
    let user = try await fetchUser()
    print(user)
}
```

Task 代表一个异步工作单元。要点：

- **结构化并发**：Task 有父子关系，父任务会等子任务完成；
- **取消传播**：父 Task 取消，子 Task 自动收到取消信号；
- **优先级继承**：子 Task 继承父 Task 的优先级。

### 5. 结构化并发：async let

需要**并行**执行多个互不依赖的异步操作时，用 `async let`：

```swift
func loadPage() async throws -> Page {
    async let header = fetchHeader()     // 并行开始
    async let content = fetchContent()   // 并行开始
    async let footer = fetchFooter()
    return try await Page(header, content, footer)   // 统一等待
}
```

`async let` 的价值是「**并行 + 结构化**」：三个请求并发执行，但作用域结束时一定会等它们全部完成——不会「任务跑飞」。对比 GCD 的 `DispatchGroup`，`async let` 把「等待所有任务」从手动 `enter/leave` 变成了编译器自动管理，从根上消灭了「配对错误」。

**易错点**：`async let` 创建的子任务**必须被 await**，否则作用域退出时会隐式等待但错误可能被吞掉——务必 `try await` 所有 async let。

### 6. 结构化并发：TaskGroup

`async let` 适合「固定数量」的并行，任务数量**动态不确定**时用 `TaskGroup`：

```swift
func downloadAll(_ urls: [URL]) async -> [Data] {
    await withTaskGroup(of: Data.self) { group in
        for url in urls {
            group.addTask { try await download(url) }   // 动态添加
        }
        var results: [Data] = []
        for await data in group {   // 逐个收集结果
            results.append(data)
        }
        return results
    }
}
```

TaskGroup 与 async let 共享同一保证：**作用域内所有子任务在退出前都会完成**，子任务抛出的错误会向上传播。这就是「结构化并发」名称的由来——任务父子关系形成**任务树**，生命周期严格被作用域约束。

### 7. 取消

```swift
let task = Task { await longWork() }
task.cancel()                        // 发出取消信号

// 被取消方需主动响应
func longWork() async throws {
    try Task.checkCancellation()     // 已取消则抛出，立即退出
    // 或检查 Task.isCancelled
}
```

取消是**协作式**的：`cancel()` 只发信号，不会强制中断。异步代码需在挂起点检查 `Task.isCancelled`，或调用 `try Task.checkCancellation()` 主动响应。这与 GCD 的 block「无法取消」形成鲜明对比。

### 8. Actor：编译器强制的数据隔离

Actor 是引用类型，但它内部的状态**被隔离**——只能通过 actor 方法访问，且同一时刻只有一个任务能进入：

```swift
actor BankAccount {
    private var balance = 0

    func deposit(_ amount: Int) {   // 编译器保证串行访问 balance
        balance += amount
    }

    func getBalance() -> Int { balance }
}
```

**为什么 Actor 比锁更强**：锁要求你「记住」给哪块数据上哪把锁，忘了就出 bug；Actor 把「数据隔离」写进类型本身，**编译器强制**所有内部状态访问都走 actor 方法并串行化。数据竞争从「运行时可能发生的 bug」变成了「编译不过的错误」。

**关键易错点——Actor 可重入**：

```swift
actor BankAccount {
    private var balance = 0
    func withdraw(_ amount: Int) async {
        let current = balance        // ① 读
        await someAsyncWork()        // ② 挂起点！此时别的任务可进入 actor 改 balance
        balance = current - amount   // ③ 用旧值写，可能覆盖别人的修改
    }
}
```

Actor 方法在 `await` 处会**挂起并让出**，挂起期间其他任务可以进入 actor。若在 `await` 前后都依赖某个「读到的状态」，恢复后这个状态可能已经变了。**Actor 隔离了数据竞争，但没隔离逻辑竞态**——`await` 之间的代码要假设状态可能已变化。

### 9. Sendable：编译器级数据竞争检查

`Sendable` 协议标记「可以安全地跨并发域传递」的类型：

```swift
struct User: Sendable { let name: String }   // 值类型天然 Sendable
final class Cache: Sendable { ... }          // 不可变类可 Sendable
```

编译器用 Sendable 做**静态数据竞争检查**：把非 Sendable 的可变对象从一个并发域传到另一个，会给出警告甚至报错。这解决了 GCD 时代的根本问题——「这个对象跨线程传安全吗」从「靠经验判断」变成了「编译器保证」。

| 类型 | 是否天然 Sendable |
|------|------------------|
| struct / enum（值类型） | 是 |
| 不可变引用类型 | 可声明 Sendable |
| 可变引用类型 | **不是**，跨并发域传递触发检查 |

确需绕过时用 `@unchecked Sendable`，但要自负其责。

### 10. MainActor 与 @MainActor

UI 更新必须在主线程，Swift 用 `@MainActor` 把这个约束也交给编译器：

```swift
@MainActor
class ViewModel {
    var title = ""
    func updateUI() { }     // 保证在主线程执行
}

func refresh() async {
    await MainActor.run { updateUI() }   // 显式切回主线程
}
```

`@MainActor` 让「哪些代码必须在主线程」成为类型/函数的静态属性，编译器自动插入线程切换，漏掉主线程调用会在编译期报警。对比 GCD 时代「手动 `DispatchQueue.main.async` 且忘了就崩溃」，这是巨大的进步。

---

## 五、多读单写

**场景**：一个数据（如缓存字典）被频繁读、偶尔写。若读也加互斥锁，读读之间也会被串行化，浪费并发能力。多读单写（Multiple Readers, Single Writer）的目标是：**读可以并发，写必须独占，且写时不能有读**。

### 1. 方案一：dispatch_barrier（推荐，最简洁）

```swift
final class DataStore {
    // 关键：必须是「自定义并发队列」
    private let queue = DispatchQueue(label: "com.demo.store", attributes: .concurrent)
    private var dict: [String: Any] = [:]

    // 读：并发执行，多个读可同时进行
    func get(_ key: String) -> Any? {
        queue.sync { dict[key] }     // sync 是为了「有返回值，阻塞等结果」
    }

    // 写：栅栏，独占执行
    func set(_ key: String, _ value: Any) {
        queue.async(flags: .barrier) {
            self.dict[key] = value    // async：写不需要立即返回，栅栏独占
        }
    }
}
```

**要点**：

- 读用 `sync`（需要返回值，阻塞等结果）；
- 写用 `async(flags: .barrier)`（不需要返回值，异步 + 独占）；
- 队列必须是 `.concurrent`，否则 barrier 失效。

### 2. 方案二：Actor（Swift 并发写法）

```swift
actor DataStore {
    private var dict: [String: Any] = [:]

    func get(_ key: String) -> Any? { dict[key] }
    func set(_ key: String, _ value: Any) { dict[key] = value }
}
```

Actor 把「访问串行化」交给编译器，比 barrier 更简洁也更安全。

### 3. 方案对比

| 维度 | dispatch_barrier | Actor |
|------|-----------------|-------|
| 实现复杂度 | 低（纯 GCD API） | 更低（编译器管） |
| 安全性 | 靠开发者正确使用 | 编译器强制 |
| 调用方式 | 同步方法 | 需 `await` 调用 |
| 适用 | 同步调用场景 | async/await 场景首选 |

---

## 六、常见问题与最佳实践

### 1. 常见崩溃与坑

| 坑 | 说明 |
|----|------|
| 子线程操作 UIKit | 必须在主线程更新 UI，否则崩溃或渲染异常 |
| `dispatch_group` enter/leave 不配对 | leave 多于 enter 直接崩溃 |
| barrier 用在全局队列 | 不生效，写操作可能与其他读写并发 |
| `NSLock` 重复 lock | 死锁 |
| Actor 方法 `await` 前后假设状态不变 | 逻辑竞态 |
| 可变引用类型跨并发域传递 | 数据竞争，应声明 Sendable |
| 误以为 `await` 会阻塞线程 | 挂起 ≠ 阻塞 |

### 2. 最佳实践清单

1. **UI 永远主线程**：`@MainActor` + `MainActor.run`；
2. **新代码优先 async/await**，避免回调嵌套；
3. **共享可变状态优先 Actor**，而不是手动加锁；
4. **跨并发域传值声明 Sendable**，让编译器帮你查竞态；
5. **多读单写用 Actor 或 barrier**；
6. **避免嵌套 sync**，尤其主线程 sync 主队列；
7. **锁的粒度尽量小**，临界区代码越短越好；
8. **Actor 方法内 `await` 后重新校验状态**；
9. **统一加锁顺序**，避免死锁；
10. **控制并发数量**：用 `DispatchSemaphore` 或 `TaskGroup` 分批。

---

## 附：高频速记

- **并发 vs 并行**：并发是逻辑同时（切换），并行是物理同时（多核）。
- **sync 不开新线程**，阻塞当前线程；**async 是否开线程看队列**。
- **主线程 sync 主队列 → 死锁**；串行队列内 sync 自己 → 死锁。
- **barrier 只对自定义并发队列生效**，用于多读单写。
- **信号量**：`wait` 减一、`signal` 加一；初始值 = 最大并发数。
- **enter/leave 必须配对**。
- **挂起（await）≠ 阻塞（sync）**：await 释放线程，sync 占着线程。
- **async 函数编译成状态机**，await 是挂起点。
- **结构化并发**：Task 父子关系，作用域结束必等子任务；async let 固定并行、TaskGroup 动态并行。
- **取消是协作式**：cancel 发信号，需自己检查 `Task.isCancelled`。
- **Actor 隔离数据、编译器强制串行**；但 `await` 处可重入，恢复后状态可能已变。
- **Sendable**：编译器数据竞争检查；值类型天然 Sendable。
- **@MainActor**：主线程隔离交给编译器。
