# ArkTS 基础语法

> ArkTS 是 HarmonyOS 的应用开发语言，本质是 TypeScript 的严格子集：保留类型系统与大部分语法，裁剪运行时动态特性以换取性能与稳定性，再叠加 ArkUI 的声明式 UI 扩展。本篇聚焦语言本身，按「基础类型 → 变量 → 函数 → 类与接口 → 泛型 → 模块 → 流程控制 → 类型断言与空安全」铺开纯语法部分，再进入并发模型，最后给出 ArkTS 与 TypeScript 的差异清单。UI 声明式语法与状态管理装饰器单独成篇，见《ArkUI基础语法》。已熟悉 TS 的读者可重点看第 11 章差异清单。

## 目录

- [1. ArkTS 概述](#1-arkts-概述)
- [2. 基础类型](#2-基础类型)
- [3. 变量与常量](#3-变量与常量)
- [4. 函数](#4-函数)
- [5. 类与接口](#5-类与接口)
- [6. 泛型](#6-泛型)
- [7. 模块与命名空间](#7-模块与命名空间)
- [8. 运算符与流程控制](#8-运算符与流程控制)
- [9. 类型断言与空安全](#9-类型断言与空安全)
- [10. 并发模型](#10-并发模型)
- [11. ArkTS 与 TypeScript 的差异](#11-arkts-与-typescript-的差异)
- [附：高频速记](#附高频速记)

---

# 1. ArkTS 概述

## 1.1 ArkTS 是什么

ArkTS 是华为为 HarmonyOS 应用开发打造的编程语言，源文件以 `.ets` 为后缀。它的定位一句话可以说清：以 TypeScript 为基础的语言子集 + 面向 ArkUI 声明式开发的语法扩展。

两者的分工：

| 层面 | 内容 |
| ---- | ---- |
| 语言子集 | 继承 TS 的类型系统、class、泛型、模块等核心语法；禁用 any、动态属性、for...in 等动态特性 |
| ArkUI 扩展 | struct 组件、build() UI 描述、状态管理装饰器（@State/@Prop/@Link 等）、渲染控制（if/else、ForEach） |

一个最小的 ArkUI 组件长这样，能同时看到两部分的影子：

```ts
@Entry
@Component
struct Index {
  @State message: string = 'Hello ArkTS'

  build() {
    Column() {
      Text(this.message)
        .fontSize(30)
      Button('点我')
        .onClick(() => {
          this.message = '已点击'
        })
    }
  }
}
```

struct、@Entry、@Component、@State、build() 属于 ArkUI 扩展；string 类型、箭头函数、类成员访问属于 TS 语法部分。

## 1.2 与 TypeScript / JavaScript 的关系

三者的关系是层层收紧：JavaScript 是动态语言，TypeScript 给它加上静态类型但保留全部动态能力，ArkTS 则从 TS 中裁掉运行时动态特性，只保留可静态优化的部分，再加上 UI 扩展。

| 对比维度 | JavaScript | TypeScript | ArkTS |
| ---- | ---- | ---- | ---- |
| 类型检查 | 无 | 编译期，可选 | 编译期，强制 |
| any 类型 | 天然支持 | 支持 | 禁止 |
| 运行时改对象结构 | 支持 | 支持 | 禁止 |
| 执行引擎 | V8 / JSCore 等解释执行 | 编译为 JS 后执行 | ArkCompiler 编译为字节码（.abc），AOT 优化 |

为什么要裁掉动态特性？因为动态性是性能的天敌。禁止运行时修改对象布局后，属性偏移量在编译期就能确定，属性访问从「哈希查找」变成「固定偏移读取」；禁止 any 之后，类型信息完整，编译器可以做 AOT 编译和内联优化。这是 ArkTS 的核心设计取舍——用一部分灵活性换取接近原生语言的执行效率。

## 1.3 编译期装饰器的本质

ArkUI 的装饰器（@State、@Component 等）不是运行时反射，而是编译期的代码生成指令：编译器把装饰器展开成等价的命令式代码（比如 @State 展开后包含依赖收集和 UI 刷新通知逻辑），运行时根本不存在「装饰器」这个概念。

这也解释了为什么 ArkTS 装饰器只能用在特定位置（struct 内的字段、类、方法上），并且每条都有严格的使用规则——它们本质上是编译器认得的关键字，写错位置编译器直接报错。

# 2. 基础类型

## 2.1 基本类型

```ts
let count: number = 42          // 数字，不区分 int/double，统一为 number
let price: number = 9.99
let name: string = 'ArkTS'      // 字符串，单双引号等价，支持模板字符串
let ok: boolean = true          // 布尔，只能赋 true/false
```

number 统一表示整数和浮点数，没有 Java 那种 int/long/float/double 的细分。整数运算的结果仍然是 number（IEEE 754 双精度），需要精确大整数时用 bigint。

模板字符串用反引号，配合 `${}` 嵌入表达式：

```ts
let user: string = 'Tom'
let greeting: string = `你好, ${user}, 明年 ${18 + 1} 岁`
```

## 2.2 数组与元组

```ts
// 数组：两种等价写法
let nums: number[] = [1, 2, 3]
let strs: Array<string> = ['a', 'b']

// 元组：固定长度、每个位置类型可不同
let point: [number, string] = [1, 'one']
let id: number = point[0]
```

数组是同类型元素的有序集合，长度可变；元组是固定长度、各位置类型可不同的复合值。访问越界元素在 ArkTS 中会在运行时报错，不像 JS 那样返回 undefined。

## 2.3 枚举

```ts
enum Color {
  Red,      // 默认从 0 开始，Red=0
  Green,    // Green=1
  Blue      // Blue=2
}

enum StatusCode {
  Success = 200,
  NotFound = 404,
  Error = 500
}

let c: Color = Color.Green
let code: StatusCode = StatusCode.Success
```

枚举成员可以显式赋值（数字或字符串），未赋值的从上一个成员递增。按名取值用 Color.Red，反向取值 Color[1] 在 ArkTS 中受限，需要按名使用。

## 2.4 联合类型与类型别名

```ts
// 联合类型：值可以是几种类型之一
let id: number | string = 100
id = 'A100'   // 也可以

// 类型别名：给类型起名字
type Point = {
  x: number
  y: number
}

type ID = number | string
let p: Point = { x: 1, y: 2 }
```

联合类型配合类型收窄（typeof / instanceof / in 判断）使用，是 ArkTS 里替代多态重载的常见手段：

```ts
function format(value: number | string): string {
  if (typeof value === 'number') {
    return value.toFixed(2)     // 此分支中 value 已收窄为 number
  }
  return value.toUpperCase()    // 此分支中 value 已收窄为 string
}
```

## 2.5 字面量类型

```ts
type Direction = 'up' | 'down' | 'left' | 'right'

let dir: Direction = 'up'    // 只能是这四个字符串之一
// dir = 'top'               // 编译报错
```

字面量类型把取值范围约束到几个具体值，常和联合类型组合表达「有限选项」，比 boolean 更有表达力（比如 loading / success / error 三态）。

## 2.6 any / unknown / void / null / undefined

```ts
// ArkTS 禁止 any / unknown 作为变量类型
// let x: any = 100          // 编译报错
// let y: unknown = 'str'    // 编译报错

let nothing: void = undefined    // void：函数无返回值
let n: null = null
let u: undefined = undefined
```

ArkTS 强制所有变量有明确类型，any 和 unknown 被禁用。函数无返回值用 void。null 和 undefined 是两个独立类型，配合可选类型（如 string | null）表达「可能没有值」。

与 JS / TS 库互操作时若拿不到类型信息，any 又不能用，可用 ESObject 兜底——但应尽量避免，它会降低类型检查、产生告警并带来运行时开销：

```ts
// let data: any = loadFromJsLib()    // any 被禁
let data: ESObject = loadFromJsLib()  // ESObject：互操作动态对象的兜底
```

# 3. 变量与常量

## 3.1 let 与 const

ArkTS 禁止 var，变量声明只有 let（可变）和 const（不可变）：

```ts
let current: number = 1      // 可重新赋值
current = 2

const max: number = 100      // 不可重新赋值
// max = 200                 // 编译报错
```

const 约束的是绑定不可变，不是值深度不可变——const 声明的对象内部属性仍可修改：

```ts
class Config {
  url: string = 'https://example.com'
}

const config: Config = new Config()
config.url = 'https://harmonyos.com'   // 允许，修改的是对象内容
// config = new Config()               // 报错，绑定不可变
```

## 3.2 类型注解与类型推断

类型注解是显式声明，类型推断是编译器自动推导。两者混用是惯常做法：能推断时省略注解，公开接口和字段补全注解。

```ts
let count = 10              // 推断为 number
let name = 'ArkTS'          // 推断为 string

function add(a: number, b: number): number {   // 参数必须注解，返回值可推断
  return a + b
}

class User {
  id: number = 0            // 字段建议显式注解
  nickname: string = ''
}
```

# 4. 函数

## 4.1 函数声明与箭头函数

```ts
// 函数声明
function sum(a: number, b: number): number {
  return a + b
}

// 函数表达式
const multiply = function (a: number, b: number): number {
  return a * b
}

// 箭头函数（最常用）
const divide = (a: number, b: number): number => {
  return a / b
}

// 单表达式可省略 return 和大括号
const square = (n: number): number => n * n
```

箭头函数除了语法简洁，还有一个关键差异：它不绑定自己的 this，捕获定义处外层的 this。UI 事件回调里大量使用箭头函数，正是为了在回调中继续访问组件的 this：

```ts
Button('点我')
  .onClick(() => {
    this.count++    // 箭头函数中的 this 仍是组件实例
  })
```

## 4.2 参数：可选、默认、剩余

```ts
// 可选参数：参数名后加 ?，类型自动变为 type | undefined
function greet(name: string, title?: string): string {
  return title ? `${title} ${name}` : name
}
greet('Tom')              // "Tom"
greet('Tom', 'Dr')        // "Dr Tom"

// 默认参数：调用时可省略
function power(base: number, exp: number = 2): number {
  return base ** exp
}
power(3)                  // 9
power(3, 3)               // 27

// 剩余参数：rest 收集成数组
function total(...nums: number[]): number {
  let sum = 0
  for (const n of nums) {
    sum += n
  }
  return sum
}
total(1, 2, 3)            // 6
```

## 4.3 函数类型

函数类型描述「参数列表 + 返回值」的形状，用于回调、高阶函数：

```ts
type MathOp = (a: number, b: number) => number

const add: MathOp = (a, b) => a + b
const sub: MathOp = (a, b) => a - b

function calculate(a: number, b: number, op: MathOp): number {
  return op(a, b)
}
calculate(10, 5, add)     // 15
calculate(10, 5, sub)     // 5
```

回调是 ArkTS 中最常见的函数类型应用，比如 setTimeout、事件回调、ForEach 的键值生成函数：

```ts
ForEach(this.items, (item: Item) => {
  Text(item.name)
}, (item: Item) => item.id.toString())
```

## 4.4 函数重载

函数重载让同一个函数名接受多组不同参数，通过「多个签名 + 一个实现」表达：

```ts
// 重载签名：只有声明，没有函数体
function format(value: string): string
function format(value: number): string

// 实现签名：参数类型是各重载签名的联合
function format(value: string | number): string {
  return typeof value === 'string' ? value : value.toFixed(2)
}

format('ArkTS')   // "ArkTS"
format(3.14159)   // "3.14"
```

重载的约束：各签名参数列表必须不同（类型/数量/顺序）；实现函数的参数类型要能兼容所有签名。编译期根据实参选择匹配的签名，运行时仍是同一个函数体——重载不产生多个函数。

## 4.5 闭包

闭包 = 函数 + 它捕获的外层变量。函数在定义处记住外层作用域的变量，即使外层函数已返回，捕获的变量仍被持有：

```ts
function makeCounter(): () => number {
  let count = 0
  return () => {
    count++
    return count
  }
}

const counter = makeCounter()
counter()   // 1
counter()   // 2，count 被闭包持有，状态持续
```

闭包在 ArkUI 里常用于事件回调，但要留意：闭包捕获的是变量本身（引用），不是值的快照——若捕获的是状态装饰器变量，要注意刷新时机。

# 5. 类与接口

## 5.1 类与构造器

```ts
class Person {
  name: string           // 字段声明
  age: number = 0        // 字段可带默认值

  constructor(name: string, age: number) {
    this.name = name     // 构造器里初始化
    this.age = age
  }

  describe(): string {
    return `${this.name}, ${this.age} 岁`
  }
}

const p = new Person('Tom', 25)
p.describe()
```

和 TS 不同，ArkTS 的 class 字段必须先声明再使用，不能在构造器里临时加属性——这是「对象布局固定」约束的直接体现。

## 5.2 可见性与 readonly

```ts
class Account {
  public id: string = ''          // 公开（默认）
  private password: string = ''   // 仅类内部
  protected level: number = 0     // 类内部 + 子类
  readonly createdAt: number = Date.now()   // 初始化后不可改

  constructor(id: string) {
    this.id = id
    // this.createdAt = 0          // 报错，readonly 不可再赋值
  }
}
```

ArkTS 不支持 TS 的 # 号私有字段写法，统一用 private 关键字。

## 5.3 继承与抽象类

```ts
class Animal {
  name: string = ''
  makeSound(): void {
    console.log('...')
  }
}

class Dog extends Animal {
  breed: string = ''

  makeSound(): void {        // 重写父类方法
    console.log('汪汪')
  }
}

// 抽象类：不能实例化，子类必须实现抽象成员
abstract class Shape {
  abstract area(): number    // 抽象方法，无实现

  describe(): string {       // 普通方法，子类直接继承
    return `面积: ${this.area()}`
  }
}

class Circle extends Shape {
  radius: number = 0

  constructor(r: number) {
    super()                  // 先调用父类构造器
    this.radius = r
  }

  area(): number {
    return Math.PI * this.radius ** 2
  }
}
```

继承用 extends，子类构造器必须在访问 this 前调用 super()。抽象类定义「部分实现的模板」，把公共逻辑放在父类，把必须定制的部分留给子类。

## 5.4 接口与 implements

```ts
interface Printable {
  print(): void
}

interface Serializable {
  toJSON(): string
}

// 一个类可实现多个接口
class Document implements Printable, Serializable {
  content: string = ''

  print(): void {
    console.log(this.content)
  }

  toJSON(): string {
    return JSON.stringify({ content: this.content })
  }
}

// 接口也可以描述对象形状（结构约定）
interface User {
  id: number
  name: string
  email?: string           // 可选属性
  readonly createdAt: number   // 只读属性
}

const u: User = {
  id: 1,
  name: 'Tom',
  createdAt: Date.now()
}
```

注意 ArkTS 不支持 TS 的结构化类型（structural typing）：两个接口即使成员完全相同，也不能互相赋值——类型必须显式 implements 或 extends 建立关系。这是和 TS 语义差别最大的点之一。

## 5.5 静态成员与 getter/setter

```ts
class Counter {
  static instanceCount: number = 0     // 静态字段，属于类

  private _value: number = 0

  constructor() {
    Counter.instanceCount++
  }

  get value(): number {                // getter
    return this._value
  }

  set value(v: number) {               // setter
    if (v >= 0) {
      this._value = v
    }
  }

  static reset(): void {               // 静态方法
    Counter.instanceCount = 0
  }
}

Counter.instanceCount   // 类名访问静态成员
```

## 5.6 对象字面量

对象字面量必须显式标注类型，不能像 TS 那样裸写——这是「对象布局编译期固定」的直接体现：

```ts
interface Point {
  x: number
  y: number
}

const p1: Point = { x: 1, y: 2 }   // 正确：标注了 interface 类型
// const p2 = { x: 1, y: 2 }       // 报错：对象字面量缺少类型标注
```

约束有三条：必须对应 interface 或 class 类型；属性名必须是合法标识符；属性值类型要精确匹配。数组字面量同理，元素类型必须可推断。

# 6. 泛型

## 6.1 泛型函数

```ts
function identity<T>(value: T): T {
  return value
}

let s = identity<string>('ArkTS')   // 显式指定
let n = identity(42)                // 也可推断为 number
```

## 6.2 泛型类与接口

```ts
class Box<T> {
  private items: T[] = []

  add(item: T): void {
    this.items.push(item)
  }

  get(index: number): T {
    return this.items[index]
  }
}

const box = new Box<string>()
box.add('a')
box.add('b')

interface Comparable<T> {
  compareTo(other: T): number
}

class Version implements Comparable<Version> {
  major: number = 0
  minor: number = 0

  compareTo(other: Version): number {
    if (this.major !== other.major) return this.major - other.major
    return this.minor - other.minor
  }
}
```

## 6.3 泛型约束与默认值

```ts
// extends 约束：T 必须有 length 属性
function logLength<T extends { length: number }>(value: T): T {
  console.log(value.length)
  return value
}
logLength('hello')       // string 有 length
logLength([1, 2, 3])     // 数组有 length
// logLength(123)        // 报错，number 没有 length

// 泛型默认值
class Cache<K, V = string> {
  private map: Map<K, V> = new Map()

  put(key: K, value: V): void {
    this.map.set(key, value)
  }

  get(key: K): V | undefined {
    return this.map.get(key)
  }
}
const cache = new Cache<number>()    // V 默认 string
```

注意 ArkTS 泛型是不变型的（invariant），不像 TS 的泛型默认协变。泛型参数在编译期被严格区分，List<Animal> 和 List<Dog> 之间没有隐式转换关系，这是比 TS 更严格的类型安全保证。

## 6.4 受限的工具类型

ArkTS 从 TS 工具类型中只保留了四个：Partial、Required、Readonly、Record，其余（Pick、Omit、Exclude 等）全部禁用：

```ts
interface User {
  id: number
  name: string
  age: number
}

type PartialUser = Partial<User>            // 所有属性变可选
type RequiredUser = Required<PartialUser>   // 所有属性变必填
type ReadonlyUser = Readonly<User>          // 所有属性变只读
type NameScore = Record<string, number>     // 键 string、值 number 的映射
```

注意 Record 的下标访问类型是 `V | undefined`，取值后要判空：

```ts
const scores: Record<string, number> = { math: 95 }
const math: number | undefined = scores['math']
if (math !== undefined) {
  console.log(`数学: ${math}`)
}
```

# 7. 模块与命名空间

## 7.1 export 与 import

ArkTS 使用 ES Module 风格的模块语法，每个 `.ets` 文件是一个模块：

```ts
// ── utils.ets ──
export interface User {
  id: number
  name: string
}

export function formatUser(user: User): string {
  return `${user.id}: ${user.name}`
}

const VERSION = '1.0.0'
export default VERSION           // 默认导出，一个模块只能有一个

// ── main.ets ──
import VERSION, { User, formatUser } from './utils'
// 或者整体导入
import * as utils from './utils'

const u: User = { id: 1, name: 'Tom' }
formatUser(u)
```

HarmonyOS 工程里还有另一套 kit 导入风格，从系统 kit 引入平台能力：

```ts
import { router } from '@kit.ArkUI'
import { http } from '@kit.NetworkKit'
import { preferences } from '@kit.ArkData'
```

## 7.2 命名空间

namespace 用于组织同一模块内的代码，避免全局命名冲突：

```ts
namespace Geometry {
  export const PI: number = 3.14159

  export function circleArea(r: number): number {
    return PI * r * r
  }

  // 未 export 的成员外部不可见
  const SECRET = 42
}

Geometry.circleArea(2)   // 通过命名空间名访问
```

# 8. 运算符与流程控制

## 8.1 运算符

| 类别 | 运算符 | 说明 |
| ---- | ---- | ---- |
| 算术 | `+ - * / % **` | `**` 幂运算 |
| 赋值 | `= += -= *= /= %=` | 复合赋值 |
| 比较 | `== === != !==` | 恒用 `===` 和 `!==`，禁用宽松等 |
| 逻辑 | `&& \|\| ! ??` | `??` 空值合并，只在 null/undefined 时取右值 |
| 三元 | `cond ? a : b` | 条件表达式 |
| 可选链 | `?.` | 安全访问可能为 null 的链路 |
| 位运算 | `& \| ^ ~ << >> >>>` | 与 Java 语义一致 |

`??` 和 `||` 的区别值得单独记：`||` 在左值为任何假值（0、''、false、null、undefined）时取右值，`??` 只在 null/undefined 时取右值：

```ts
let count: number | null = 0
let a = count ?? 10    // 0 —— count 不是 null，取原值
let b = count || 10    // 10 —— 0 是假值，被 || 替换
```

## 8.2 条件与循环

```ts
// if / else
if (score >= 90) {
  grade = 'A'
} else if (score >= 60) {
  grade = 'B'
} else {
  grade = 'C'
}

// switch：ArkTS 要求 case 分支有确定类型，不支持 fall-through 之外的写法
switch (day) {
  case 1:
    name = '周一'
    break
  case 2:
    name = '周二'
    break
  default:
    name = '其他'
}

// for：经典计数循环
for (let i = 0; i < 10; i++) {
  console.log(`${i}`)
}

// for-of：遍历可迭代对象的值（最常用）
for (const item of items) {
  console.log(item.name)
}

// while：先判断后执行
while (queue.length > 0) {
  queue.pop()
}

// do-while：先执行一次再判断
let attempt = 0
do {
  attempt++
} while (attempt < 3)

// break：跳出整个循环；continue：跳过本次进入下一次
for (let i = 0; i < 10; i++) {
  if (i === 5) break         // 到 5 直接结束循环
  if (i % 2 === 0) continue  // 偶数跳过，只打印奇数
  console.log(`${i}`)
}
```

注意 for...in 在 ArkTS 中被禁用（遍历对象键的场景改用 Object.keys()，遍历数组场景改用 for...of）。

## 8.3 迭代器与集合

ArkTS 内置常用集合类型：

```ts
let set: Set<number> = new Set([1, 2, 2, 3])     // 去重，size=3
let map: Map<string, number> = new Map()
map.set('a', 1)
map.get('a')                // 1
map.has('a')                // true

set.forEach((v) => console.log(`${v}`))
for (const k of map.keys()) {       // ArkTS 禁用解构，不能用 for (const [k, v] of map)
  console.log(`${k}=${map.get(k)}`)
}
```

## 8.4 异常处理

try/catch/finally 处理运行时异常，throw 主动抛出：

```ts
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('除数不能为 0')
  }
  return a / b
}

try {
  const r = divide(10, 0)
  console.log(`${r}`)
} catch (e) {
  // 关键约束：catch 子句不能标注类型
  // catch (e: Error) 会编译报错，因为 any/unknown 被禁、异常无法标注类型
  console.error(`出错: ${e}`)
} finally {
  console.log('清理资源')   // 无论成败都执行
}
```

两条 ArkTS 特有约束：catch 子句省略类型标注，直接写 catch (e)；throw 只能抛 Error 或其子类对象，不能像 JS 那样抛任意值（throw 'error'、throw 42 都会报错）。

# 9. 类型断言与空安全

## 9.1 as 断言与类型守卫

```ts
// as：告诉编译器「按这个类型处理」
let value: Object = 'hello'
let len: number = (value as string).length

// typeof：运行时类型判断（收窄联合类型）
function process(v: number | string): void {
  if (typeof v === 'number') {
    console.log(v.toFixed(1))
  } else {
    console.log(v.toUpperCase())
  }
}

// instanceof：判断类实例（收窄类层次）
function describe(obj: Animal | Machine): void {
  if (obj instanceof Animal) {
    obj.makeSound()
  } else {
    obj.start()
  }
}
```

as 断言不做运行时检查，断言错误会在访问属性时崩溃，使用前应确保类型正确。

## 9.2 可选链与非空断言

```ts
interface Profile {
  address?: string
}

interface User {
  profile?: Profile
  name: string
}

let user: User | null = null

// 可选链 ?.：链路上任一环节为 null/undefined 就短路返回 undefined
let addr: string | undefined = user?.profile?.address

// 空值合并兜底
let display: string = user?.name ?? '匿名用户'

// 非空断言 !：确定不为 null 时使用，断言错则运行时崩溃
let name: string = user!.name
```

使用习惯：可选链 + ?? 是安全组合；非空断言 ! 只在「业务逻辑保证非空」时使用，比如 @Link 的初始化、地图查询后立即判空处理的场景。

# 10. 并发模型

## 10.1 线程模型与事件循环

ArkTS 采用「单线程 UI + 多线程任务」模型。主线程（UI 线程）跑事件循环处理渲染和交互，耗时任务必须放到子线程，否则阻塞 UI 造成丢帧。跨线程内存默认不共享——普通对象跨线程传递要序列化拷贝；想共享数据用 Sendable 对象。

## 10.2 TaskPool 与 Worker

| 维度 | TaskPool | Worker |
| ---- | ---- | ---- |
| 线程生命周期 | 系统自动管理，按需创建销毁 | 手动创建，常驻 |
| 任务模型 | 独立任务，支持优先级 | 消息驱动，长期通信 |
| 数据传递 | 支持序列化传输、Sendable 共享 | 序列化消息 |
| 适用场景 | 短耗时离散任务（解析、压缩、IO） | 长期后台任务（轮询、监听、复杂计算常驻） |

```ts
import { taskpool } from '@kit.ArkTS'

// @Concurrent 标记可在子线程执行的函数
@Concurrent
function computeSum(nums: number[]): number {
  let sum = 0
  for (const n of nums) {
    sum += n
  }
  return sum
}

@Entry
@Component
struct ThreadPoolPage {
  @State result: string = ''

  async runTask(): Promise<void> {
    const task = new taskpool.Task(computeSum, [1, 2, 3, 4, 5])
    const sum = await taskpool.execute(task) as number
    this.result = `结果: ${sum}`
  }

  build() {
    Column() {
      Text(this.result)
      Button('计算').onClick(() => this.runTask())
    }
  }
}
```

Worker 的用法：

```ts
import { worker } from '@kit.ArkTS'

// 主线程
const workerInstance = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets')
workerInstance.postMessage({ type: 'start', payload: 42 })
workerInstance.onmessage = (e) => {
  console.log(`收到: ${e.data}`)
}
workerInstance.terminate()   // 不用时销毁

// MyWorker.ets（子线程入口）
workerThreadInstance.onmessage = (e) => {
  workerThreadInstance.postMessage(`处理完成: ${e.data.payload}`)
}
```

## 10.3 Sendable 共享

默认对象跨线程要序列化拷贝，大数据（如大数组、图片缓冲）拷贝开销大。Sendable 是 ArkTS 的跨线程共享对象机制：标记为 @Sendable 的类可以跨线程直接传递引用，约束是布局固定、方法不变。

```ts
@Sendable
export class ImageData {
  width: number = 0
  height: number = 0
  pixels: ArrayBuffer = new ArrayBuffer(0)
}
```

@Sendable 类的约束：只能包含字段和方法，字段类型必须是可共享类型（基础类型、Sendable 类、ArrayBuffer 等），不能有闭包捕获。适合线程间传递大块只读或低频写数据。

# 11. ArkTS 与 TypeScript 的差异

## 11.1 为什么要约束

TS 的一切动态特性都建立在 JS 引擎之上；ArkTS 的目标是编译成高效字节码跑在 ArkVM 上。凡是阻碍静态分析、影响对象布局固定的特性都被裁掉。理解这一点，所有约束都能推导出来：动态 → 无法优化 → 禁止。

## 11.2 禁用特性清单

| 禁用的 TS 特性 | ArkTS 替代做法 | 原因 |
| ---- | ---- | ---- |
| `any` / `unknown` 类型 | 显式 interface / class / 联合类型 | 类型必须完全确定 |
| `var` 声明 | `let` / `const` | 消除变量提升的不确定性 |
| 对象字面量无类型 | 字面量必须对应 interface / class 类型 | 对象布局编译期固定 |
| 动态增删属性（`obj[key]`、`delete`、`with`） | 固定对象结构，用 `Map` 存动态键值 | 属性偏移量需静态确定 |
| `for...in` | `for...of` / `Object.keys()` | 遍历语义与布局固定冲突 |
| 结构化类型（structural typing） | 显式 `implements` / `extends` | 类型关系显式化，避免隐式兼容 |
| `#` 私有字段 | `private` 关键字 | 统一私有实现机制 |
| `Symbol()` API | 字符串或枚举作键 | 运行时 Symbol 影响优化 |
| TS 自定义装饰器 | ArkUI 内置装饰器体系 | 装饰器是编译器指令，不开放自定义 |
| 条件类型、映射类型等高级类型 | 具体的显式类型 | 编译期类型计算开销大、收益小 |
| 声明合并（同名 interface 合并） | 单一定义 | 消除全局命名不确定性 |
| 解构赋值 / 解构变量声明 / 解构参数 | 逐项取值、单独传参 | 与固定对象布局语义冲突 |
| `Function.apply / call / bind` | 直接调用或箭头函数包装 | 运行时动态 this 绑定破坏静态分析 |
| 生成器函数（`function*`） | 手动迭代器 class（hasNext/next） | 暂停恢复语义难以静态优化 |
| 函数与静态方法内使用 `this` | 仅在实例方法中使用 this | this 动态绑定无法静态确定 |

给 TS 开发者的迁移心法：把「随手写对象字面量」改成「先定义 interface 再标注类型」；把「对象当 Map 用」改成真正的 Map；把「any 过渡」改成「具体类型」。其余语法基本原样可用。

## 11.3 常见报错场景

```ts
// 1. 对象字面量缺类型
// let user = { name: 'Tom' }              // 报错
interface User { name: string }
let user: User = { name: 'Tom' }           // 正确

// 2. 动态属性
// obj['newKey'] = 1                       // 报错
let dict: Map<string, number> = new Map()
dict.set('newKey', 1)                      // 正确

// 3. 宽松相等
// if (a == b) {}                          // 编译告警/报错
if (a === b) {}                            // 正确
```

---

## 附：高频速记

- ArkTS = TS 严格子集；.ets 文件；编译为 .abc 字节码跑在 ArkVM。
- 禁 any/unknown/var/for...in/delete/动态属性/#私有字段/结构化类型；一律显式类型。
- number 统一整数浮点；元组固定长度；联合类型 + typeof 收窄；字面量类型约束有限选项。
- 箭头函数捕获外层 this，事件回调必用；class 字段先声明后使用，对象布局不可运行时更改。
- 泛型不变型；模块用 export/import，系统能力从 @kit 导入。
- 恒用 ===；?? 只兜 null/undefined，|| 兜所有假值；可选链 ?. 与空值合并 ?? 是标准安全组合。
- 函数可重载（多签名 + 联合类型实现体）；闭包捕获变量引用而非快照；对象字面量必须标注 interface/class 类型。
- 工具类型仅 Partial/Required/Readonly/Record 四个；Record 下标访问返回 V | undefined 需判空。
- 异常处理：catch 子句不标注类型，throw 只能抛 Error；break/continue 控制循环流程。
- 与 JS/TS 互操作兜底用 ESObject（替代 any，应尽量避免）。
- 并发：主线程单线程事件循环；TaskPool 离散任务（@Concurrent 函数），Worker 常驻通信；@Sendable 类跨线程共享引用（布局固定约束）。
