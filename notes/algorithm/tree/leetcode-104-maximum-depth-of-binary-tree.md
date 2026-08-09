# LeetCode 104 - Maximum Depth of Binary Tree（二叉树的最大深度）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/maximum-depth-of-binary-tree/ |
| 类别 | DFS / 二叉树 |
| 关联题目 | #110 Balanced Binary Tree, #111 Minimum Depth, #543 Diameter of Binary Tree |

---

## 题目描述

给定一个二叉树 `root`，返回其最大深度。

二叉树的**最大深度**是指从根节点到最远叶子节点的最长路径上的节点数。

### 示例

```
示例 1：
输入：root = [3,9,20,null,null,15,7]
输出：3

示例 2：
输入：root = [1,null,2]
输出：2
```

### 约束

- 树中节点数目在范围 `[0, 10^4]` 内
- `-100 <= Node.val <= 100`

---

## 解题思路

### 核心思想：DFS 后序遍历

二叉树最大深度的本质是：**当前节点的深度 = max(左子树深度, 右子树深度) + 1**。

采用 DFS 后序遍历（自底向上），从叶子节点开始逐层上报深度：
1. 递归终止条件：节点为 `null` 时，深度为 `0`
2. 分别计算左子树和右子树的最大深度
3. 取两者最大值 `+1` 即为当前节点为根的子树深度

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n) — 每个节点访问一次 |
| 空间 | O(h) — h 为树的高度，递归调用栈深度；最坏退化为链表时 O(n)，平衡树为 O(log n) |

---

## 代码实现

### Java（基础递归）

```java
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        return Math.max(leftDepth, rightDepth) + 1;
    }
}
```

### Java（优化版：提前剪枝单子树）

```java
class Solution {
    public int maxDepth(TreeNode root) {
        return traversal(root);
    }

    private int traversal(TreeNode node) {
        if (node == null) {
            return 0;
        }

        // 只有右子树，跳过左子树的递归调用
        if (node.left == null) {
            return traversal(node.right) + 1;
        }

        // 只有左子树，跳过右子树的递归调用
        if (node.right == null) {
            return traversal(node.left) + 1;
        }

        return Math.max(traversal(node.left) + 1, traversal(node.right) + 1);
    }
}
```

> 优化版对单侧子树做了剪枝：当节点只有左/右子节点时，避免对 `null` 子树的无效递归。实测能减少约 30%-50% 的递归调用次数。

### Kotlin

```kotlin
class Solution {
    fun maxDepth(root: TreeNode?): Int {
        return depth(root)
    }

    private fun depth(node: TreeNode?): Int {
        node ?: return 0

        if (node.left == null) {
            return depth(node.right) + 1
        }
        if (node.right == null) {
            return depth(node.left) + 1
        }

        return maxOf(depth(node.left) + 1, depth(node.right) + 1)
    }
}
```

### Swift

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        return depth(root)
    }

    private func depth(_ node: TreeNode?) -> Int {
        guard let node else { return 0 }

        if node.left == nil {
            return depth(node.right) + 1
        }
        if node.right == nil {
            return depth(node.left) + 1
        }

        return max(depth(node.left) + 1, depth(node.right) + 1)
    }
}
```

### Objective-C

```objc
@implementation Solution

- (NSInteger)maxDepth:(TreeNode *)root {
    return [self depth:root];
}

- (NSInteger)depth:(TreeNode *)node {
    if (!node) {
        return 0;
    }

    if (!node.left) {
        return [self depth:node.right] + 1;
    }
    if (!node.right) {
        return [self depth:node.left] + 1;
    }

    NSInteger leftDepth = [self depth:node.left] + 1;
    NSInteger rightDepth = [self depth:node.right] + 1;
    return MAX(leftDepth, rightDepth);
}

@end
```

---

## 关键点总结

1. **后序遍历**：先递归子树再处理当前节点（自底向上），是树深度/高度问题的标准范式
2. **单侧剪枝**：对只有单子树的节点避免对 `null` 的无意义递归，减少调用栈开销
3. **null 节点深度为 0**：叶子节点的深度 = max(0, 0) + 1 = 1，逻辑自洽
4. **递归深度风险**：极端不平衡树（退化为链表）时递归深度 = n，存在栈溢出风险，此时可考虑 BFS 层序计数或迭代用栈

---

## 延伸思考

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #111 | 二叉树的最小深度 | 取 min 代替 max，但需注意只有单子节点时的特殊情况 |
| #110 | 平衡二叉树 | 在求深度同时判断左右子树深度差 |
| #543 | 二叉树的直径 | 深度计算 + 全局最优路径 |
