# 京东面试题 - 数组去重 (LeetCode 26)

def remove_duplicates(nums):
    """
    删除有序数组中的重复项
    思路：双指针法，一个指针遍历，一个指针记录不重复元素位置
    """
    if not nums:
        return 0
    
    # slow指针指向下一个不重复元素应该存放的位置
    slow = 1
    
    # fast指针用于遍历数组
    for fast in range(1, len(nums)):
        # 当遇到不重复的元素时，将其放到slow位置
        if nums[fast] != nums[fast - 1]:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow

# 测试用例
def test_remove_duplicates():
    # 测试用例1：正常情况
    nums1 = [1, 1, 2, 2, 3, 4, 4, 5]
    result1 = remove_duplicates(nums1)
    print(f"测试1: 输入{[1, 1, 2, 2, 3, 4, 4, 5]}")
    print(f"结果: 长度={result1}, 数组={nums1[:result1]}")
    
    # 测试用例2：无重复元素
    nums2 = [1, 2, 3, 4, 5]
    result2 = remove_duplicates(nums2)
    print(f"测试2: 输入{[1, 2, 3, 4, 5]}")
    print(f"结果: 长度={result2}, 数组={nums2[:result2]}")
    
    # 测试用例3：全部重复
    nums3 = [1, 1, 1, 1]
    result3 = remove_duplicates(nums3)
    print(f"测试3: 输入{[1, 1, 1, 1]}")
    print(f"结果: 长度={result3}, 数组={nums3[:result3]}")
    
    # 测试用例4：空数组
    nums4 = []
    result4 = remove_duplicates(nums4)
    print(f"测试4: 输入{[]}")
    print(f"结果: 长度={result4}, 数组={nums4[:result4]}")

if __name__ == "__main__":
    test_remove_duplicates()