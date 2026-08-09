# LeetCode 46 - Permutations（全排列）

| 项目 | 内容 |
|------|------|
| 难度 | Medium |
| 链接 | https://leetcode.cn/problems/permutations/ |
| 类别 | 回溯（Backtracking） |
| 关联题目 | #47 全排列 II（含重复元素）, #78 子集, #77 组合, #39 组合总和 |

---

## 题目描述

给定一个**不含重复数字**的数组 `nums`，返回其所有可能的全排列。你可以按任意顺序返回答案。

### 示例

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

输入：nums = [0,1]
输出：[[0,1],[1,0]]

输入：nums = [1]
输出：[[1]]
```

### 约束

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- `nums` 中的所有整数**互不相同**

---

## 解题思路

### 核心思想：回溯（DFS + 状态恢复）

全排列的本质是**枚举所有可能的顺序**。回溯法通过深度优先搜索构建排列，每层选择一个未使用的元素加入路径，递归到底后回溯（撤销选择），继续尝试其他分支。

```
回溯三要素：
  路径（path）：已选的元素列表，构成当前排列
  选择列表：尚未使用的元素（通过 used[] 标记）
  终止条件：path.size() == nums.length → 找到一个完整排列
```

### 决策树示例（nums = [1, 2, 3]）

```text
                        []
           /            |            \
         [1]           [2]           [3]          ← 第 1 层，选第 1 个元素
        /    \        /    \        /    \
     [1,2]  [1,3]  [2,1]  [2,3]  [3,1]  [3,2]    ← 第 2 层
      |       |      |       |      |       |
   [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1] ← 第 3 层（终点）
```

每一层选择一个未使用的元素，递归到下一层。到达叶子节点时 path 长度 == 3，记录一个完整排列，然后回溯撤销最后一个选择，尝试该层的其他选项。

### 回溯模板

```text
void backtrack(路径, 选择列表) {
    if (终止条件) {
        记录结果;
        return;
    }
    for (选择 in 选择列表) {
        if (选择已使用) continue;
        做选择：将元素加入路径、标记已用;
        backtrack(路径, 新选择列表);
        撤销选择：移除元素、取消标记;
    }
}
```

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n × n!) — 共 n! 个排列，每个排列复制 cost O(n) |
| 空间 | O(n) — used 数组 + 递归栈深度 |

---

## 代码实现

### Java

```java
import java.util.*;

class Solution {
    private List<List<Integer>> resultList = new ArrayList<>();

    public List<List<Integer>> permute(int[] nums) {
        if (nums == null) {
            return resultList;
        }

        traversal(nums, 0, new int[nums.length], new ArrayList<>());
        return resultList;
    }

    private void traversal(int[] nums, int currentIndex,
                           int[] usedFlags, List<Integer> pathList) {
        // 终止条件：路径长度 == 数组长度，找到一个完整排列
        if (pathList.size() == nums.length) {
            resultList.add(new ArrayList<>(pathList)); // 深拷贝
            return;
        }

        // 遍历选择列表，每次都从 0 开始（排列需考虑所有未使用元素）
        for (int index = 0; index < nums.length; index++) {
            if (usedFlags[index] == 1) {
                continue;   // 已使用，跳过
            }

            // 做选择
            pathList.add(nums[index]);
            usedFlags[index] = 1;

            // 递归进入下一层
            traversal(nums, index + 1, usedFlags, pathList);

            // 撤销选择（回溯核心）
            pathList.remove(pathList.size() - 1);
            usedFlags[index] = 0;
        }
    }
}
```

**写法要点**：
- `int[] usedFlags` 用 0/1 标记替代 `boolean[]`——排列关心顺序，同一元素不能在不同位置出现两次
- `resultList` 作为实例变量，省去递归中透传的模板参数
- `resultList.add(new ArrayList<>(pathList))` **必须深拷贝**——回溯过程中 `pathList` 会被撤销修改
- 回溯的「撤销」和「做选择」严格对称：`add` ↔ `remove`、`usedFlags = 1` ↔ `usedFlags = 0`

---

## 关键点总结

1. **排列 vs 组合**：排列需要 `used[]` 标记已选元素（`[1,2]` 和 `[2,1]` 是不同的排列）；组合用 `start` 索引避免重复
2. **回溯 = DFS + 撤销**：递归前做选择，递归后撤销——保证了每次回溯回到上一层的状态时，path 和 used 都是干净的
3. **终止条件**：`path.size() == nums.length`——排列长度固定等于数组长度
4. **结果复制**：`new ArrayList<>(path)` 必须深拷贝，否则回溯撤销会把结果改坏
5. **与 #47 的区别**：#46 元素互不相同，用 `used[]` 即可；#47 含重复元素，需要额外排序 + 剪枝去重

---

## 延伸思考

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #47 | 全排列 II | 含重复元素 → 排序 + `used[i-1]` 剪枝 |
| #78 | 子集 | 不要求长度 = n，每层都记录 |
| #77 | 组合 | 用 `start` 索引控制顺序不重复，而非 `used[]` |
| #39 | 组合总和 | 可重复选择 + 目标和限制 |
| #22 | 括号生成 | 回溯条件变成「左括号数 ≤ 右括号数」 |
