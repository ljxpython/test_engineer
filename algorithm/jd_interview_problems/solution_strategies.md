# 京东测试开发面试算法题 - 解题思路总结

## 核心解题方法论

### 1. 双指针技巧
**适用场景**：数组、链表、字符串的遍历和修改
**核心思想**：使用两个指针以不同速度或方向遍历，解决一类问题

**常见应用**：
- 数组去重：快慢指针
- 链表环检测：快慢指针
- 字符串反转：左右指针
- 两数之和：左右指针

### 2. 哈希表法
**适用场景**：快速查找、去重、计数
**核心思想**：用空间换时间，O(1)时间复杂度查找

**常见应用**：
- 字符串中第一个唯一字符
- 两数之和
- 数组交集
- 有效的字母异位词

### 3. 递归与迭代
**适用场景**：树、链表等递归结构
**核心思想**：将大问题分解为小问题

**常见应用**：
- 链表反转
- 二叉树遍历
- 斐波那契数列
- 爬楼梯问题

## 具体题目解题模板

### 数组类题目模板
```python
def array_template(nums):
    # 1. 边界条件处理
    if not nums or len(nums) == 0:
        return 0
    
    # 2. 初始化指针/变量
    slow = 0
    
    # 3. 遍历处理
    for fast in range(len(nums)):
        # 满足条件时处理
        if condition:
            nums[slow] = nums[fast]
            slow += 1
    
    # 4. 返回结果
    return slow
```

### 链表类题目模板
```python
def linked_list_template(head):
    # 1. 边界条件
    if not head or not head.next:
        return head
    
    # 2. 初始化指针
    prev = None
    current = head
    
    # 3. 遍历处理
    while current:
        # 保存下一个节点
        next_temp = current.next
        # 处理当前节点
        current.next = prev
        # 移动指针
        prev = current
        current = next_temp
    
    return prev
```

### 字符串类题目模板
```python
def string_template(s):
    # 1. 转换为列表（如果需要修改）
    chars = list(s)
    
    # 2. 双指针处理
    left, right = 0, len(chars) - 1
    while left < right:
        # 交换或其他处理
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    
    # 3. 转换回字符串
    return ''.join(chars)
```

## 测试开发特殊考点

### 1. 边界条件处理
```python
def test_boundary_conditions():
    # 空值处理
    assert func(None) == expected_none
    
    # 单个元素
    assert func([1]) == expected_single
    
    # 重复元素
    assert func([1, 1, 1]) == expected_duplicate
    
    # 最大值最小值
    assert func([sys.maxsize, -sys.maxsize]) == expected_extreme
```

### 2. 异常处理机制
```python
def func_with_exception_handling(data):
    try:
        # 主要逻辑
        result = main_logic(data)
        return result
    except TypeError as e:
        # 类型错误处理
        return handle_type_error(e)
    except ValueError as e:
        # 值错误处理
        return handle_value_error(e)
    except Exception as e:
        # 其他异常处理
        return handle_general_error(e)
```

### 3. 测试用例设计思路
```python
def comprehensive_test_cases():
    test_cases = [
        # 正常情况
        {"input": normal_input, "expected": normal_output},
        
        # 边界情况
        {"input": boundary_input, "expected": boundary_output},
        
        # 异常情况
        {"input": invalid_input, "expected": error_response},
        
        # 性能测试
        {"input": large_input, "expected": performance_output},
    ]
    
    for case in test_cases:
        result = func(case["input"])
        assert result == case["expected"], f"Test failed for {case['input']}"
```

## 高频考点速记

### 必会算法（按优先级）
1. **数组去重** - 快慢指针
2. **链表反转** - 迭代+递归
3. **字符串反转** - 双指针
4. **二分查找** - 左右指针
5. **有效的括号** - 栈的应用
6. **合并两个有序链表** - 双指针
7. **二叉树遍历** - 递归+迭代

### 时间复杂度速查
- 数组遍历：O(n)
- 链表操作：O(n)
- 二分查找：O(log n)
- 哈希表操作：O(1)
- 排序算法：O(n log n)

### 空间复杂度优化
- 原地修改：O(1)
- 递归调用：O(n)（调用栈）
- 哈希表：O(n)

## 面试技巧

### 1. 思考过程表达
- 先理解题目，确认理解正确
- 说出暴力解法，再思考优化
- 解释算法思路，画图辅助
- 分析时间空间复杂度

### 2. 代码编写规范
- 变量命名清晰
- 添加必要注释
- 处理边界条件
- 主动写测试用例

### 3. 测试思维体现
- 考虑异常情况
- 设计测试用例
- 关注代码覆盖率
- 性能测试意识