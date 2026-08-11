# LeetCode 344 - Reverse String（反转字符串）

> 反转字符串是双指针的最基础模板——左右指针向中间靠拢逐位交换，O(1) 额外空间原地完成。掌握这道题后再做 #541 反转字符串 II、#151 翻转字符串里的单词就水到渠成。

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/reverse-string/ |
| 类别 | 双指针 |
| 关联题目 | #541 Reverse String II, #557 Reverse Words in a String III, #151 Reverse Words in a String, #345 Reverse Vowels of a String |

---

## 题目描述

编写一个函数，将输入的字符数组 `s` 原地反转，要求 O(1) 额外空间。

```
示例 1:
输入: s = ['h','e','l','l','o']
输出: ['o','l','l','e','h']

示例 2:
输入: s = ['H','a','n','n','a','h']
输出: ['h','a','n','n','a','H']
```

约束：`1 <= s.length <= 10^5`

---

## 解题思路

双指针相向而行，逐位交换——左指针 `i` 从 0 向右，右指针 `j` 从末尾向左，`i < j` 时交换并移动，相遇即结束。

```text
s = ['h','e','l','l','o']

i=0, j=4: h↔o → ['o','e','l','l','h']
i=1, j=3: e↔l → ['o','l','l','e','h']
i=2, j=2: i>=j → 结束

结果: ['o','l','l','e','h']
```

### 复杂度分析

- **时间**：`O(N)`——每个字符只访问一次
- **空间**：`O(1)`——只用一个 temp 变量

---

## 代码实现

```java
class Solution {
    public void reverseString(char[] s) {
        if (s == null || s.length <= 1) {
            return;
        }

        int i = 0, j = s.length - 1;
        while (i < j) {
            char tmp = s[i];
            s[i] = s[j];
            s[j] = tmp;
            i++;
            j--;
        }
    }
}
```

> **优化要点**：
> - `i` / `j` 取代 `beginIndex` / `endIndex`，简化为双指针通用命名
> - `i < j` 作为循环条件——当长度为奇数时中间元素无需交换，自然终止
> - 原地操作不返回新数组，符合题目 O(1) 需求

---

## 关键点总结

1. **双指针模板**：`while (i < j)` 交换 `s[i]` 和 `s[j]`，是反转类问题的最简形式
2. **奇偶通用**：`i < j` 天然覆盖了奇数和偶数长度——奇数时中间元素不处理，偶数时恰好全部交换完
3. **O(1) 空间**：只有一个 `tmp` 变量，不依赖任何额外数组
4. **边界保护**：`null` 和 `length <= 1` 直接返回，避免空指针和无效操作

---

## 延伸思考

| 题目 | 关联点 |
|------|--------|
| #541 Reverse String II | 每 2k 个字符反转前 k 个——双指针分段应用 |
| #557 Reverse Words in a String III | 逐词反转而不是整个字符串——先定位单词边界，再对每个单词双指针 |
| #151 Reverse Words in a String | 整体反转 + 逐词反转——两次双指针配合 |
| #345 Reverse Vowels of a String | 只反转元音字母——双指针跳过非目标字符 |
