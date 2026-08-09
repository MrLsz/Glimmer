# LeetCode 104 - Maximum Depth of Binary Tree（二叉树的最大深度）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/maximum-depth-of-binary-tree/ |
| 类别 | 树 / DFS（深度优先搜索） |
| 关联题目 | #111 二叉树的最小深度, #110 平衡二叉树, #543 二叉树的直径 |

---

## 题目描述

给定一个二叉树 `root`，返回其最大深度。

二叉树的**最大深度**是指从根节点到最远叶子节点的最长路径上的节点数。

### 示例

```
输入：root = [3,9,20,null,null,15,7]
    3
   / \
  9  20
     / \
    15  7
输出：3

输入：root = [1,null,2]
输出：2
```

### 约束

- 树中节点的数量在 `[0, 10^4]` 范围内
- `-100 <= Node.val <= 100`

---

## 解题思路

### 核心思想：DFS 递归求子树深度

每个节点的深度 = `max(左子树深度, 右子树深度) + 1`。递归到底，逐层向上累加。

```
traversal(node):
  if node == null → return 0                           // 空树深度为 0
  if node.left == null → return traversal(right) + 1    // 只有右子树
  if node.right == null → return traversal(left) + 1    // 只有左子树
  return max(traversal(left), traversal(right)) + 1     // 左右都有
```

> 代码中的前两个 `if` 是剪枝优化——当一子树为空时，避免多余的递归调用，直接走另一侧。效果上与标准写法等效，但减少了无意义的空节点遍历。

### 递归推演（root = [3, 9, 20, null, null, 15, 7]）

```text
traversal(3)
  left = traversal(9)         right = traversal(20)
           ↓                            ↓
     left null → traversal(null)=0     traversal(15) → 1
     right null → traversal(null)=0    traversal(7)  → 1
     取 max(0,0)+1 = 1                取 max(1,1)+1 = 2

  取 max(1, 2) + 1 = 3  ← 答案
```

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n) — 每个节点访问一次 |
| 空间 | O(h) — 递归栈深度，h 为树的高度，最坏倾斜树 O(n) |

---

## 代码实现

### Java

```java
class Solution {
    public int maxDepth(TreeNode root) {
        return traversal(root);
    }

    private int traversal(TreeNode node) {
        // 空节点深度为 0
        if (node == null) {
            return 0;
        }
        // 剪枝：左子为空，只需看右子
        if (node.left == null) {
            return traversal(node.right) + 1;
        }
        // 剪枝：右子为空，只需看左子
        if (node.right == null) {
            return traversal(node.left) + 1;
        }
        // 左右均非空，取较深的子树 +1
        return Math.max(traversal(node.left) + 1, traversal(node.right) + 1);
    }
}
```

---

## 关键点总结

1. **递归思想**：树的深度 = 子树深度 + 1，天然适合递归解决
2. **终止条件**：节点为 `null` 时返回 `0`，这是递归的底部
3. **剪枝优化**：当一侧子树为空，跳过多余的 `traversal(null)` 调用——标准写法可以简化但逻辑等价
4. **DFS vs BFS**：DFS 递归写法最简洁；BFS 层序遍历也可以通过「层数计数」得到同样结果
5. **与 #111 的区分**：#104 求最深，#111 求最浅——区别在终止条件：最小深度要考虑只有单子树的情况

---

## 延伸思考

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #111 | 二叉树的最小深度 | 求最浅叶子，需处理单子树场景 |
| #110 | 平衡二叉树 | 每个节点检查左右子树深度差 ≤ 1 |
| #543 | 二叉树的直径 | 最大深度 + 跨节点路径 |
| #102 | 二叉树的层序遍历 | BFS 按层输出，层数即深度 |
