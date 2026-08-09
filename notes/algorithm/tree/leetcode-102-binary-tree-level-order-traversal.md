# LeetCode 102 - Binary Tree Level Order Traversal（二叉树的层序遍历）

| 项目 | 内容 |
|------|------|
| 难度 | Medium |
| 链接 | https://leetcode.cn/problems/binary-tree-level-order-traversal/ |
| 类别 | 二叉树 / BFS（广度优先搜索） |
| 关联题目 | #103 Binary Tree Zigzag Level Order, #107 Level Order II, #199 Right Side View, #429 N-ary Tree Level Order |

---

## 题目描述

给你二叉树的根节点 `root`，返回其节点值的**层序遍历**（即逐层地，从左到右访问所有节点）。

### 示例

```
示例 1：
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
解释：
    3
   / \
  9  20
     / \
    15  7
返回其层序遍历结果。

示例 2：
输入：root = [1]
输出：[[1]]

示例 3：
输入：root = []
输出：[]
```

### 约束

- 树中节点数目在范围 `[0, 2000]` 内
- `-1000 <= Node.val <= 1000`

---

## 解题思路

### 核心思想：BFS + 队列分层处理

二叉树的层序遍历是 BFS（广度优先搜索）最经典的应用场景。使用队列（Queue）辅助，逐层处理节点。

**思路流程：**

1. 特判：若根节点为空，直接返回空列表
2. 将根节点入队
3. 循环处理，直到队列为空：
   - 记录当前队列长度 `levelSize`（即当前层的节点数）
   - 创建一个列表 `currentLevel` 存储当前层的节点值
   - 对本层 `levelSize` 个节点逐个处理：
     - 出队一个节点，将其值加入 `currentLevel`
     - 若该节点有左子节点，将左子节点入队
     - 若该节点有右子节点，将右子节点入队
   - 将 `currentLevel` 加入结果列表
4. 返回结果列表

### 关键设计：记录每层节点数

通过在每一轮循环开始时记录当前队列长度 `levelSize`，可以精确控制本层处理多少个节点，而不受下一层入队节点的影响。这是层序遍历区别于普通 BFS 的核心技巧。

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n) — 每个节点访问一次 |
| 空间 | O(n) — 队列最多存储最宽层的节点数（完美二叉树最底层约 n/2 个节点）；输出结果占用 O(n) |

---

## TreeNode 定义

### Java

```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

---

## 代码实现

### Java

```java
import java.util.*;

class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) {
            return result;
        }

        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> levelValues = new ArrayList<>(levelSize);

            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                levelValues.add(node.val);

                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }

            result.add(levelValues);
        }

        return result;
    }
}
```

---

## 关键点总结

1. **分层控制**：通过 `levelSize = queue.size()` 在每轮循环开始前固定当前层节点数，实现精确的分层输出
2. **BFS 范式**：队列 + while 循环是 BFS 的标准模板，适用于所有树的层序问题
3. **空值处理**：根节点为空的边界条件务必提前处理
4. **队列选择**：Java 中用 `LinkedList` 实现 Queue 接口，性能优于 `ArrayDeque`（需要频繁的 add/remove 操作）

---

## 延伸思考

此题是二叉树层序遍历的基础，通过调整输出顺序和筛选条件可衍生出多类高频题：

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #103 | 二叉树的锯齿形层序遍历 | 交替反转每层输出顺序 |
| #107 | 二叉树的层序遍历 II | 自底向上输出（结果反转即可） |
| #199 | 二叉树的右视图 | 每层只保留最后一个节点值 |
| #637 | 二叉树的层平均值 | 每层计算平均值而非输出全部值 |
| #429 | N 叉树的层序遍历 | 多子节点的扩展 |

