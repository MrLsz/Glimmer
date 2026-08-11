# LeetCode 56 - Merge Intervals（合并区间）

> 合并重叠区间是排序 + 贪心的经典模板题——先按左端点排序，再线性扫描合并。本文按模板规范拆解：题目描述 → 解题思路 → 代码实现 → 关键点总结 → 延伸思考。

| 项目 | 内容 |
|------|------|
| 难度 | Medium |
| 链接 | https://leetcode.cn/problems/merge-intervals/ |
| 类别 | 排序 + 区间合并 |
| 关联题目 | #57 Insert Interval, #252 Meeting Rooms, #253 Meeting Rooms II, #435 Non-overlapping Intervals |

---

## 题目描述

给定一个区间数组 `intervals`，其中 `intervals[i] = [start_i, end_i]`，合并所有重叠的区间，返回一个不重叠的区间数组。

```
示例 1:
输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
输出: [[1,6],[8,10],[15,18]]
解释: [1,3] 和 [2,6] 重叠 → 合并为 [1,6]

示例 2:
输入: intervals = [[1,4],[4,5]]
输出: [[1,5]]
解释: [1,4] 和 [4,5] 相切（4 == 4）也视为重叠
```

约束：`1 <= intervals.length <= 10^4`，`0 <= start_i <= end_i <= 10^4`

---

## 解题思路

核心思想只有两步：**先排序，再贪心合并**。

### 排序策略

按左端点升序排列，左端点相同时按右端点升序。排序后得到一个关键性质：**任意两个区间如果有重叠，它们在数组中的顺序一定是相邻的**（因为左端点有序）。

```text
排序前: [[1,3],[8,10],[2,6],[15,18]]
排序后: [[1,3],[2,6],[8,10],[15,18]]
                      ↑
              [1,3] 和 [2,6] 重叠，且相邻
```

### 合并策略

维护当前合并区间 `[startValue, endValue]`，遍历排序后的区间：

- 若 `当前区间[0] <= endValue`（有重叠）→ `endValue = max(endValue, 当前区间[1])`
- 若 `当前区间[0] > endValue`（无重叠）→ 将 `[startValue, endValue]` 加入结果，更新为新区间
- 遍历结束后把最后一个区间加入结果

```text
遍历推演（示例 1）:

初始: startValue=1, endValue=3, resultList=[]
遍历 [2,6]: 2 <= 3 有重叠 → endValue = max(3,6) = 6
遍历 [8,10]: 8 > 6 无重叠 → 加入 [1,6], 更新 start=8, end=10
遍历 [15,18]: 15 > 10 无重叠 → 加入 [8,10], 更新 start=15, end=18
收尾: 加入 [15,18]

结果: [[1,6],[8,10],[15,18]]
```

### 复杂度分析

- **时间**：`O(N log N)`——排序占主导，线性扫描 `O(N)`
- **空间**：`O(N)`——存储结果列表（不计排序的栈空间）

---

## 代码实现

```java
class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals == null || intervals.length <= 1) {
            return intervals;
        }

        // ① 按左端点升序，相同时按右端点
        Arrays.sort(intervals, (a, b) ->
            a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]
        );

        // ② 遍历合并
        List<int[]> res = new ArrayList<>();
        int[] cur = intervals[0];                        // 当前合并区间

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= cur[1]) {             // 有重叠
                cur[1] = Math.max(cur[1], intervals[i][1]);
            } else {                                     // 无重叠：收口 + 起新
                res.add(cur);
                cur = intervals[i];
            }
        }
        res.add(cur);                                    // ③ 最后一个区间收口

        return res.toArray(new int[0][]);
    }
}
```

> **优化要点**：
> - 排序 lambda 用三元表达式一行搞定，省略了 `if-else` 展开
> - 用 `int[] cur` 直接持有区间引用，少两个 `startValue/endValue` 局部变量，并且无重叠时 `cur = intervals[i]` 就完成了「更新为新区间」
> - `toArray(new int[0][])` 比 `new int[size][]` 更简洁（JVM 会自行创建正确大小的数组）
> - 对比用户原始代码：省去了 `List<List<Integer>>` 的拆装箱开销和最后手动填充二维数组的 `for` 循环

---

## 关键点总结

1. **排序是前提**：按左端点排序后，重叠区间必然相邻，这是 O(N) 扫描的基础
2. **`intervals[i][0] <= endValue`** 是重叠判断的核心条件——`<=` 覆盖了端点相接的情况（如 `[1,4]` 和 `[4,5]`）
3. **用 `Math.max` 扩展右边界**：防止被包含区间（如 `[1,10]`、`[2,5]`）拉低右边界
4. **收尾别遗漏**：循环结束后最后一个合并区间必须手动加入结果

---

## 延伸思考

| 题目 | 关联点 |
|------|--------|
| #57 Insert Interval | 给定已排序不重叠的区间列表，插入新区间并合并——可以先插入再复用本题逻辑，也可以扫一遍处理 |
| #252 Meeting Rooms | 判断一个人能否参加所有会议——等价于检查是否存在重叠区间 |
| #253 Meeting Rooms II | 求最少需要多少个会议室——转为「同时进行的最大重叠数」，用差分数组或最小堆 |
| #435 Non-overlapping Intervals | 求移除最少区间使剩余不重叠——贪心选右端点最小的区间 |
| #1288 Remove Covered Intervals | 删除被其他区间完全覆盖的区间——排序策略不同（左端点升序、右端点降序） |
