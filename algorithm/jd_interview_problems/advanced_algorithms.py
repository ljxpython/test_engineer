# 京东测试开发补充算法题

## 栈和队列相关

def is_valid_parentheses(s):
    """
    有效的括号 (LeetCode 20)
    京东面试高频题，考察栈的应用
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    
    return not stack

def implement_queue_using_stacks():
    """
    用栈实现队列 (LeetCode 232)
    考察数据结构转换能力
    """
    class MyQueue:
        def __init__(self):
            self.stack1 = []  # 输入栈
            self.stack2 = []  # 输出栈
        
        def push(self, x):
            self.stack1.append(x)
        
        def pop(self):
            if not self.stack2:
                while self.stack1:
                    self.stack2.append(self.stack1.pop())
            return self.stack2.pop() if self.stack2 else None
        
        def peek(self):
            if not self.stack2:
                while self.stack1:
                    self.stack2.append(self.stack1.pop())
            return self.stack2[-1] if self.stack2 else None
        
        def empty(self):
            return not self.stack1 and not self.stack2
    
    return MyQueue()

## 二叉树相关

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    """
    二叉树的最大深度 (LeetCode 104)
    京东面试常考基础题
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def level_order(root):
    """
    二叉树的层序遍历 (LeetCode 102)
    考察队列和BFS应用
    """
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for i in range(level_size):
            node = queue.pop(0)
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result

## 排序和搜索

def quick_sort(arr):
    """
    快速排序实现
    京东面试可能要求手写排序算法
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

def binary_search(nums, target):
    """
    二分查找 (LeetCode 704)
    京东面试高频算法题
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

## 哈希表应用

def two_sum(nums, target):
    """
    两数之和 (LeetCode 1)
    京东面试经典入门题
    """
    hash_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    
    return []

def first_unique_char(s):
    """
    字符串中的第一个唯一字符 (LeetCode 387)
    考察哈希表统计应用
    """
    char_count = {}
    
    # 第一次遍历：统计字符出现次数
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # 第二次遍历：找到第一个出现一次的字符
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    
    return -1

## 动态规划入门

def climb_stairs(n):
    """
    爬楼梯 (LeetCode 70)
    京东面试动态规划入门题
    """
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

def max_subarray(nums):
    """
    最大子序和 (LeetCode 53)
    京东面试经典DP题
    """
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

## 京东电商场景算法

def calculate_discount(price, discount_type, discount_value):
    """
    电商促销价格计算
    京东业务场景算法题
    """
    if discount_type == 'percentage':
        return price * (1 - discount_value / 100)
    elif discount_type == 'fixed':
        return max(price - discount_value, 0)
    elif discount_type == 'buy_x_get_y':
        # 买X送Y逻辑
        return price  # 简化实现
    else:
        return price

def inventory_allocation(inventory, orders):
    """
    库存分配算法
    京东核心业务逻辑
    """
    allocation_result = {}
    remaining_inventory = inventory.copy()
    
    for order_id, order_items in orders.items():
        can_fulfill = True
        allocation = {}
        
        # 检查库存是否充足
        for item_id, quantity in order_items.items():
            if remaining_inventory.get(item_id, 0) < quantity:
                can_fulfill = False
                break
        
        if can_fulfill:
            # 分配库存
            for item_id, quantity in order_items.items():
                remaining_inventory[item_id] -= quantity
                allocation[item_id] = quantity
            allocation_result[order_id] = {'status': 'fulfilled', 'allocation': allocation}
        else:
            allocation_result[order_id] = {'status': 'insufficient_inventory', 'allocation': {}}
    
    return allocation_result, remaining_inventory

# 测试用例
def test_advanced_algorithms():
    print("=== 京东补充算法题测试 ===")
    
    # 1. 有效括号测试
    print("\n1. 有效括号测试")
    test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
    for case in test_cases:
        result = is_valid_parentheses(case)
        print(f"'{case}': {result}")
    
    # 2. 二叉树测试
    print("\n2. 二叉树最大深度测试")
    # 创建测试二叉树: [3,9,20,null,null,15,7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    depth = max_depth(root)
    print(f"二叉树最大深度: {depth}")
    
    # 3. 排序测试
    print("\n3. 快速排序测试")
    arr = [3, 6, 8, 10, 1, 2, 1]
    sorted_arr = quick_sort(arr)
    print(f"排序结果: {sorted_arr}")
    
    # 4. 哈希表测试
    print("\n4. 两数之和测试")
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"两数之和结果: {result}")
    
    # 5. 动态规划测试
    print("\n5. 爬楼梯测试")
    for n in range(1, 6):
        ways = climb_stairs(n)
        print(f"爬{n}级楼梯有{ways}种方法")
    
    # 6. 电商场景测试
    print("\n6. 库存分配测试")
    inventory = {'item1': 100, 'item2': 50, 'item3': 200}
    orders = {
        'order1': {'item1': 30, 'item2': 20},
        'order2': {'item1': 80, 'item3': 100},
        'order3': {'item2': 40}
    }
    
    allocation, remaining = inventory_allocation(inventory, orders)
    print(f"分配结果: {allocation}")
    print(f"剩余库存: {remaining}")

if __name__ == "__main__":
    test_advanced_algorithms()