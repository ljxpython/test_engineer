# 二分法查找算法实现：https://programmercarl.com/0704.%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE.html#%E5%85%B6%E4%BB%96%E8%AF%AD%E8%A8%80%E7%89%88%E6%9C%AC

# 力扣题目： https://leetcode.cn/problems/binary-search/description/
'''
二分查找法：
    什么是二分查找法呢？
        在有限的有序的数组中，查找目标值的一种方法
        取中间的值，然后判断，缩小查找范围到其左右两个区间，之后不断迭代查找
    什么情况下适合呢？
        上面我说的概念应该已经描述的很清楚了


'''
class Solution(object):
    def search(self, nums:list, target:int):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left,right = 0, len(nums)-1 # 定义target在左闭右开的区间里，即：[left, right]
        while left <= right:
            middle = left + (right - left)//2
            if nums[middle] < target:
                left = middle + 1
            elif nums[middle] > target:
                right = middle - 1
            else:
                return middle
        return -1

# 二分法的变体题目
# https://leetcode.cn/problems/search-insert-position/description/
# 题解：https://programmercarl.com/0035.%E6%90%9C%E7%B4%A2%E6%8F%92%E5%85%A5%E4%BD%8D%E7%BD%AE.html#%E5%85%B6%E4%BB%96%E8%AF%AD%E8%A8%80%E7%89%88%E6%9C%AC



# 二分法的变体题目二: 34. 在排序数组中查找元素的第一个和最后一个位置
# https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/description/



    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        left, right = 0, len(nums) - 1  # 定义target在左闭右开的区间里，即：[left, right]
        while left <= right:
            middle = left + (right - left) // 2
            if nums[middle] < target:
                left = middle + 1
            elif nums[middle] > target:
                right = middle - 1
            else:
                print(middle)
                # nums 中存在 target，则左右滑动指针，来找到符合题意的区间
                left, right = middle, middle
                # 向左滑动，找左边界
                while left - 1 >= 0 and nums[left - 1] == target: left -= 1
                # 向右滑动，找右边界
                while right + 1 < len(nums) and nums[right + 1] == target: right += 1
                return [left,right]
        return [-1 ,-1]

# 二分查找法变体题目三： 求 x 的平方根
# https://leetcode.cn/problems/sqrtx/description/

# 二分查找法变体题目四： ：367. 有效的完全平方数
# https://leetcode.cn/problems/valid-perfect-square/description/



if __name__ == '__main__':
    s = Solution()
    # resp = s.search([-1,0,3,5,9,12],12)
    resp = s.searchRange([1],1)
    print(resp)