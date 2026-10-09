# Python 基础语法

> Python 是一门解释型、动态类型、强类型的通用语言。它的设计哲学是「可读性优先」：用缩进代替花括号、用简洁的内置结构（list/dict/set/推导式）压缩样板代码。本篇按「对象模型 → 类型与字面量 → 序列 → 映射与集合 → 流程控制 → 函数 → 类 → 异常 → 模块包 → 迭代器生成器 → 上下文管理器 → 内存管理」的顺序铺开纯语法，重点是 Java/Swift 开发者最容易踩的差异：动态类型、可变与不可变、参数传递语义、深浅拷贝、装饰器、生成器。已经会写 Python 的读者可以直接跳第 13 章内存管理，那里解释了很多人「代码能跑但行为奇怪」的根源。

## 目录

- [1. Python 概述](#1-python-概述)
  - [1.1 语言定位与设计哲学](#11-语言定位与设计哲学)
  - [1.2 解释执行与 CPython](#12-解释执行与-cpython)
  - [1.3 动态类型 vs 静态类型](#13-动态类型-vs-静态类型)
- [2. 一切皆对象](#2-一切皆对象)
  - [2.1 对象、类型与 id](#21-对象类型与-id)
  - [2.2 可变对象 vs 不可变对象](#22-可变对象-vs-不可变对象)
  - [2.3 赋值、浅拷贝、深拷贝](#23-赋值浅拷贝深拷贝)
- [3. 基础类型与字面量](#3-基础类型与字面量)
  - [3.1 数值：int / float / bool / complex](#31-数值int--float--bool--complex)
  - [3.2 字符串 str](#32-字符串-str)
  - [3.3 None](#33-none)
- [4. 序列类型](#4-序列类型)
  - [4.1 list](#41-list)
  - [4.2 tuple](#42-tuple)
  - [4.3 str 也是序列](#43-str-也是序列)
  - [4.4 range](#44-range)
  - [4.5 切片 slicing](#45-切片-slicing)
  - [4.6 序列通用操作](#46-序列通用操作)
- [5. 映射与集合](#5-映射与集合)
  - [5.1 dict](#51-dict)
  - [5.2 set / frozenset](#52-set--frozenset)
  - [5.3 推导式](#53-推导式)
- [6. 运算符与流程控制](#6-运算符与流程控制)
  - [6.1 运算符](#61-运算符)
  - [6.2 条件与三元表达式](#62-条件与三元表达式)
  - [6.3 循环 for / while 与 else 子句](#63-循环-for--while-与-else-子句)
- [7. 函数](#7-函数)
  - [7.1 定义与参数](#71-定义与参数)
  - [7.2 可变默认参数陷阱](#72-可变默认参数陷阱)
  - [7.3 lambda 与高阶函数](#73-lambda-与高阶函数)
  - [7.4 作用域 LEGB 与 global / nonlocal](#74-作用域-legb-与-global--nonlocal)
  - [7.5 闭包](#75-闭包)
  - [7.6 装饰器 decorator](#76-装饰器-decorator)
- [8. 类与面向对象](#8-类与面向对象)
  - [8.1 类定义、self 与 __init__](#81-类定义self-与-__init__)
  - [8.2 实例属性 vs 类属性](#82-实例属性-vs-类属性)
  - [8.3 访问控制的约定](#83-访问控制的约定)
  - [8.4 继承、多继承与 MRO](#84-继承多继承与-mro)
  - [8.5 魔术方法](#85-魔术方法)
  - [8.6 property、classmethod、staticmethod](#86-propertyclassmethodstaticmethod)
  - [8.7 __slots__](#87-__slots__)
  - [8.8 dataclass](#88-dataclass)
- [9. 异常处理](#9-异常处理)
  - [9.1 异常模型与 try / except / else / finally](#91-异常模型与-try--except--else--finally)
  - [9.2 raise 与自定义异常](#92-raise-与自定义异常)
  - [9.3 常见内置异常](#93-常见内置异常)
- [10. 模块与包](#10-模块与包)
  - [10.1 import 机制与搜索路径](#101-import-机制与搜索路径)
  - [10.2 from / import / as / 星号](#102-from--import--as--星号)
  - [10.3 包与 __init__.py](#103-包与-__init__py)
  - [10.4 __name__ 与 main](#104-__name__-与-main)
- [11. 迭代器与生成器](#11-迭代器与生成器)
  - [11.1 可迭代对象与迭代器](#111-可迭代对象与迭代器)
  - [11.2 生成器与 yield](#112-生成器与-yield)
  - [11.3 生成器表达式](#113-生成器表达式)
  - [11.4 惰性求值的意义](#114-惰性求值的意义)
- [12. 上下文管理器](#12-上下文管理器)
  - [12.1 with 语句](#121-with-语句)
  - [12.2 自定义上下文管理器](#122-自定义上下文管理器)
  - [12.3 contextlib](#123-contextlib)
- [13. 内存管理](#13-内存管理)
  - [13.1 引用计数](#131-引用计数)
  - [13.2 垃圾回收与循环引用](#132-垃圾回收与循环引用)
  - [13.3 小整数池与字符串驻留](#133-小整数池与字符串驻留)
  - [13.4 常见内存陷阱](#134-常见内存陷阱)
- [附：高频速记](#附高频速记)

---

# 1. Python 概述

## 1.1 语言定位与设计哲学

Python 由 Guido van Rossum 于 1991 年发布，定位是一门「让代码读起来接近伪代码」的通用语言，同时覆盖脚本、后端、数据科学、机器学习、运维自动化多个领域。它最鲜明的特征是强制缩进——代码块不靠 `{}` 或 `begin/end` 界定，而靠缩进层级。

```python
def greet(name):
    if name:
        return f"hello {name}"
    return "hello world"
```

这种设计牺牲了「自由排版」，换来的是「结构一眼可见」：任何人读到的缩进结构就是真实的执行结构，不存在「花括号和缩进打架」的情况。副作用是混用空格和 Tab 会直接报 `IndentationError`，所以 Python 社区约定统一用 4 个空格缩进（PEP 8）。

几个贯穿全文的核心事实，先立起来：

| 事实 | 含义 | 对 Java/Swift 开发者意味着什么 |
| ---- | ---- | ---- |
| 动态类型 | 变量没有固定类型，类型跟对象走 | 没有编译期类型检查，错误要运行期才暴露 |
| 强类型 | 不会隐式做危险的类型转换 | `"1" + 1` 会报 TypeError，不像 JS 拼成 `"11"` |
| 一切皆对象 | 整数、字符串、函数、类、模块都是对象 | 可以把函数当参数传、把类当值赋给变量 |
| 引用语义 | 变量只是「指向对象的标签」 | 赋值不复制对象，改的是同一个对象 |

## 1.2 解释执行与 CPython

CPython 是 Python 的参考实现，运行流程是「源码 → 字节码 → 虚拟机执行」，和 Java 的「源码 → 字节码 → JVM」很像，但有本质区别：

```text
Python:  .py 源码 ──编译──> .pyc 字节码 ──解释──> PVM (Python 虚拟机)
Java:    .java 源码 ──编译──> .class 字节码 ──JIT──> JVM
```

区别在于：

- Python 的「编译」发生在运行时，且默认无类型信息，字节码层面的优化空间远小于 Java。Java 的 JIT 可以做激进的内联和逃逸分析，CPython 的解释器基本是逐条解释字节码。
- 也因此，CPython 用全局解释器锁（GIL，Global Interpreter Lock）保证同一时刻只有一个线程执行 Python 字节码——多线程在 CPU 密集任务上拿不到性能提升，这是 Python 并发模型绕不开的话题（并发详细内容另见多线程篇）。

常用的其他实现：PyPy（JIT，快）、Jython（跑在 JVM 上）、MicroPython（嵌入式）、Cython（编译成 C 扩展）。

## 1.3 动态类型 vs 静态类型

Python 里变量名本身不携带类型，类型属于对象：

```python
x = 42        # x 此时指向 int 对象 42
x = "hello"   # 合法，x 重新指向 str 对象
```

对比 Java，变量声明时类型就锁死了：

```java
int x = 42;   // x 永远只能是 int
```

动态类型带来两点直接影响：

1. 写起来快、重构和读代码时成本高——没有编译器帮你抓「传错类型」的错误，要靠单元测试和类型注解补位。
2. Python 3.5 起引入类型注解（type hints）作为「可选补充」，配合 mypy 等工具做静态检查，但注解不改变运行期行为：

```python
def add(a: int, b: int) -> int:
    return a + b

add(1, "2")   # 运行期不会报错（除非代码内部抛），类型注解只是提示
```

> 易错点：类型注解默认不强制，`add(1, "2")` 若内部是 `a + b` 会抛 `TypeError`，但那是运行期的 `+` 抛的，不是注解在拦。想让注解生效要接 mypy / pyright 这类检查器。

---

# 2. 一切皆对象

## 2.1 对象、类型与 id

Python 里所有值都是对象，每个对象有三个基本属性：

- 身份（identity）：由内置函数 `id(obj)` 返回，是对象在生命周期内唯一的内存地址标识，相当于 Java 里的引用地址。
- 类型（type）：由 `type(obj)` 返回，且类型本身也是对象（`type(int)` 是 `type`）。
- 值（value）：对象实际存储的数据。

```python
x = 10
id(x)        # 例如 4312306704
type(x)      # <class 'int'>
```

`is` 运算符比较的是身份（是不是同一个对象），`==` 比较的是值（内容相不相等）。这是 Python 最经典的坑之一：

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True，内容相同
a is b   # False，不是同一个对象
```

> 面试常考：`==` 由对象的 `__eq__` 方法决定，`is` 永远比较 `id`。判断「是否 None」必须用 `x is None` 而不是 `x == None`，因为前者是身份比较、速度最快且不会被 `__eq__` 重写干扰。

## 2.2 可变对象 vs 不可变对象

这是 Python 与 Java/Swift 差异最大、也是最容易出错的地方。对象的「可变性」决定了它能不能被原地修改：

| 类别 | 类型 | 能否原地修改 |
| ---- | ---- | ---- |
| 不可变（immutable） | int、float、bool、str、tuple、frozenset、None | 否，任何「修改」都产生新对象 |
| 可变（mutable） | list、dict、set、bytearray、自定义类实例 | 是，可以原地改 |

不可变对象不是「不能变」，而是「变 = 造新对象」。看这个反直觉的例子：

```python
x = 1000
y = x
x += 1
print(x, y)   # 1001 1000，x 变了 y 没变，因为 int 不可变，x += 1 是 x = x + 1

a = [1, 2]
b = a
a.append(3)
print(a, b)   # [1, 2, 3] [1, 2, 3]，a 和 b 指向同一个 list，原地修改双方可见
```

第一段里 `x += 1` 本质是「算出 1001 这个新 int，把标签 x 贴过去」，原来的 1000 对象还在，y 还指着它。第二段里 `a.append(3)` 是原地修改 list 对象本身，b 指向同一个对象，所以也看到了。

这引出一个关键区分——参数传递语义。Python 官方说法是「按引用传递」还是「按值传递」都不准确，准确说法是「按对象引用传递」（pass by object reference），也叫「按共享传递」（call by sharing）：

```python
def f(lst, n):
    lst.append(4)   # lst 指向的 list 被原地修改，调用方可见
    n += 1          # n += 1 让 n 指向新的 int，调用方不可见

arr = [1, 2, 3]
num = 10
f(arr, num)
print(arr, num)   # [1, 2, 3, 4] 10
```

> 结论：函数参数传入后，可变对象在函数内被原地修改会影响调用方；不可变对象的「修改」只是重新绑定，不影响调用方。这正是 Java 里「基本类型传值、对象传引用」在 Python 里的对应物，只不过 Python 的 int 也是对象。

## 2.3 赋值、浅拷贝、深拷贝

既然变量是「标签」，`=` 赋值永远不会复制对象，只是多贴一个标签。真要复制要用 `copy` 模块：

```python
import copy

a = [[1, 2], [3, 4]]

b = a              # 赋值：b 和 a 是同一个对象
c = a[:]           # 浅拷贝：新外层 list，内层还是共享
d = copy.copy(a)   # 浅拷贝：等价于 a[:] 或 list(a)
e = copy.deepcopy(a)  # 深拷贝：连内层一起复制

a[0][0] = 99
print(b[0][0], c[0][0], d[0][0], e[0][0])  # 99 99 99 1
```

用图表示三者的区别：

```text
a  ──> [[1,2],[3,4]]         原始对象
b  ──> 同一个对象             赋值：只加标签
c  ──> [ ● , ● ]             浅拷贝：外层新，内层两个 ● 还指向原 [1,2]/[3,4]
        └──┘└──┘
e  ──> [[1,2],[3,4]]         深拷贝：里外全新
```

浅拷贝只复制最外层容器，内层元素仍然是原对象的引用；深拷贝递归复制所有层级。对只含不可变元素的扁平 list，浅拷贝足够；一旦嵌套了可变对象，就要想清楚要不要深拷贝。

> 易错点：`list.copy()`、`a[:]`、`list(a)`、`copy.copy(a)` 都是浅拷贝，不是深拷贝。多层嵌套且要完全隔离时，必须 `copy.deepcopy`。

---

# 3. 基础类型与字面量

## 3.1 数值：int / float / bool / complex

Python 的整数是任意精度的，不存在 int 溢出：

```python
big = 10 ** 100       # 1 后面 100 个 0，Java 的 long 早就溢出了
type(big)             # <class 'int'>
```

浮点数是 IEEE 754 双精度，和 Java 的 double 一样，存在精度问题：

```python
0.1 + 0.2             # 0.30000000000000004
```

数值字面量支持多种进制和下划线分隔：

```python
0b1010       # 二进制，10
0o17         # 八进制，15
0x1F         # 十六进制，31
1_000_000    # 下划线只是可读性分隔，值等于 1000000
```

bool 是 int 的子类，`True == 1`、`False == 0` 都成立，这是从 C 继承来的历史包袱：

```python
isinstance(True, int)   # True
True + 1                # 2
```

complex 用于复数，工程里不常用，知道 `3 + 4j` 这种字面量即可。

## 3.2 字符串 str

str 是不可变的 Unicode 字符串。Python 3 里 str 存的是 Unicode 码点，与底层字节严格分离——字节要单独用 `bytes` 表示，两者互转靠 `encode` / `decode`，这是处理中文、网络传输、文件 IO 时绕不开的一对方法：

```python
s = "中文"
b = s.encode("utf-8")   # str -> bytes
b.decode("utf-8")       # bytes -> str
```

字符串支持 `+` 拼接、`*` 重复、`in` 成员判断、`len()` 长度、以及丰富的 `str` 方法。格式化推荐用 f-string（3.6+），可读性和性能都最好：

```python
name, age = "Tom", 18
f"{name} is {age} years old"       # 直接内插
f"{age:0>4d}"                       # 格式化：左侧补零到 4 位 -> '0018'
f"{3.14159:.2f}"                    # 保留两位小数 -> '3.14'
```

三种旧式格式化（`%` 格式化、`str.format`、f-string）里 f-string 唯一推荐，前两种基本只在看老代码时遇到。

> 易错点：`+` 拼接在循环里是 O(n²)——每次 `+` 都产生新的不可变 str 对象，累积复制。大量拼接要用 `''.join(list_of_str)`。

## 3.3 None

None 是 Python 的「空值」，类型是 `NoneType`，整个程序里只有一个 None 单例，判断它用 `is`：

```python
x = None
x is None      # True，推荐写法
x == None      # 也能工作，但不推荐（可被 __eq__ 干扰）
```

函数没有 `return` 时默认返回 None，这也是很多「函数为什么返回 None」疑问的答案。

---

# 4. 序列类型

序列（sequence）是一类「有序、可下标访问」的数据结构，list、tuple、str、range 都算序列。它们共享切片、`in`、`len`、`+`、`*` 等操作。

## 4.1 list

list 是可变、可含任意类型元素的有序序列，是 Python 使用频率最高的容器：

```python
a = [1, 2, 3]
a.append(4)          # 末尾追加
a.insert(0, 0)       # 指定位置插入
a.pop()              # 弹出末尾元素并返回
a.remove(2)          # 删除第一个等于 2 的元素
a.extend([5, 6])     # 追加多个
a.index(3)           # 查找下标，找不到抛 ValueError
a.count(1)           # 计数
a.sort()             # 原地排序
sorted(a)            # 返回新排序列表，不改原列表
```

list 底层是动态数组，`append` 均摊 O(1)，但 `insert(0, x)` 是 O(n)（要把后面所有元素后移一位）。

## 4.2 tuple

tuple 是不可变序列，一旦创建就不能增删改元素：

```python
t = (1, 2, 3)
t = 1, 2, 3      # 等价，逗号才是 tuple 的标志，不是括号
t[0] = 9         # TypeError: 'tuple' object does not support item assignment
```

单元素 tuple 必须加尾逗号，否则会被当成普通括号表达式：

```python
(1)      # 这是 int 1，不是 tuple
(1,)     # 这才是单元素 tuple
```

tuple 不可变但可以「装」可变对象——不可变的是 tuple 自身（装了几个元素、指向谁），元素指向的对象照样可变：

```python
t = (1, [2, 3])
t[1].append(4)    # 合法，list 是可变对象
print(t)          # (1, [2, 3, 4])
```

所以 tuple 不能作为 dict 的 key 的前提是它「所有元素都不可变」。可哈希性（hashable）才是能不能当 key 的根本标准，见 5.1。

## 4.3 str 也是序列

字符串作为不可变字符序列，支持切片、`in`、`len`、`+`、`*`：

```python
s = "hello"
s[0]        # 'h'
s[1:3]      # 'el'
"ll" in s   # True
s * 2       # 'hellohello'
```

但 `s[0] = 'H'` 会报 TypeError——str 不可变，要改成 `s = 'H' + s[1:]`。

## 4.4 range

range 表示一个整数区间，常和 for 配合，且是惰性的（不真正生成所有数字）：

```python
range(5)          # 0 1 2 3 4
range(2, 5)       # 2 3 4
range(0, 10, 2)   # 0 2 4 6 8
list(range(3))    # [0, 1, 2]，需要实体 list 时才转
```

注意 range 的参数是 `start, stop, step`，左闭右开，`stop` 不包含在内，和切片语义一致。

## 4.5 切片 slicing

切片是 Python 最优雅的特性之一，语法 `seq[start:stop:step]`，三个参数都可省略：

```python
a = [0, 1, 2, 3, 4, 5]
a[1:4]       # [1, 2, 3]，左闭右开
a[:3]        # [0, 1, 2]，省略 start 从头
a[3:]        # [3, 4, 5]，省略 stop 到尾
a[:]         # 完整浅拷贝
a[::2]       # [0, 2, 4]，步长 2
a[::-1]      # [5, 4, 3, 2, 1, 0]，负步长 = 反转
```

切片对 str、tuple、list 通用，且对「可切片对象」返回同类新对象。负数索引从右往左数：

```python
a[-1]     # 5，最后一个
a[-3:]    # [3, 4, 5]，最后三个
```

> 易错点：切片越界不报错（`a[100:]` 返回空 list），但单下标越界会抛 IndexError。这是「切片宽容、索引严格」的规则。

## 4.6 序列通用操作

| 操作 | 示例 | 说明 |
| ---- | ---- | ---- |
| 下标 | `a[0]`、`a[-1]` | 越界抛 IndexError |
| 切片 | `a[1:3]` | 越界不报错 |
| 成员 | `x in a`、`x not in a` | 线性查找 O(n) |
| 长度 | `len(a)` | 内置函数，不是方法 |
| 拼接 | `a + b` | 产生新序列 |
| 重复 | `a * 3` | 产生新序列 |
| 遍历下标 | `enumerate(a)` | 返回 (下标, 元素) |
| 并行遍历 | `zip(a, b)` | 按最短序列配对 |
| 求最值 | `min(a)`、`max(a)` | 元素需可比较 |
| 求和 | `sum(a)` | 元素需是数值 |

`enumerate` 和 `zip` 是 Python 遍历的灵魂，代替了 Java 里手动维护下标：

```python
for i, v in enumerate(["a", "b", "c"]):
    print(i, v)          # 0 a / 1 b / 2 c

for x, y in zip([1, 2], ["a", "b"]):
    print(x, y)          # 1 a / 2 b
```

> 易错点：`a * 3` 对含可变元素的 list 是浅重复——`[[0]] * 3` 会得到三个指向同一个 `[0]` 的引用，改一个全变。需要独立元素用列表推导式 `[[0] for _ in range(3)]`。

---

# 5. 映射与集合

## 5.1 dict

dict 是 Python 的哈希表，键值对容器。键必须可哈希（hashable），值无限制：

```python
d = {"a": 1, "b": 2}
d["c"] = 3          # 增 / 改
d.get("x", 0)       # 取值，键不存在返回默认值 0，不抛异常
d["x"]              # 取值，键不存在抛 KeyError
d.setdefault("k", 0)  # 存在则返回，不存在则写入默认值
d.pop("a")          # 删除并返回值
"a" in d            # 判断键是否存在
d.keys() / d.values() / d.items()   # 返回视图，遍历用
```

`get` 和 `setdefault` 是避免 KeyError 的两个常用手法。遍历习惯：

```python
for k, v in d.items():
    print(k, v)
```

关于「可哈希」：只有不可变对象才默认可哈希，所以 list 不能当 key，tuple（全不可变元素）可以：

```python
{ (1, 2): "a" }    # 合法
{ [1, 2]: "a" }    # TypeError: unhashable type: 'list'
```

dict 在 Python 3.7+ 保证按插入顺序迭代（CPython 3.6 已实现，3.7 成为语言规范），但不要依赖它做「有序字典」的严谨语义，真要有序场景用 collections.OrderedDict 语义更明确。

## 5.2 set / frozenset

set 是无序、不重复的可变集合，基于哈希表，成员判断 O(1)（对比 list 的 O(n)）：

```python
s = {1, 2, 3}
s.add(4)
s.remove(2)        # 不存在抛 KeyError
s.discard(2)       # 不存在也不报错
s1 & s2            # 交集
s1 | s2            # 并集
s1 - s2            # 差集
s1 ^ s2            # 对称差集
```

set 元素同样要求可哈希。frozenset 是 set 的不可变版本，可哈希，能当 dict 的 key 或 set 的元素。set 最典型用途是去重和高效查找：

```python
len(set([1, 1, 2, 3, 3]))   # 3，去重
```

> 易错点：`{}` 是空 dict 不是空 set，空 set 要写 `set()`。这个陷阱源自历史兼容。

## 5.3 推导式

推导式（comprehension）是 Python 的招牌语法，用一行表达式构建容器，且通常比等价的 for 循环更快：

```python
# 列表推导式
[x * 2 for x in range(5)]              # [0, 2, 4, 6, 8]
[x for x in range(10) if x % 2 == 0]   # [0, 2, 4, 6, 8]，带过滤条件
[x if x % 2 == 0 else -x for x in range(5)]  # [0, -1, 2, -3, 4]，带三元

# 字典推导式
{k: v * 2 for k, v in {"a": 1}.items()}  # {'a': 2}

# 集合推导式
{x % 3 for x in range(10)}              # {0, 1, 2}
```

注意「过滤」用 `if` 放末尾，「变换」用三元放前面，两者别混。生成器表达式（用圆括号）见第 11 章，它是推导式的惰性版本。

---

# 6. 运算符与流程控制

## 6.1 运算符

Python 运算符大部分和 C/Java 一致，差异点要记住：

| 类别 | 运算符 | 备注 |
| ---- | ---- | ---- |
| 算术 | `+ - * / // % **` | `/` 是真正除法（3/2=1.5），`//` 是整除，`**` 是幂 |
| 比较 | `== != < > <= >=` | 支持链式比较 `1 < x < 10` |
| 逻辑 | `and or not` | 单词而非 `&& || !`，返回的是操作数本身不是 bool |
| 成员 | `in not in` | 判断是否在容器中 |
| 身份 | `is is not` | 比较对象身份（id） |
| 位运算 | `& | ^ ~ << >>` | 和 Java 一致 |

两个独有且高频的行为：

链式比较：

```python
x = 5
1 < x < 10    # True，等价于 1 < x and x < 10，且 x 只求值一次
```

逻辑运算符的短路与「返回值」——`and`/`or` 返回决定结果的那个操作数，而不是布尔值：

```python
a = 0 or "default"      # "default"，0 是假值，返回后者
b = "x" and "y"         # "y"，都为真，返回后者
c = None or [] or "z"   # "z"
```

这个特性常被用来做「给变量设默认值」：`name = user_input or "anonymous"`。但要小心 0、空串、空 list 都是「假值」（falsy），它们会被 `or` 跳过，这是把 `or` 当默认值工具时的经典坑。

> 易错点：Python 的假值有 `None`、`False`、`0`、`0.0`、`""`、`[]`、`{}`、`set()`。判断「是否有值」和判断「是否为 None」是两回事，前者 `if x:` 会把 0 也当成假，后者必须 `if x is None:`。

## 6.2 条件与三元表达式

```python
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")
```

三元表达式是 `a if cond else b`，顺序和 C 系相反（条件放中间）：

```python
sign = "positive" if x > 0 else "non-positive"
```

Python 3.10+ 还引入了结构化模式匹配 `match`，类似 switch 但更强：

```python
match x:
    case 0:
        print("zero")
    case 1 | 2:
        print("one or two")
    case str(s) if len(s) > 1:
        print("long string", s)
    case _:
        print("other")
```

## 6.3 循环 for / while 与 else 子句

for 直接遍历可迭代对象，不用下标：

```python
for item in [1, 2, 3]:
    print(item)
```

while 和 C 系一致，配合 `break` / `continue`。Python 独有的特性是循环可以带 `else` 子句——循环**没有被 break 打断**时才执行 else：

```python
for n in range(2, 10):
    for d in range(2, n):
        if n % d == 0:
            break
    else:
        print(n, "是质数")   # 内层 for 完整跑完没 break，说明没因子
```

> 易错点：循环的 `else` 不是「循环结束后执行」，而是「没被 break 时执行」。语义和直觉相反，阅读时当成 `no break` 理解。这个特性争议很大，很多团队干脆不用。

---

# 7. 函数

## 7.1 定义与参数

函数用 `def` 定义，参数分四类：位置参数、默认参数、可变位置参数、可变关键字参数：

```python
def f(a, b, c=0, *args, **kwargs):
    pass
```

- `a, b`：位置参数（必需）
- `c=0`：默认参数
- `*args`：把多余的位置参数打包成 tuple
- `**kwargs`：把多余的关键字参数打包成 dict

调用时可以按位置或关键字传参：

```python
def greet(name, greeting="hello"):
    return f"{greeting}, {name}"

greet("Tom")                    # 位置
greet(name="Tom", greeting="hi")  # 关键字
```

`*` 和 `**` 在调用侧是「解包」作用，和定义侧相反：

```python
nums = [1, 2, 3]
print(*nums)         # 等价 print(1, 2, 3)

d = {"a": 1, "b": 2}
f(**d)               # 等价 f(a=1, b=2)
```

Python 3 还支持「仅限关键字参数」——`*` 之后的参数只能按关键字传，强制调用方写清楚参数名：

```python
def g(x, *, sep=","):
    pass

g(1, sep=";")   # 合法
g(1, ";")       # TypeError，sep 只能按关键字传
```

## 7.2 可变默认参数陷阱

这是 Python 最著名的坑之一。默认参数在函数定义时只求值一次，而不是每次调用都求值：

```python
def add_item(x, lst=[]):
    lst.append(x)
    return lst

add_item(1)   # [1]
add_item(2)   # [1, 2]，第二次调用复用了同一个 list！
```

原因：`lst=[]` 里的空 list 在 def 执行那一刻创建，之后所有不带 lst 的调用共享这同一个 list 对象。正确做法是用 None 作默认值，在函数体内再创建：

```python
def add_item(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst
```

## 7.3 lambda 与高阶函数

lambda 是匿名函数，语法 `lambda 参数: 表达式`，只能写单表达式（不能有语句、不能多行）：

```python
square = lambda x: x * x
square(3)   # 9
```

lambda 主要用于需要「传一个短函数」的场合，配合内置高阶函数：

```python
list(map(lambda x: x * 2, [1, 2, 3]))              # [2, 4, 6]
list(filter(lambda x: x % 2 == 0, range(10)))      # [0, 2, 4, 6, 8]
sorted(["apple", "pear", "kiwi"], key=len)         # 按长度排序
sorted(users, key=lambda u: u.age)                 # 按对象属性排序
```

`key` 参数是 sorted / min / max / sort 的通用利器，比 Java 里写 Comparator 简洁得多。

> 建议：lambda 超过一行就该改用 def 命名函数，可读性优先。PEP 8 也建议优先 def。

## 7.4 作用域 LEGB 与 global / nonlocal

Python 变量查找遵循 LEGB 顺序——Local → Enclosing（闭包外层）→ Global → Builtin：

```python
x = "global"          # G
def outer():
    x = "enclosing"   # E
    def inner():
        x = "local"   # L
        print(x)      # 优先找到 local
    inner()
```

有个和直觉相反的点：在函数内「读取」外层变量没问题，但「赋值」会默认创建新的局部变量，而不是修改外层的：

```python
x = 10
def f():
    x = 20       # 创建局部变量 x，不影响全局 x
f()
print(x)         # 10，全局 x 没变
```

要修改外层变量，必须显式声明：

```python
x = 10
def f():
    global x     # 声明用全局的 x
    x = 20
f()
print(x)         # 20
```

`nonlocal` 用于闭包中修改「最近的外层非全局作用域」变量：

```python
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

c = counter()
c()   # 1
c()   # 2
```

## 7.5 闭包

闭包 = 函数 + 它引用的外层作用域变量。Python 里内层函数能「记住」定义时所在的外层变量：

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n   # n 被内层函数捕获
    return multiplier

double = make_multiplier(2)
double(5)   # 10
```

闭包是装饰器的基石（下一节），也是经典面试题「for 循环里 lambda 共享变量」的根源：

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)
funcs[0]()   # 2，三个 lambda 都返回 2，不是 0/1/2
```

原因是 lambda 捕获的是变量 `i` 本身（引用），不是循环当下的值；循环结束后 `i` 已经是 2。修复方式是用默认参数「冻结」当前值：`lambda i=i: i`，或用 `functools.partial`。

## 7.6 装饰器 decorator

装饰器是「接受函数、返回函数」的高阶函数，用来给函数增加额外行为，而不修改函数本身。理解它之前，先看一个等价形式：

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def hello(name):
    return f"hello {name}"

hello("tom")   # 先打印 calling hello，再返回 hello tom
```

`@log` 完全等价于 `hello = log(hello)`。装饰器把「原函数」替换成了 wrapper，所以：

- `*args, **kwargs` 用来透传任意参数，保证装饰器对任何签名的函数都通用。
- `return func(...)` 保留原函数的返回值。

带参数的装饰器（如 `@log("INFO")`）需要再加一层：外层函数接收参数、返回真正的装饰器：

```python
def tag(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{level}] {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@tag("INFO")
def run():
    pass
```

这里 `@tag("INFO")` 等价于 `run = tag("INFO")(run)`。

一个影响调试的细节：被装饰后函数的 `__name__`、`__doc__` 变成了 wrapper 的，用 `functools.wraps(func)` 可以还原元数据：

```python
from functools import wraps

def log(func):
    @wraps(func)          # 保留 func 的 __name__ / __doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

> 结论：装饰器本质上就是「函数的函数」，Python 里函数是一等公民（可当参数、可作返回值），装饰器才有存在空间。它对应 Java 里的注解 + AOP 切面，但装饰器是运行期直接改写函数对象，更直接。

---

# 8. 类与面向对象

## 8.1 类定义、self 与 __init__

Python 的类用 `class` 定义，`__init__` 是构造器（不是 `new`，实例化直接 `类名()`），`self` 相当于 Java 的 `this`，但必须显式写在每个实例方法的第一个参数：

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says wang"

d = Dog("旺财")
d.speak()          # '旺财 says wang'
```

`__init__` 负责初始化（在对象已创建后运行），真正的对象创建是 `__new__`（普通场景不碰）。`self` 不是关键字，只是约定俗成的名字，但强烈建议遵守。

## 8.2 实例属性 vs 类属性

类属性定义在类体里，属于类本身，所有实例共享；实例属性定义在 `__init__` 里（通过 `self`），每个实例独立：

```python
class Cat:
    species = "猫"        # 类属性

    def __init__(self, name):
        self.name = name  # 实例属性

c1, c2 = Cat("a"), Cat("b")
c1.species        # '猫'，通过实例读类属性
Cat.species       # '猫'，通过类读
c1.name           # 'a'，实例属性
```

> 易错点：`c1.species = "狗"` 不会改类属性，而是在 c1 上新建了一个实例属性 `species` 并遮蔽了类属性。这是 Python 属性查找（实例命名空间优先于类命名空间）导致的，和 Java 的静态字段共享语义不同。要改类属性得写 `Cat.species = "狗"`。

## 8.3 访问控制的约定

Python 没有真正的 private，靠命名约定区分可见性：

| 写法 | 约定 | 实际效果 |
| ---- | ---- | ---- |
| `self.name` | 公开 | 无限制 |
| `self._name` | 受保护（约定） | 只是提示，外界仍可访问 |
| `self.__name` | 私有（约定） | 被改名（name mangling）成 `_类名__name`，避免子类冲突 |

`__name` 的「私有」是障眼法——解释器把它改名成 `_ClassName__name`，主要目的是防止子类无意覆盖，而不是阻止访问。外界仍能通过 `obj._ClassName__name` 拿到：

```python
class A:
    def __init__(self):
        self.__x = 1

A()._A__x   # 1，照样能访问
```

> 结论：Python 的访问控制是「君子约定」，没有编译期/运行期强制。`_` 前缀表示「别动」，`__` 前缀只是做了名字改写。Java 开发者别把 `__` 当成真的 private。

## 8.4 继承、多继承与 MRO

单继承语法 `class Child(Parent)`，`super()` 调用父类方法：

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)     # 调用父类构造
        self.breed = breed
```

Python 支持多继承，方法查找顺序由 MRO（Method Resolution Order，方法解析顺序）决定，算法是 C3 线性化：

```python
class A:
    def f(self): return "A"
class B(A):
    def f(self): return "B"
class C(A):
    def f(self): return "C"
class D(B, C):
    pass

D().f()      # 'B'，按 MRO：D -> B -> C -> A -> object
D.mro()      # [D, B, C, A, object]
```

MRO 用 `类名.mro()` 或 `类名.__mro__` 查看。`super()` 在多继承里不再简单指向「父类」，而是「MRO 中当前类之后的下一个类」，这避免了菱形继承里父类被重复调用的问题。

> 易错点：多继承容易写出难以推理的代码（尤其菱形结构），能用组合或协议（鸭子类型）解决的问题就别上多继承。真要继承，让 `__init__` 都调用 `super().__init__()`，别绕过。

## 8.5 魔术方法

魔术方法（dunder method，双下划线方法）让自定义对象能参与 Python 的语法和内置函数，是「鸭子类型」的实现基础：

| 魔术方法 | 触发场景 |
| ---- | ---- |
| `__init__` | 实例化 |
| `__str__` | `str(obj)`、`print(obj)` |
| `__repr__` | `repr(obj)`、交互式环境展示 |
| `__eq__` | `==` |
| `__hash__` | `hash(obj)`、作 dict 的 key |
| `__len__` | `len(obj)` |
| `__iter__` / `__next__` | 迭代 |
| `__getitem__` | `obj[i]`、切片 |
| `__call__` | `obj()`，让实例可调用 |
| `__enter__` / `__exit__` | with 语句 |

实现一个可比较、可打印的类：

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
print(p)          # Point(1, 2)
p == Point(1, 2)  # True
```

> 易错点：定义了 `__eq__` 而不定义 `__hash__`，实例会变成不可哈希，无法放入 set / dict key。因为 Python 要求「相等的对象必须有相同的 hash」。要么同时实现两者，要么把 `__hash__ = None` 显式声明不可哈希。

## 8.6 property、classmethod、staticmethod

property 把方法伪装成属性，用于「读取时计算」或「写入时校验」，避免直接暴露内部字段：

```python
class Circle:
    def __init__(self, r):
        self._r = r
    @property
    def area(self):
        return 3.14 * self._r ** 2   # 读 area 时动态算
    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, value):
        if value < 0:
            raise ValueError("radius 不能为负")
        self._r = value

c = Circle(2)
c.area          # 12.56，像属性一样访问，不需要加括号
c.r = -1        # ValueError
```

classmethod 和 staticmethod 的区别在于第一个参数：

| 装饰器 | 第一个参数 | 用途 |
| ---- | ---- | ---- |
| `@classmethod` | cls（类本身） | 操作类属性、提供替代构造器 |
| `@staticmethod` | 无 | 逻辑上属于类、但不依赖类或实例的工具函数 |

```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d
    @classmethod
    def from_string(cls, s):
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)     # cls 会根据实际调用类动态解析

Date.from_string("2026-10-08")   # 替代构造器
```

classmethod 常见于「替代构造器」场景，staticmethod 其实就是普通函数放到类命名空间里。

## 8.7 __slots__

默认情况下，每个实例用一个 dict（`__dict__`）存属性，灵活但内存开销大。`__slots__` 用固定槽位代替 dict，省内存、访问更快：

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y
```

代价是：不能动态添加属性（`p.z = 1` 会 AttributeError）、不能有 `__dict__`、与某些特性（如多继承、pickle 的某些用法）有兼容限制。海量小对象（如点的集合、矩阵元素）才值得用，普通类别过早优化。

## 8.8 dataclass

Python 3.7+ 的 dataclass 自动生成 `__init__`、`__repr__`、`__eq__` 等样板方法，适合「数据载体」类：

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    vip: bool = False     # 有默认值的字段放后面

u = User("tom", 18)
print(u)          # User(name='tom', age=18, vip=False)
u == User("tom", 18)   # True，自动比较
```

对比手写 `__init__`，dataclass 少了几十行样板。配合 `field(default_factory=...)` 还能正确处理可变默认值（见 7.2 的陷阱，dataclass 里同样不能直接 `= []`）：

```python
@dataclass
class Order:
    items: list = field(default_factory=list)   # 每次实例化都新建 list
```

---

# 9. 异常处理

## 9.1 异常模型与 try / except / else / finally

Python 用异常处理错误，语法比 Java 多一个 else 子句：

```python
try:
    x = int("abc")
except ValueError as e:      # 捕获具体异常
    print("转换失败", e)
except (TypeError, KeyError):  # 捕获多个异常
    pass
else:
    print("没异常才执行", x)   # try 块完全成功才走这里
finally:
    print("无论如何都执行")     # 资源清理
```

四个子句的语义：

- `except`：捕获匹配的异常
- `else`：try 块没抛异常时执行
- `finally`：无论是否异常、是否 return 都执行，常用于释放资源

> 易错点：`except Exception` 会吞掉几乎所有异常（包括本该暴露的程序 bug），要尽量捕获具体异常类型。`except:` 裸捕获连 KeyboardInterrupt、SystemExit 都吞，几乎永远是错的。另外 finally 里 return 会覆盖 try 里的 return，别在 finally 里返回值。

## 9.2 raise 与自定义异常

`raise` 抛出异常，自定义异常只需继承 Exception：

```python
class InsufficientFundsError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError("余额不足")
    return balance - amount
```

保留原始异常链用 `raise ... from ...`：

```python
try:
    risky()
except ValueError as e:
    raise RuntimeError("处理失败") from e   # 保留原始 e 作为 cause
```

## 9.3 常见内置异常

| 异常 | 触发场景 |
| ---- | ---- |
| `TypeError` | 类型不对，如 `1 + "1"` |
| `ValueError` | 类型对但值不对，如 `int("abc")` |
| `KeyError` | 字典键不存在 |
| `IndexError` | 序列下标越界 |
| `AttributeError` | 对象没有该属性 |
| `ZeroDivisionError` | 除零 |
| `ImportError` / `ModuleNotFoundError` | 导入失败 |
| `FileNotFoundError` | 文件不存在 |

异常层级里，`Exception` 是绝大多数业务异常的基类，`BaseException` 是所有异常的根（还包括 SystemExit、KeyboardInterrupt，通常不捕获它们）。

---

# 10. 模块与包

## 10.1 import 机制与搜索路径

每个 `.py` 文件就是一个模块，import 后模块名即文件名：

```python
import math
math.sqrt(16)   # 4.0
```

import 时 Python 按顺序搜索 sys.path 里的目录（含脚本所在目录、环境变量 PYTHONPATH、标准库目录、第三方 site-packages），找到第一个匹配的模块就加载。模块首次 import 后会被缓存到 sys.modules，重复 import 不会重复执行模块代码。

## 10.2 from / import / as / 星号

```python
from math import sqrt        # 只导入 sqrt，直接用 sqrt(16)
from math import sqrt as sq  # 起别名
import numpy as np           # 模块别名
from math import *           # 导入全部（不推荐，污染命名空间）
```

> 易错点：`from math import *` 会导入一堆不知道哪来的名字，覆盖你已有的变量，且可读性差，团队里基本禁用。`import math` 和 `from math import sqrt` 选一个：前者命名空间清晰，后者省敲字。

## 10.3 包与 __init__.py

包是含 `__init__.py` 的目录（Python 3.3+ 即使没有 `__init__.py` 也认作命名空间包，但常规项目仍建议放）：

```text
mypkg/
├── __init__.py
├── a.py
└── sub/
    ├── __init__.py
    └── b.py
```

`__init__.py` 在导入包时执行，可以放包的初始化逻辑，或通过 `__all__` 控制 `from mypkg import *` 导出的名字。包内模块用相对导入互相引用：

```python
# mypkg/a.py 里引用同包 sub/b.py
from .sub import b        # 相对导入
from . import a           # 引用同包 a
```

相对导入用 `.` 表示当前包、`..` 表示父包，仅在包内有效，直接以脚本运行包内文件会报错。

## 10.4 __name__ 与 main

每个模块有个 `__name__` 属性：作为主程序运行时是 `"__main__"`，被 import 时是模块名。用它区分「直接运行」和「被导入」：

```python
if __name__ == "__main__":
    main()   # 只有直接运行 python xxx.py 时才执行
```

这是几乎所有 Python 脚本的标准结尾，保证模块既能单独跑、又能被别处 import 而不触发入口逻辑。

---

# 11. 迭代器与生成器

## 11.1 可迭代对象与迭代器

分清两个概念：

- 可迭代对象（iterable）：实现了 `__iter__`，能被 `for` 遍历。list、tuple、str、dict、set、range 都是。
- 迭代器（iterator）：实现了 `__next__`，能被 `next()` 逐个取值，遍历一次就耗尽。

两者关系用 `iter()` 和 `next()` 打通：

```python
it = iter([1, 2, 3])   # iter() 把可迭代对象转成迭代器
next(it)   # 1
next(it)   # 2
next(it)   # 3
next(it)   # StopIteration，耗尽
```

for 循环本质上是「取迭代器 → 反复 next → 捕获 StopIteration 停止」的语法糖。关键区别：list 是可迭代对象但不是迭代器（能反复遍历），迭代器是一次性的。

```python
lst = [1, 2, 3]
list(lst)   # [1, 2, 3]，list 可反复遍历

it = iter(lst)
list(it)    # [1, 2, 3]
list(it)    # []，迭代器已耗尽
```

## 11.2 生成器与 yield

生成器（generator）是特殊的迭代器，函数里只要出现 `yield` 就变成生成器函数，调用它不执行函数体，而是返回生成器对象：

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)
next(gen)   # 3
next(gen)   # 2
```

yield 的妙处是「暂停并保留现场」——每次 `next` 执行到下一个 yield 就暂停，局部变量、执行位置都保留，下次 next 接着跑。这比「一次性算出整个 list」更省内存，因为值是按需一个个产生的。

## 11.3 生成器表达式

生成器表达式是「惰性的列表推导式」，把方括号换成圆括号：

```python
squares = [x * x for x in range(1_000_000)]      # 列表推导式：立即算出 100 万个元素
squares = (x * x for x in range(1_000_000))      # 生成器表达式：惰性，用到才算
```

函数调用时若生成器是唯一参数，可以省略外层的圆括号：`sum(x * x for x in range(10))`。

## 11.4 惰性求值的意义

生成器（含生成器表达式）的核心价值是惰性求值——不一次性占用全部内存。对比两种做法处理超大文件：

```python
# 一次性读入，可能撑爆内存
lines = [line for line in open("big.txt")]
# 惰性逐行处理，内存占用恒定
for line in open("big.txt"):
    process(line)
```

生成器还能表达「无限序列」：

```python
def naturals():
    n = 0
    while True:
        yield n
        n += 1

from itertools import islice
list(islice(naturals(), 5))   # [0, 1, 2, 3, 4]，截取前 5 个
```

> 结论：处理可能很大的数据集、或数据流式产生时，优先用生成器；数据量小、需要反复随机访问时才用 list。

---

# 12. 上下文管理器

## 12.1 with 语句

with 保证资源（文件、锁、连接、事务）无论是否异常都能被正确释放，替代手写 try/finally：

```python
with open("data.txt") as f:      # 离开 with 块自动 f.close()
    content = f.read()
```

等价于：

```python
f = open("data.txt")
try:
    content = f.read()
finally:
    f.close()
```

with 是文件操作的标准写法，也是「拿锁」的标准写法：`with lock:` 进入时 acquire、离开时 release，忘记释放锁这类问题从根上消除。

## 12.2 自定义上下文管理器

实现 `__enter__`（进入时执行）和 `__exit__`（离开时执行）即可：

```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"耗时 {self.elapsed:.3f}s")

with Timer():
    do_work()
```

`__exit__` 返回 True 表示「吞掉异常」，返回 False（或 None）则异常继续向外抛。

## 12.3 contextlib

标准库 contextlib 提供两个便捷工具。`contextmanager` 用生成器快速写上下文管理器，不必手写类：

```python
from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    yield
    print(f"</{name}>")

with tag("div"):
    print("内容")
```

`yield` 之前的代码是 `__enter__`，之后的代码是 `__exit__`。还有 `closing`、`nullcontext` 等工具函数。

---

# 13. 内存管理

## 13.1 引用计数

CPython 主要靠引用计数（reference counting）管理内存：每个对象维护一个计数器，被引用就 +1，引用解除就 -1，减到 0 立即回收：

```python
import sys
a = []                 # 引用计数 1
b = a                  # 2
sys.getrefcount(a)     # 返回 3（函数参数本身也临时持有一个引用）
del b                  # 减回 1
del a                  # 减到 0，list 立即被回收
```

引用计数的好处是「即时回收」——对象一没人用就释放，没有 GC 停顿。副作用是每个赋值都要更新计数，有性能开销，这也是 CPython 偏慢的原因之一。

## 13.2 垃圾回收与循环引用

引用计数有个致命盲区——循环引用无法自减到 0：

```python
class Node:
    pass

a, b = Node(), Node()
a.next, b.next = b, a    # a 引用 b，b 引用 a，形成环
del a, b                 # 外部引用都删了，但两者互相引用，计数不为 0
```

所以 CPython 额外引入分代垃圾回收（generational GC）专门处理循环引用：把对象按「存活代数」分 0/1/2 三代，新对象在 0 代，存活越久代数越高、被扫描频率越低。GC 用可达性分析（类似 Java 的标记-清除）找出循环引用里不可达的对象并回收。可用 `gc` 模块手动触发或调参：

```python
import gc
gc.collect()   # 手动触发一次全量 GC
```

## 13.3 小整数池与字符串驻留

两个「缓存」优化，常被面试和 is 判断搞混：

- 小整数池：-5 到 256 之间的整数在解释器启动时预创建，所有对它们的引用都指向同一个对象。
- 字符串驻留（interning）：由字面量产生的短字符串、纯字母数字的标识符字符串，会被驻留（共享同一对象）。

```python
a, b = 256, 256
a is b    # True，命中小整数池

x, y = 257, 257
x is y    # False（CPython 里通常 False），257 不在小整数池

"abc" is "abc"       # True，驻留
"a b" is "a b"       # False，含空格的字符串可能不驻留
```

> 易错点：这就是「比较整数/字符串别用 is」的根本原因——is 的结果依赖缓存实现，小数字碰巧 True、大数字 False，行为不稳定。判断值相等永远用 `==`，`is` 只用于判断身份（如 `is None`）。

## 13.4 常见内存陷阱

| 陷阱 | 原因 | 规避 |
| ---- | ---- | ---- |
| 可变默认参数 | 默认值只求值一次 | 默认值用 None，函数内再建 |
| `[[0]]*3` 共享内层 | `*` 是浅重复 | 用 `[[0] for _ in range(3)]` |
| for 里 lambda 共享变量 | 闭包捕获的是变量引用 | `lambda i=i: ...` 冻结 |
| `+` 拼接字符串 | 每次都建新 str | `''.join(...)` |
| 大文件整读进内存 | 一次性加载 | 用生成器 / 迭代器流式处理 |
| 循环引用 | 引用计数减不到 0 | 用 weakref、或及时断链 |

这些陷阱多数根源于「引用语义 + 可变性」这两个第 2 章讲透的概念，理解了对象模型，大部分怪现象都能归因。

---

# 附：高频速记

| 主题 | 关键点 |
| ---- | ---- |
| 类型系统 | 动态类型 + 强类型 + 一切皆对象 + 引用语义 |
| 可变性 | int/str/tuple 不可变，list/dict/set 可变；可变对象原地改影响所有引用者 |
| 赋值 vs 拷贝 | `=` 只加标签；`[:]`/`copy.copy` 浅拷贝；`copy.deepcopy` 深拷贝 |
| 参数传递 | 按对象引用传递（call by sharing），可变对象函数内改影响调用方 |
| `==` vs `is` | `==` 比值（走 `__eq__`），`is` 比身份（id）；判 None 用 `is` |
| 切片 | `seq[start:stop:step]` 左闭右开，越界不报错，负步长反转 |
| dict | 键必须可哈希（不可变），`get`/`setdefault` 防 KeyError |
| 推导式 | `[x for x in ... if ...]`，生成器表达式用圆括号（惰性） |
| 循环 else | 没被 break 才执行，语义 = no break |
| 函数 | `*args`/`**kwargs`；默认参数只求值一次（用 None 规避）；`lambda` 单表达式 |
| 作用域 | LEGB：Local→Enclosing→Global→Builtin；改外层用 global/nonlocal |
| 装饰器 | 函数的函数，`@decorator` = `f = decorator(f)`，用 `functools.wraps` 保元数据 |
| 类 | `__init__` 构造、`self` 是 this；类属性 vs 实例属性；无真 private（`__` 是名字改写） |
| 多继承 | MRO 用 C3 线性化，`类.mro()` 查看；super() 走 MRO 下一个 |
| 魔术方法 | `__str__/__eq__/__hash__/__iter__/__enter__` 等，是鸭子类型基础 |
| dataclass | 3.7+ 自动生成 init/repr/eq，可变默认值用 field(default_factory=...) |
| 异常 | try/except/else/finally；捕获具体异常；`raise ... from ...` 保链 |
| 模块 | import 缓存于 sys.modules；`__name__ == "__main__"` 区分入口 |
| 迭代器/生成器 | 生成器用 yield 惰性产出，省内存；迭代器一次性 |
| with | `__enter__`/`__exit__`，保证资源释放；contextlib.contextmanager 简化 |
| 内存 | 引用计数即时回收 + 分代 GC 处理循环引用；-5~256 小整数池、字符串驻留 |
