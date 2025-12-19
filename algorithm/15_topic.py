"""
https://leetcode.cn/problems/3sum/description/
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。


示例 1：

输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
示例 2：

输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。
示例 3：

输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。

注意审题,元素可以相同,但是索引不能相同
"""


class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # 排序一下后更加容易,固定一个值,然后使用双指针
        nums.sort()
        result = []
        n = len(nums)

        # 固定一个值,然后找合适的内容
        for i in range(n-2):  # 修改这里
            # 定义两个指针
            left = i + 1
            right = n - 1
            if nums[i] > 0:
                # 这种情况可以直接跳出循环
                break
            # 去重
            if i > 0 and nums[i] == nums[i-1]:
                continue

            while left < right:
                total = nums[i] + nums[left] + nums[right]
                # total 过大和过小的情况去除掉
                if total > 0:
                    right -= 1
                elif total < 0:
                    left += 1
                # 下面是符合的情况
                else:
                    # 将值记录到result中
                    result.append([nums[i] , nums[left], nums[right]])
                    # 去重处理
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    left += 1
                    right -= 1

        return result


if __name__ == '__main__':
    solve = Solution()
    nums = [-1,-1,2,1]
    resp = solve.threeSum(nums=nums)
    print(resp)