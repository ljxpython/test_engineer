"""

题目描述：
给定一个含有 n 个正整数的数组和一个正整数 target，找出该数组中满足其和 ≥ target 的长度最小的连续子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。

示例：
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2（子数组 [4,3] 的和为 7，长度最短）
解题思路：
通常使用滑动窗口（双指针）方法，时间复杂度为 O(n)，空间复杂度为 O(1)。


"""

from typing import List

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        n = len(nums)
        min_length = float('inf')
        current_sum = 0
        for right in range(n):
            current_sum += nums[right]
            if current_sum >= target:
                min_length = min(min_length,right-left+1)
                # 缩小窗口
                current_sum -= nums[left]
                left += 1
        return min_length if min_length != float('inf') else 0


