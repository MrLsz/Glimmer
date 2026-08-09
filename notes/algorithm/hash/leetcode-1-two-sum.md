# LeetCode 1 - Two Sum（两数之和）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/two-sum/ |
| 类别 | 哈希表 |
| 关联题目 | #167 Two Sum II（有序数组）, #15 3Sum, #18 4Sum, #454 4Sum II |

---

## 题目描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出**和为目标值** `target` 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，且**不能使用两次相同的元素**。你可以按任意顺序返回答案。

### 示例

```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9，返回 [0, 1]

输入：nums = [3,2,4], target = 6
输出：[1,2]

输入：nums = [3,3], target = 6
输出：[0,1]
```

### 约束

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- **只会存在一个有效答案**

---

## 解题思路

### 核心思想：HashMap 将「查找」时间降到 O(1)

暴力法是两层循环扫描所有组合，时间 O(n²)。优化方向很直接：**能否在遍历时，立刻知道 `target - nums[i]` 是否已经出现过？**

HashMap 恰好能胜任：键存值、值存下标，查找 `target - nums[i]` 只需 O(1)。

```
遍历 nums[i]:
  complement = target - nums[i]
  if map.containsKey(complement):
      return [map.get(complement), i]   // 找到
  map.put(nums[i], i)                   // 未找到，记录当前值
```

> **为什么把 put 放在检查之后**：题目要求「不能使用两次相同的元素」。如果先 put 再检查，当 `nums[i] == target / 2` 时会把同一个元素用两次。顺序保证了只查找**之前**已出现的值。

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n) — 遍历一次，每次 HashMap 操作 O(1) |
| 空间 | O(n) — 最坏情况下存入 n-1 个元素 |

---

## 代码实现

### Java

```java
import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        // key = 数组值, value = 下标
        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];

            // 先查：complement 是否已经在之前的元素中出现过
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }

            // 后存：当前值记录到 map
            map.put(nums[i], i);
        }

        return new int[0]; // 题目保证有答案，不会走到这里
    }
}
```

**写法要点**：
- 用 `HashMap` 而非数组下标映射——因为 `nums[i]` 范围是 ±10⁹，数组装不下
- **先查后存**保证同一元素不会被用两次（处理 `target = 2×nums[i]` 的边界）
- `complement` 用 `int` 不会溢出，因为 target 和 nums[i] 均在 ±10⁹ 范围

---

## 关键点总结

1. **O(1) 查找是核心**：HashMap 的 `containsKey` 将「判断补数是否出现过」从 O(n) 降到 O(1)
2. **有序与无序的区别**：#1 的输入是**无序**数组，只能用 HashMap；若数组有序（如 #167），可用双指针进一步压缩空间到 O(1)
3. **先查后存的顺序**：决定了能否正确处理 `target = 2 × nums[i]` 的边界情况
4. **空间换时间**：经典做法——牺牲 O(n) 空间把时间从 O(n²) 拉到 O(n)
5. **HashMap 的 key 选择**：key 是数组值而非下标——因为我们要按值查下标，方向不能反

---

## 延伸思考

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #167 | 两数之和 II（有序数组） | 输入有序 → 双指针 O(n)/O(1) |
| #15 | 三数之和 | 三数 → 排序 + 双指针 + 去重 |
| #18 | 四数之和 | 四数 → 排序 + 双指针 + 剪枝 |
| #454 | 四数相加 II | 四个数组 → 分组 + HashMap |
| #170 | 两数之和 III（数据结构设计） | 多次查询 → 设计 add/find 接口 |
