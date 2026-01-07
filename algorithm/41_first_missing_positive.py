def first_missing_positive(nums):
    """
    寻找数组中第一个缺失的正整数。
    
    力扣第 41 题: First Missing Positive
    算法思路: 原地哈希 (In-place Hash / Cyclic Sort)
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    n = len(nums)
    
    # 1. 原地置换: 将每个在 [1, n] 范围内的数字 x 放到索引 x-1 的位置上
    for i in range(n):
        # 使用 while 循环，因为交换回来的数可能也需要继续交换到正确位置
        # 条件1: 1 <= nums[i] <= n (只处理范围内正整数)
        # 条件2: nums[nums[i] - 1] != nums[i] (目标位置还没放对，也避免了重复值的死循环)
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            # 交换当前数字到它正确的位置
            target_idx = nums[i] - 1
            nums[i], nums[target_idx] = nums[target_idx], nums[i]
            
    # 2. 扫描数组: 第一个不满足 nums[i] == i + 1 的位置，对应的数字 i + 1 就是缺失的
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
            
    # 3. 如果 1 到 n 都齐了，那么缺失的就是 n + 1
    return n + 1

if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ([1, 2, 0], 3),                  # 正常排序缺失
        ([3, 4, -1, 1], 2),              # 包含负数和乱序
        ([7, 8, 9, 11, 12], 1),          # 连 1 都没有
        ([1, 1], 2),                     # 重复正数
        ([1, 1, 2, 2], 3),               # 多个重复
        ([-10, -5, 1, 3, 3, 2], 4),      # 负数 + 重复 + 乱序
        ([], 1)                          # 空数组
    ]
    
    print("开始算法测试 (LeetCode 41 - 第一个缺失的正数):")
    print("-" * 50)
    for nums, expected in test_cases:
        original_nums = nums.copy()
        result = first_missing_positive(nums.copy())
        status = "PASSED" if result == expected else "FAILED"
        print(f"输入: {original_nums}")
        print(f"预期结果: {expected}, 实际结果: {result} -> {status}")
        print("-" * 50)
