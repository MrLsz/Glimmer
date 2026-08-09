# LeetCode 20 - Valid Parentheses（有效的括号）

| 项目 | 内容 |
|------|------|
| 难度 | Easy |
| 链接 | https://leetcode.cn/problems/valid-parentheses/ |
| 类别 | 栈 |
| 关联题目 | #22 Generate Parentheses, #32 Longest Valid Parentheses, #301 Remove Invalid Parentheses |

---

## 题目描述

给定一个只包含 `'('`、`')'`、`'{'`、`'}'`、`'['`、`']'` 的字符串 `s`，判断字符串是否有效。

有效字符串需满足：
1. 左括号必须用相同类型的右括号闭合
2. 左括号必须以正确的顺序闭合
3. 每个右括号都有一个对应的相同类型的左括号

### 示例

```
输入：s = "()"
输出：true

输入：s = "()[]{}"
输出：true

输入：s = "(]"
输出：false

输入：s = "([)]"
输出：false

输入：s = "{[]}"
输出：true
```

### 约束

- `1 <= s.length <= 10^4`
- `s` 仅由括号字符 `'('`、`')'`、`'{'`、`'}'`、`'['`、`']'` 组成

---

## 解题思路

### 核心思想：栈的经典应用

括号匹配问题的本质是 **后进先出（LIFO）** 模式——最近遇到的左括号，必须最先被匹配。这恰好与栈的特性完美契合。

**思路流程：**

1. 遍历字符串的每个字符 `c`
2. 如果 `c` 是左括号 `'('`、`'{'`、`'['`，将其压入栈中
3. 如果 `c` 是右括号 `')'`、`'}'`、`']'`：
   - 若栈为空，说明没有对应的左括号，返回 `false`
   - 取出栈顶元素，检查是否与当前右括号匹配。若不匹配，返回 `false`
4. 遍历结束后，若栈为空则全部匹配成功，返回 `true`；否则有多余的左括号未闭合，返回 `false`

### 括号匹配判断

使用 HashMap 建立右括号到左括号的映射关系，便于快速判断：

```
')' → '('
'}' → '{'
']' → '['
```

### 复杂度分析

| 维度 | 复杂度 |
|------|--------|
| 时间 | O(n) — 遍历字符串一次，每个字符最多入栈、出栈各一次 |
| 空间 | O(n) — 最坏情况下全是左括号，栈大小等于字符串长度 |

---

## 代码实现

### Java

```java
import java.util.*;

class Solution {
    private static final Map<Character, Character> BRACKET_PAIRS = new HashMap<>();

    static {
        BRACKET_PAIRS.put(')', '(');
        BRACKET_PAIRS.put('}', '{');
        BRACKET_PAIRS.put(']', '[');
    }

    public boolean isValid(String s) {
        // 特判：长度为奇数无法完全匹配
        if (s.length() % 2 != 0) {
            return false;
        }

        Deque<Character> stack = new ArrayDeque<>();

        for (char bracket : s.toCharArray()) {
            Character expectedLeft = BRACKET_PAIRS.get(bracket);
            if (expectedLeft != null) {
                // 右括号：栈顶必须匹配
                if (stack.isEmpty() || stack.peek() != expectedLeft) {
                    return false;
                }
                stack.pop();
            } else {
                // 左括号：压入栈
                stack.push(bracket);
            }
        }

        return stack.isEmpty();
    }
}
```

---

## 关键点总结

1. **后进先出原则**：括号匹配天然满足栈的 LIFO 特性——最内层的左括号最先被闭合
2. **奇偶优化**：字符串长度为奇数时，一定不匹配，可提前返回 `false`
3. **映射表**：右括号到左括号的映射避免冗长的 `if-else` 判断
4. **Java 栈选择**：使用 `ArrayDeque` 而非 `Stack` 类（`Stack` 是遗留类，性能较差）

---

## 延伸思考

此题是多类括号匹配问题的起点，可延伸至：

- **#22 Generate Parentheses**：生成所有可能的有效括号组合（回溯）
- **#32 Longest Valid Parentheses**：求最长有效括号子串长度（动态规划 / 栈）
- **#301 Remove Invalid Parentheses**：删除最少括号使字符串有效（BFS / DFS）
