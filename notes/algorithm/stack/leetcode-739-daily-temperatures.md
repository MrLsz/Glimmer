# LeetCode 739 - Daily Temperatures（每日温度）

> 每日温度是单调栈的入门模板题——栈中维护「尚未找到更高温度」的下标并按温度递减排列，每次遇到更高温度就批量出栈结算。掌握这道题后再做 #496 下一个更大元素 I、#503 下一个更大元素 II 水到渠成。

| 项目 | 内容 |
|------|------|
| 难度 | Medium |
| 链接 | https://leetcode.cn/problems/daily-temperatures/ |
| 类别 | 单调栈 |
| 关联题目 | #496 Next Greater Element I, #503 Next Greater Element II, #42 Trapping Rain Water, #84 Largest Rectangle in Histogram |

---

## 题目描述

给定一个整数数组 `temperatures` 表示每天的温度，返回数组 `answer`，其中 `answer[i]` 表示第 i 天之后需要等待多少天才会有更高的温度。若之后没有更高温度，则 `answer[i] = 0`。

```
示例 1:
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]

示例 2:
输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]

示例 3:
输入: temperatures = [30,60,90]
输出: [1,1,0]
```

约束：`1 <= temperatures.length <= 10^5`，`30 <= temperatures[i] <= 100`

---

## 解题思路

暴力解法是每个元素向后扫描直到找到更高温度——O(N²) 不可接受。单调栈将时间复杂度压到 O(N)。

### 单调栈策略

维护一个**单调递减栈**（栈底到栈顶温度递减），栈中存的是**下标**而不是温度值。遍历每一天：

- 当前温度 **≤** 栈顶温度 → 入栈（等待更高温度）
- 当前温度 **>** 栈顶温度 → 栈顶元素找到了答案，出栈并结算 `res[oldIndex] = index - oldIndex`，继续检查新的栈顶

```text
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

index=0, t=73: 栈空 → 入栈 [0]
index=1, t=74: 74 > t[栈顶0]=73 → 弹出0, res[0]=1-0=1 → 入栈 [1]
index=2, t=75: 75 > t[栈顶1]=74 → 弹出1, res[1]=2-1=1 → 入栈 [2]
index=3, t=71: 71 < t[栈顶2]=75 → 入栈 [2,3]
index=4, t=69: 69 < t[栈顶3]=71 → 入栈 [2,3,4]
index=5, t=72: 72 > t[栈顶4]=69 → 弹出4, res[4]=5-4=1
               72 > t[栈顶3]=71 → 弹出3, res[3]=5-3=2
               72 < t[栈顶2]=75 → 入栈 [2,5]
index=6, t=76: 76 > t[栈顶5]=72 → 弹出5, res[5]=6-5=1
               76 > t[栈顶2]=75 → 弹出2, res[2]=6-2=4
               栈空 → 入栈 [6]
index=7, t=73: 73 < t[栈顶6]=76 → 入栈 [6,7]

遍历结束，栈中剩余 [6,7] 均未找到更高温度 → res[6]=0, res[7]=0
结果: [1,1,4,2,1,1,0,0]
```

### 复杂度分析

- **时间**：`O(N)`——每个元素最多入栈一次、出栈一次
- **空间**：`O(N)`——最坏情况下栈中存所有元素（递减序列如 `[90,80,70]`）

---

## 代码实现

```java
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        if (temperatures == null) {
            return null;
        }

        int[] res = new int[temperatures.length];
        Deque<Integer> stack = new ArrayDeque<>();   // 存下标，单调递减栈

        for (int i = 0; i < temperatures.length; i++) {
            // 当前温度 > 栈顶温度 → 栈顶元素找到答案，批量出栈
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prevIndex = stack.pop();
                res[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        // 栈中剩余元素自动为 0（int 数组默认值）
        return res;
    }
}
```

> **优化要点**：
> - 删除空栈判断的分支——`while` 条件中的 `!stack.isEmpty()` 已经覆盖，`continue` 是多余的。栈空时直接跳过 while 执行 `push`，逻辑完全一致
> - 删除末尾的 while 清零循环——`int[]` 默认值就是 0，栈中剩余元素不需要额外处理
> - `res` / `stack` / `prevIndex` 取代冗长命名，保持双指针/栈类题解的一致风格

---

## 关键点总结

1. **栈中存下标而不是值**：因为需要计算「等待天数」（下标差值），只存温度值无法求出距离
2. **单调递减栈维护「尚未找到更高温度」的候选**：栈中元素按温度递减排列，当前温度超栈顶时意味着栈顶找到了答案
3. **每个元素入栈一次、出栈一次**：均摊 O(1) 每元素，总体 O(N)
4. **int 数组默认值为 0**：未找到更高温度的元素不需要显式赋值，省去收尾循环

---

## 延伸思考

| 题目 | 关联点 |
|------|--------|
| #496 Next Greater Element I | 找下一个更大元素——单调栈找下一个更大值的基本模板 |
| #503 Next Greater Element II | 循环数组找下一个更大元素——遍历两遍或用 `i % n` 模拟 |
| #42 Trapping Rain Water | 接雨水——单调栈按层计算积水，栈中存递减高度 |
| #84 Largest Rectangle in Histogram | 柱状图最大矩形——单调栈找左右边界，与本题「找下一个更小」对称 |
