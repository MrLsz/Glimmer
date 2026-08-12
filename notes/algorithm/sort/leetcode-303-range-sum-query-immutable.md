# LeetCode 303 - Range Sum Query - Immutable（区域和检索 - 数组不可变）

> 前缀和的入门模板题——构造函数中计算前缀和数组，`sumRange` 用 `prefix[right] - prefix[left-1]` 实现 O(1) 查询。核心易错点：**减的是 left-1 而不是 left**。

| 项目   | 内容                                                                         |
| ---- | -------------------------------------------------------------------------- |
| 难度   | Easy                                                                       |
| 链接   | <https://leetcode.cn/problems/range-sum-query-immutable/>                  |
| 类别   | 前缀和                                                                        |
| 关联题目 | #304 Range Sum Query 2D, #560 Subarray Sum Equals K, #724 Find Pivot Index |

---

## 题目描述

给定整数数组 `nums`，实现 `NumArray` 类支持多次调用 `sumRange(left, right)` 返回 `[left, right]` 区间的元素和（左右闭区间）。

```
示例:
输入: NumArray([-2, 0, 3, -5, 2, -1])
sumRange(0, 2) → 1
sumRange(2, 5) → -1
sumRange(0, 5) → -3
```

约束：`1 <= nums.length <= 10^4`，`-10^5 <= nums[i] <= 10^5`，最多调用 `10^4` 次 `sumRange`

---

## 解题思路

前缀和的核心公式：

```
prefix[i] = nums[0] + ... + nums[i]          // 前缀和定义
sum(left, right) = prefix[right] - prefix[left - 1]   // 当 left > 0
                 = prefix[right]                       // 当 left == 0
```

### 常见错误

减 `prefix[left]` 而不是 `prefix[left - 1]`——相当于把 `nums[left]` 也减掉了：

```
nums = [1, 2, 3], prefix = [1, 3, 6]
sum(0, 2): 正确 = 6 - prefix[-1] = 6
          错误 = 6 - prefix[0] = 5  ← 多减了 nums[0]
sum(1, 2): 正确 = 6 - prefix[0] = 5
          错误 = 6 - prefix[1] = 3  ← 多减了 nums[1]
```

### 复杂度分析

- **构造**：`O(N)`——一次遍历计算前缀和
- **查询**：`O(1)`——直接数组下标访问
- **空间**：`O(N)`——前缀和数组

---

## 代码实现

```java
class NumArray {
    private int[] prefix;

    public NumArray(int[] nums) {
        prefix = new int[nums.length];
        int sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            prefix[i] = sum;
        }
    }

    public int sumRange(int left, int right) {
        return prefix[right] - (left > 0 ? prefix[left - 1] : 0);
        //                          ↑ 关键：减的是 left-1，不是 left
    }
}
```

---

## 关键点总结

1. **前缀和本质**：`prefix[i]` = 前 i+1 个元素的和，区间和 = 右端点前缀 - 左端前一位置前缀
2. **减 left-1** 不是 left——这是前缀和的最高频错误
3. **left == 0 边界**：三元表达式 `left > 0 ? prefix[left - 1] : 0` 一行处理
