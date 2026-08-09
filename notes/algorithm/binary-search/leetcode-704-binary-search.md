# LeetCode 704 - Binary Search（二分查找）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/binary-search/ |
| 类别 | 二分查找 |
| 关联题目 | #35 Search Insert Position, #69 Sqrt(x), #34 Find First and Last, #33 Search Rotated Array |

---

## 题目描述

给定一个 `n` 个元素有序的（升序）整型数组 `nums` 和一个目标值 `target`，写一个函数搜索 `nums` 中的 `target`，如果目标值存在返回下标，否则返回 `-1`。

### 示例

```
输入：nums = [-1,0,3,5,9,12], target = 9
输出：4
解释：9 出现在 nums 中并且下标为 4

输入：nums = [-1,0,3,5,9,12], target = 2
输出：-1
解释：2 不存在 nums 中因此返回 -1
```

### 约束

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- `nums` 中的所有元素**互不相同**
- `nums` 是按**升序**排列的

---

## 解题思路

### 核心思想：区间收缩

二分查找的本质是**在有序数组中通过不断折半缩小搜索区间，直到找到目标或区间为空**。

```
初始区间：[0, n-1]
每轮计算 mid = left + (right - left) / 2
  → nums[mid] == target → 命中，返回 mid
  → nums[mid] <  target → 目标在右半，left  = mid + 1
  → nums[mid] >  target → 目标在左半，right = mid - 1
终止条件：left > right → 区间为空，返回 -1
```

### 区间定义：左闭右闭 `[left, right]`

推荐使用 `[left, right]` 定义搜索区间，逻辑最直观：

| 含义 | 值 |
|------|-----|
| 初始区间 | `left = 0`, `right = nums.length - 1` |
| 循环条件 | `while (left <= right)` — 区间至少含一个元素 |
| mid 计算 | `left + (right - left) / 2` — 防溢出 |
| 目标在左侧 | `right = mid - 1` — mid 已排除 |
| 目标在右侧 | `left = mid + 1` — mid 已排除 |

> **为什么不写 `mid = (left + right) / 2`**：当 `left + right` 超过 `int` 最大值时溢出，`left + (right - left) / 2` 是安全写法。

### 与左闭右开 `[left, right)` 的对比

| 维度 | `[left, right]`（推荐） | `[left, right)` |
|------|------------------------|-----------------|
| 初始 right | `n - 1` | `n` |
| 循环条件 | `left <= right` | `left < right` |
| 目标在左侧 | `right = mid - 1` | `right = mid` |
| 区间为空 | `left > right` | `left == right` |
| 直观程度 | 高 | 中 |
| 每次排除 mid | 是 | 是 |

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(log n) — 每轮区间减半，至多 log₂(n) 轮 |
| 空间 | O(1) — 只用了三个变量 |

---

## 代码实现

### Java

```java
class Solution {
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }
}
```

**写法要点**：
- 循环条件 `left <= right` 而非 `<`，保证区间只有一个元素时仍进入循环
- `mid` 每次都被 `±1` 排除，不会死循环
- 终态 `left > right` 时返回 `-1`，无需额外判断

---

## 关键点总结

1. **有序是前提**：二分查找只适用于有序（或至少具备单调性）的数组——这里的「有序」不一定是整体有序，旋转数组的局部有序同样适用
2. **区间定义决定一切**：`[left, right]` 还是 `[left, right)` 决定了循环条件、mid 排除方式和终止条件的写法。选定一种就不要混用
3. **防溢出**：`mid = left + (right - left) / 2` 是防溢出标准写法；Java 可用 `mid = (left + right) >>> 1` 利用无符号右移
4. **每个分支必须移动指针**：`left = mid + 1` 或 `right = mid - 1`，漏掉 `±1` 会导致死循环
5. **变体题的本质**：所有二分变体（左边界、右边界、旋转数组）都只是调整 `== target` 时的行为——收缩左还是收缩右

---

## 延伸思考

此题是二分查找的基础模板，掌握后可延伸到：

| 题号 | 题目 | 变化点 |
|------|------|--------|
| #35 | 搜索插入位置 | `target` 不存在时返回应插入的位置 |
| #69 | x 的平方根 | 在整数域上二分，逼近 sqrt |
| #34 | 在排序数组中查找元素的第一个和最后一个位置 | 左边界 + 右边界的变体 |
| #33 | 搜索旋转排序数组 | 「整体无序但局部有序」的二段性 |
| #153 | 寻找旋转排序数组中的最小值 | 比较 nums[mid] 与 nums[right] |
| #74 | 搜索二维矩阵 | 将二维索引映射到一维再二分 |
| #162 | 寻找峰值 | 无序数组上的「爬坡式」二分 |
