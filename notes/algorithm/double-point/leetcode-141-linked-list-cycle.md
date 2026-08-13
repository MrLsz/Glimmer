# LeetCode 141 - Linked List Cycle（环形链表）

> 判断链表是否有环是快慢指针（Floyd 判圈算法）的入门模板题——快指针每次走两步、慢指针走一步，有环则必然相遇。掌握后再做 #142 环形链表 II（找环入口）就顺理成章。

| 项目   | 内容                                                                                                           |
| ---- | ------------------------------------------------------------------------------------------------------------ |
| 难度   | Easy                                                                                                         |
| 链接   | <https://leetcode.cn/problems/linked-list-cycle/>                                                            |
| 类别   | 快慢指针                                                                                                         |
| 关联题目 | #142 Linked List Cycle II, #202 Happy Number, #876 Middle of the Linked List, #287 Find the Duplicate Number |

---

## 题目描述

给定链表的头节点 `head`，判断链表中是否有环。如果链表中某个节点可以通过 `next` 指针再次到达，则链表中存在环。

```
示例 1: 3 → 2 → 0 → -4 → (回到 2) → true
示例 2: 1 → 2 → (回到 1) → true
示例 3: 1 → null → false
```

约束：节点数范围 `[0, 10^4]`，`-10^5 <= node.val <= 10^5`

---

## 解题思路

### 快慢指针（Floyd 判圈算法）

设两个指针：慢指针 `slow` 每次走 1 步，快指针 `fast` 每次走 2 步。如果链表无环，`fast` 会先到 `null`；如果有环，两个指针会先后进入环，由于速度差为 1，最终必然相遇。

```text
有环链表: 3 → 2 → 0 → -4 → (回到 2)

slow=3, fast=3
slow=2, fast=0      (slow 走 1 步, fast 走 2 步)
slow=0, fast=2      (fast 绕了一圈)
slow=-4, fast=-4    ← 相遇，返回 true
```

### 为什么必然相遇？

进入环后，快指针每次比慢指针多走 1 步。相当于快指针以速度 1「追」慢指针，差距每次缩小 1，最终从「相差一段距离」到「相遇」——不会跳过。

### 复杂度分析

- **时间**：`O(N)`——无环时 fast 走到末尾；有环时最多走 N + 环长
- **空间**：`O(1)`——只用了两个指针

---

## 代码实现

```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        if (head == null) {
            return false;
        }

        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;         // 慢指针走 1 步
            fast = fast.next.next;    // 快指针走 2 步

            if (slow == fast) {
                return true;          // 相遇 → 有环
            }
        }
        return false;                 // fast 到 null → 无环
    }
}
```

---

## 关键点总结

1. **快慢指针速度差为 1**：这是保证「有环必相遇、不会跳过」的关键——快指针每次多走 1 步
2. **循环条件 `fast != null && fast.next != null`**：`fast.next.next` 需要两层判空保护
3. **从同一起点出发**：`slow = fast = head`，进入循环后再走，比「slow=head, fast=head.next」的错位写法更简洁
4. **Floyd 算法的扩展**：#142 找环入口时，相遇后让一个指针回到 head，两指针同步走，再次相遇点即环入口

---

## 延伸思考

| 题目                             | 关联点                          |
| ------------------------------ | ---------------------------- |
| #142 Linked List Cycle II      | 找环入口——相遇后指针回 head 同步走        |
| #202 Happy Number              | 数字变换的「隐式环」——快慢指针或哈希集判断是否进入循环 |
| #876 Middle of the Linked List | 快慢指针找中点——快指针到末尾时慢指针在中点       |
| #287 Find the Duplicate Number | 数组中的环——把下标和值视为指针，用快慢指针判圈     |
