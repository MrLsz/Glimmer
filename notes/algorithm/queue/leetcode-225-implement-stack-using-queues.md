# LeetCode 225 - Implement Stack using Queues（用队列实现栈）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/implement-stack-using-queues/ |
| 类别 | 队列 / 栈 |
| 关联题目 | #232 用栈实现队列, #155 最小栈 |

---

## 题目描述

请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（`push`、`pop`、`top` 和 `empty`）。

实现 `MyStack` 类：

- `void push(int x)` — 将元素 x 压入栈顶
- `int pop()` — 移除并返回栈顶元素
- `int top()` — 返回栈顶元素
- `boolean empty()` — 如果栈为空，返回 `true`；否则，返回 `false`

### 示例

```
输入：
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]

解释：
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top();   // 返回 2
myStack.pop();   // 返回 2
myStack.empty(); // 返回 false
```

### 约束

- `1 <= x <= 9`
- 最多调用 `100` 次 `push`、`pop`、`top` 和 `empty`
- 每次调用 `pop` 和 `top` 都保证栈不为空

---

## 解题思路

### 核心思想：push 时反转队列顺序

队列是 FIFO（先进先出），栈是 LIFO（后进先出）。让队列模拟栈的关键：**每次 `push` 时，把新元素调整到队列头部**，使队列的顺序变成栈的顺序。

```
push(x):
  1. 将 x 放入辅助队列 queue2
  2. 将主队列 queue1 的所有元素依次出队，入队到 queue2
  3. 交换 queue1 和 queue2 的引用

结果：queue1 的队首 = 最后 push 的元素（即栈顶）
```

### 两个队列的分工

| 队列 | 角色 |
|------|------|
| `queue1` | 专职栈——始终按栈顺序存放元素，队首 = 栈顶 |
| `queue2` | 辅助队列——仅在 push 时临时存放，用完即换回 |

### push 推演

```text
初始：queue1 = [1, 2]     ← 队首是 1，但栈顶应是 2（因为 2 后 push）
push(3):
  ① queue2.offer(3)       → queue2 = [3]
  ② queue1 → queue2       → queue2 = [3, 1, 2]
  ③ 交换引用              → queue1 = [3, 1, 2], queue2 = []

现在 queue1 队首是 3，符合栈顶就应返回 3
```

### 复杂度分析

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `push` | O(n) | 需要将 queue1 全部倒入 queue2 |
| `pop` | O(1) | 直接 poll queue1 的队首 |
| `top` | O(1) | 直接 peek queue1 的队首 |
| `empty` | O(1) | 判断 queue1 是否为空 |

---

## 代码实现

### Java

```java
class MyStack {

    private Queue<Integer> queue1 = new LinkedList<>();
    private Queue<Integer> queue2 = new LinkedList<>();

    public MyStack() {
    }

    public void push(int x) {
        // 1. 新元素入辅助队列
        queue2.offer(x);

        // 2. 主队列的全部元素倒入辅助队列（新元素变队首）
        while (!queue1.isEmpty()) {
            queue2.offer(queue1.poll());
        }

        // 3. 交换引用：queue1 始终保持栈顺序
        Queue<Integer> tempQueue = queue1;
        queue1 = queue2;
        queue2 = tempQueue;
    }

    public int pop() {
        return queue1.poll();   // 队首 = 栈顶
    }

    public int top() {
        return queue1.peek();   // 队首 = 栈顶
    }

    public boolean empty() {
        return queue1.isEmpty();
    }
}
```

**写法要点**：
- `push` 中交换引用的开销是 O(1)——不复制数据，只交换两个变量指向的对象
- 日常操作 `pop`/`top`/`empty` 都是 O(1)，只在 `push` 时付出 O(n) 代价
- 与 #232「用栈实现队列」对称：栈实现队列需要两个栈（inStack + outStack），`pop` 时 Pay 成本

---

## 关键点总结

1. **核心矛盾**：队列 FIFO vs 栈 LIFO，解法是把新元素推到队首（破坏队列的自然顺序）
2. **双队列分工**：`queue1` 始终维护栈顺序，`queue2` 只做 push 时的临时容器
3. **交换引用**：`tempQueue = queue1; queue1 = queue2; queue2 = tempQueue` 是 O(1) 的指针交换
4. **push 代价集中**：每次 `push` 是 O(n)，但 `pop`/`top` 直接 O(1)
5. **单队列变体**：可以只用 1 个队列，push 时先将 x 入队，再把前 n-1 个元素依次出队再入队（效果相同，空间更省）

---

## 延伸思考

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #232 | 用栈实现队列 | 对称题——两个栈模拟队列，方向相反 |
| #155 | 最小栈 | 在 O(1) 内获取栈中最小值，需辅助栈 |
| #716 | 最大栈 | 最小栈的镜像 |
| #225 变体 | 单队列实现 | 仅用一个队列 + push 时自旋 |
