"""

给你一个非空数组，返回此数组中 第三大的数 。如果不存在，则返回数组中最大的数。



示例 1：

输入：[3, 2, 1]
输出：1
解释：第三大的数是 1 。
示例 2：

输入：[1, 2]
输出：2
解释：第三大的数不存在, 所以返回最大的数 2 。
示例 3：

输入：[2, 2, 3, 1]
输出：1
解释：注意，要求返回第三大的数，是指在所有不同数字中排第三大的数。
此例中存在两个值为 2 的数，它们都排第二。在所有不同数字中排第三大的数为 1 。


提示：

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1


进阶：你能设计一个时间复杂度 O(n) 的解决方案吗？


"""

class Solution(object):
    def thirdMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # 方法1：使用set去重然后排序（简单但时间复杂度不是O(n)）
        nums_set = set(nums)
        nums_set_sort = sorted(list(nums_set))
        n = len(nums_set_sort)
        if n <= 2:
            return nums_set_sort[-1]
        else:
            return nums_set_sort[-3]

    def best(self, nums):
        """
        方法2：一次遍历法（满足O(n)时间复杂度要求）
        注意：这里不需要显式去重，因为在更新逻辑中自然处理了重复元素
        """
        first = second = third = float('-inf')
        
        for num in nums:
            # 跳过重复数字（已经在first, second, third中的数字）
            if num in (first, second, third):
                continue
                
            if num > first:
                first, second, third = num, first, second
            elif num > second:
                second, third = num, second
            elif num > third:
                third = num
                
        # 如果找到了第三大的数，返回它；否则返回最大的数
        return third if third != float('-inf') else first


if __name__ == '__main__':
    # 测试用例
    s = Solution()
    
    # 示例1
    list1 = [3, 2, 1]
    print(f"输入: {list1}")
    print(f"输出: {s.best(list1)}")  # 应该输出 1
    
    # 示例2
    list2 = [1, 2]
    print(f"输入: {list2}")
    print(f"输出: {s.best(list2)}")  # 应该输出 2
    
    # 示例3 - 关键测试用例
    list3 = [2, 2, 3, 1]
    print(f"输入: {list3}")
    print(f"输出: {s.best(list3)}")  # 应该输出 1
    
    # 额外测试用例
    list4 = [1, 2, 2, 5, 3, 5]
    print(f"输入: {list4}")
    print(f"输出: {s.best(list4)}")  # 应该输出 2 (去重后是[1,2,3,5]，第三大是2)
    
    list5 = [1, 1, 1]
    print(f"输入: {list5}")
    print(f"输出: {s.best(list5)}")  # 应该输出 1