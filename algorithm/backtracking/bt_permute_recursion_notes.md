# 全排列回溯过程中的递归与撤销笔记

> 记录一次学习回溯算法时的典型疑惑：
> 「为什么看起来好像撤销了两次？代码中只写了一次 `path.pop()`，
> 但讲解中却说：返回一层 → 撤销 3，再返回一层 → 撤销 2。」

---

## 一、相关代码片段（`bt_permute.py`）

```python
def backtrack() -> None:
    if len(path) == len(nums):
        res.append(path[:])
        return

    for i in range(len(nums)):
        if used[i]:
            continue

        used[i] = True
        path.append(nums[i])

        backtrack()      # 递归

        path.pop()       # 撤销本层刚刚 append 的那个数
        used[i] = False
```

表面现象：
- 代码里只写了一次 `path.pop()`；
- 讲解时却出现了「撤销 3，再撤销 2」之类的描述，看起来好像撤销了很多次。

核心疑惑：**为什么会出现“撤销两次”的效果？在代码里却只看到一个 `path.pop()`？**

---

## 二、关键点：每一层递归都有自己的那一次 `pop`

以 `nums = [1, 2, 3]` 为例，只看生成 `[1, 2, 3]` 这一条路径，给每一层 `backtrack` 编号：

- 第 0 层：最开始调用的 `backtrack()`，此时 `path = []`
- 第 1 层：在第 0 层中，选了 `1` 之后调用的 `backtrack()`，`path = [1]`
- 第 2 层：在第 1 层中，选了 `2` 之后调用的 `backtrack()`，`path = [1, 2]`
- 第 3 层：在第 2 层中，选了 `3` 之后调用的 `backtrack()`，`path = [1, 2, 3]`

到第 3 层时：

```python
if len(path) == len(nums):  # True，此时 path = [1, 2, 3]
    res.append(path[:])
    return                  # 返回到第 2 层
```

接下来发生的事情分两步：

### 1. 从第 3 层返回到第 2 层 → 撤销 3

从第 3 层 `return` 后，程序回到 **第 2 层** 的这两行之间：

```python
backtrack()      # 刚刚执行完第 3 层
path.pop()       # 现在轮到第 2 层自己的 pop 执行
```

- 第 2 层之前做过 `path.append(3)`，所以这里的 `path.pop()` 撤销的是 **数字 3**；
- `path` 从 `[1, 2, 3]` 变回 `[1, 2]`。

这就是讲解里说的：**「返回一层 → 撤销 3：path = [1, 2]」**。

### 2. 第 2 层结束，返回到第 1 层 → 再撤销 2

第 2 层的 `for` 循环没有更多可选项后，函数结束，`return` 回到 **第 1 层**。此时回到的是第 1 层的这两行之间：

```python
backtrack()      # 刚刚执行完第 2 层
path.pop()       # 现在轮到第 1 层自己的 pop 执行
```

- 第 1 层之前做过 `path.append(2)`，所以这里的 `path.pop()` 撤销的是 **数字 2**；
- `path` 从 `[1, 2]` 变回 `[1]`。

这就是讲解里说的：**「再撤销 2：path = [1]」**。

注意：
- **代码里并没有写两次 `pop`，只是“不同层各执行了一次自己的 `pop`”。**
- 每一层的结构都是：

  ```python
  path.append(当前层选择的数字)
  backtrack()          # 进入下一层
  path.pop()           # 撤销当前层选择的数字
  ```

  当从更深的递归返回时，各层会依次执行自己的 `path.pop()`，于是整体看起来就像「连续撤销了很多次」。

---

## 三、可以加打印辅助理解（可选）

为了更直观地看到这一点，可以给 `backtrack` 加一个 `depth` 参数，打印每一层的 `path`：

```python
def backtrack(depth=0):
    print("  " * depth, "进入 depth =", depth, "path =", path)

    if len(path) == len(nums):
        print("  " * depth, "收集结果", path)
        res.append(path[:])
        return

    for i in range(len(nums)):
        if used[i]:
            continue
        used[i] = True
        path.append(nums[i])

        backtrack(depth + 1)

        path.pop()
        used[i] = False
        print("  " * depth, "回到 depth =", depth, "path =", path)
```

运行 `permute([1, 2, 3])` 时，输出中每一行的 `depth` 和 `path` 就能清楚地展示：
- 进入更深一层时，`path` 如何增长；
- 返回时，每一层自己的 `pop` 如何依次把 `path` 撤回到上一状态。

---

## 四、最终结论

1. 回溯的“撤销”并不是写了很多次 `pop`，而是：**每一层函数都有一对 `append`/`pop`**；
2. 从最深层返回时，这些 `pop` 会按照「调用栈从深到浅」的顺序依次执行，看起来就像是“连续撤销多次”；
3. 可以把记忆简化成一句话：
   > 「每一层只负责撤销自己加的那个元素，整体效果就是从深到浅逐层恢复现场。」

当能理解这一点时，对“回溯 = 递归 + 状态恢复”的认知就基本到位了，后面对组合、子集、字符串回溯等题型的理解都会轻松很多。

---

## 五、关于“只有一个 for 循环，为什么能遍历所有排列？”的疑惑记录

疑问描述：
- 代码里只看到一处 `for i in range(len(nums)):`，看起来好像“只循环了一层”；
- 但结果中却包含了所有排列，感觉好像需要很多层嵌套 `for` 才能做到。

关键认知：
- 虽然代码文本里只写了一次 `for`，但**每调用一次 `backtrack()`，这一行 `for` 就会再执行一遍**；
- 不同递归层次上的 `backtrack()`，各自都有一份自己的 `for` 循环；
- 从整体效果来看，相当于写了多层嵌套的 `for`：
  - 第 0 层的 `for` 决定“第一位选什么”；
  - 第 1 层的 `for` 决定“第二位选什么”；
  - 第 2 层的 `for` 决定“第三位选什么”；
  - ……直到选满所有位置。

可以和“手写多重 for”进行类比：

```python
# 伪代码：3 重 for 枚举所有长度为 3 的排列（不考虑去重）
for a in nums:
    for b in nums:
        for c in nums:
            print(a, b, c)
```

递归版本则是：

```python
def backtrack():
    for i in range(len(nums)):
        # 选择 nums[i]
        backtrack()  # 让下一层去决定“下一位选什么”
```

区别在于：
- 多重 for 是“写死了有几层循环”；
- 递归 + 一个通用的 `for`，可以根据 `nums` 长度动态产生“任意层数的嵌套 for”。

最终总结：
1. **每一层 backtrack 调用都会执行一遍同样的 for 循环**，负责当前这一位的所有可能选择；
2. 递归调用负责“加深一层”，让下一层的 for 去决定下一位的选择；
3. 结束条件（`len(path) == len(nums)`）保证只在所有位置都被填满时收集结果；
4. 回溯中的“一个 for + 一个递归调用”本质上就等价于“任意层数的多重 for 枚举所有组合/排列”。
