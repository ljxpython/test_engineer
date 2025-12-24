import random

class Solution(object):
    def findKthLargest(self, nums, k):
        """
        使用快速选择算法找第k个最大元素
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # 将问题转换：第k大 = 第(n-k+1)小 = 索引为n-k的元素
        n = len(nums)
        target_index = n - k  # 目标元素的索引
        
        # 使用快速选择算法在原数组上进行分区
        return self.quickSelect(nums, 0, n - 1, target_index)
    
    def quickSelect(self, nums, left, right, target_index):
        """
        快速选择算法核心函数
        在nums[left:right+1]中找第target_index小的元素
        """
        if left == right:
            # 只有一个元素，直接返回
            return nums[left]
        
        # 随机选择pivot避免最坏情况
        pivot_index = random.randint(left, right)
        
        # 分区操作，返回pivot的新位置
        pivot_index = self.partition(nums, left, right, pivot_index)
        
        if pivot_index == target_index:
            # 找到了目标位置的元素
            return nums[pivot_index]
        elif pivot_index < target_index:
            # 目标在右半部分
            return self.quickSelect(nums, pivot_index + 1, right, target_index)
        else:
            # 目标在左半部分
            return self.quickSelect(nums, left, pivot_index - 1, target_index)
    
    def partition(self, nums, left, right, pivot_index):
        """
        分区函数：将数组分为小于pivot和大于pivot的两部分
        返回pivot在分区后的新位置
        """
        # 获取pivot的值
        pivot = nums[pivot_index]
        
        # 将pivot移到数组末尾
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        
        # store_index指向"小于pivot"区域的下一个位置
        store_index = left
        
        # 遍历[left, right)范围，将小于pivot的元素移到左侧
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        # 将pivot放回正确位置
        nums[right], nums[store_index] = nums[store_index], nums[right]
        
        # 返回pivot的最终位置
        return store_index

# 详细演示快速选择算法执行过程
def demo_quickselect():
    """
    演示快速选择算法的执行过程
    """
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    
    print("="*60)
    print("快速选择算法演示 - 找第K个最大元素")
    print("="*60)
    print(f"原数组: {nums}")
    print(f"目标: 找第{k}大的元素")
    print(f"排序后: {sorted(nums, reverse=True)}")
    print(f"答案应该是: {sorted(nums, reverse=True)[k-1]}")
    print()
    
    # 转换问题：第k大 = 第(n-k+1)小 = 索引为n-k的元素
    n = len(nums)
    target_index = n - k  # 目标索引
    print(f"转换: 第{k}大元素 = 排序后索引为{n-k}的元素")
    print(f"即: 第{n-k+1}小的元素")
    print()
    
    # 模拟快速选择过程
    left, right = 0, n - 1
    nums_copy = nums[:]  # 创建副本避免修改原数组
    
    print(f"开始快速选择，目标索引: {target_index}")
    print(f"初始数组: {nums_copy}")
    print()
    
    # 手动模拟一次分区过程
    print("第一次分区:")
    pivot_index = 0  # 随机选择pivot
    pivot = nums_copy[pivot_index]
    print(f"选择pivot: nums[{pivot_index}] = {pivot}")
    
    # 执行分区
    nums_copy[pivot_index], nums_copy[right] = nums_copy[right], nums_copy[pivot_index]
    print(f"移到末尾后: {nums_copy}")
    
    store_index = left
    print(f"初始化store_index = {store_index}")
    
    for i in range(left, right):
        print(f"  检查nums[{i}] = {nums_copy[i]}")
        if nums_copy[i] < pivot:
            print(f"    {nums_copy[i]} < {pivot}, 交换到左侧")
            nums_copy[store_index], nums_copy[i] = nums_copy[i], nums_copy[store_index]
            print(f"    交换后: {nums_copy}")
            store_index += 1
        else:
            print(f"    {nums_copy[i]} ≥ {pivot}, 保持在右侧")
    
    # 将pivot放回正确位置
    nums_copy[right], nums_copy[store_index] = nums_copy[store_index], nums_copy[right]
    print(f"将pivot放回正确位置: {nums_copy}")
    pivot_final_pos = store_index
    print(f"pivot最终位置: {pivot_final_pos}")
    print()
    
    print(f"分区结果分析:")
    print(f"  左侧[{left}:{pivot_final_pos}]: {nums_copy[left:pivot_final_pos]} (小于{pivot})")
    print(f"  pivot位置[{pivot_final_pos}]: {nums_copy[pivot_final_pos]}")
    print(f"  右侧[{pivot_final_pos+1}:{right+1}]: {nums_copy[pivot_final_pos+1:right+1]} (大于等于{pivot})")
    print()
    
    if pivot_final_pos == target_index:
        print(f"找到目标! pivot位置{pivot_final_pos} = 目标索引{target_index}")
        print(f"第{k}大元素是: {nums_copy[pivot_final_pos]}")
    elif pivot_final_pos < target_index:
        print(f"pivot位置{pivot_final_pos} < 目标索引{target_index}")
        print(f"目标在右半部分[{pivot_final_pos+1}:{right+1}]")
    else:
        print(f"pivot位置{pivot_final_pos} > 目标索引{target_index}")
        print(f"目标在左半部分[{left}:{pivot_final_pos}]")

# 测试完整算法
def test_solution():
    sol = Solution()
    
    # 测试用例1
    nums1 = [3, 2, 1, 5, 6, 4]
    k1 = 2
    result1 = sol.findKthLargest(nums1[:], k1)  # 传入副本避免修改原数组
    print(f"测试1: nums={nums1}, k={k1} -> 第{k1}大元素: {result1}")
    
    # 测试用例2
    nums2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    k2 = 4
    result2 = sol.findKthLargest(nums2[:], k2)
    print(f"测试2: nums={nums2}, k={k2} -> 第{k2}大元素: {result2}")

demo_quickselect()
print()
test_solution()