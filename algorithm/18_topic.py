"""

给你一个由 n 个整数组成的数组 nums ，和一个目标值 target 。
请你找出并返回满足下述全部条件且不重复的四元组 [nums[a], nums[b], nums[c], nums[d]]
（若两个四元组元素一一对应，则认为两个四元组重复）：

0 <= a, b, c, d < n
a、b、c 和 d 互不相同
nums[a] + nums[b] + nums[c] + nums[d] == target
你可以按 任意顺序 返回答案 。



示例 1：

输入：nums = [1,0,-1,0,-2,2], target = 0
输出：[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
示例 2：

输入：nums = [2,2,2,2,2], target = 8
输出：[[2,2,2,2]]


提示：

1 <= nums.length <= 200
-109 <= nums[i] <= 109
-109 <= target <= 109


"""


class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        # 排序数组以便使用双指针法和去重
        nums.sort()
        result = []
        n = len(nums)
        
        # 需要至少4个元素才能组成四元组
        if n < 4:
            return result
            
        # 固定第一个数
        for i in range(n - 3):
            # 去重：跳过重复的第一个数
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            # 提前剪枝：如果当前最小的四数之和都大于target，后面的都不可能满足
            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break
                
            # 提前剪枝：如果当前最大可能的四数之和都小于target，继续增大第一个数
            if nums[i] + nums[n - 3] + nums[n - 2] + nums[n - 1] < target:
                continue
                
            # 固定第二个数
            for j in range(i + 1, n - 2):
                # 去重：跳过重复的第二个数
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                    
                # 提前剪枝：如果当前最小的四数之和都大于target，后面的都不可能满足
                if nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > target:
                    break
                    
                # 提前剪枝：如果当前最大可能的四数之和都小于target，继续增大第二个数
                if nums[i] + nums[j] + nums[n - 2] + nums[n - 1] < target:
                    continue
                    
                # 使用双指针法寻找剩下的两个数
                left = j + 1
                right = n - 1
                
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    
                    if total == target:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        
                        # 去重：跳过重复的第三个数
                        while left < right and nums[left] == nums[left + 1]:
                            left += 1
                        # 去重：跳过重复的第四个数
                        while left < right and nums[right] == nums[right - 1]:
                            right -= 1
                            
                        # 移动指针继续寻找
                        left += 1
                        right -= 1
                    elif total < target:
                        # 和太小，移动左指针增大总和
                        left += 1
                    else:
                        # 和太大，移动右指针减小总和
                        right -= 1
                        
        return result


# 测试代码
if __name__ == '__main__':
    solution = Solution()
    
    # 测试用例1
    nums1 = [1, 0, -1, 0, -2, 2]
    target1 = 0
    result1 = solution.fourSum(nums1, target1)
    print(f"输入: nums = {nums1}, target = {target1}")
    print(f"输出: {result1}")
    print()
    
    # 测试用例2
    nums2 = [2, 2, 2, 2, 2]
    target2 = 8
    result2 = solution.fourSum(nums2, target2)
    print(f"输入: nums = {nums2}, target = {target2}")
    print(f"输出: {result2}")
    print()
    
    # 额外测试用例
    nums3 = [1, -2, -5, -4, -3, 3, 3, 5]
    target3 = -11
    result3 = solution.fourSum(nums3, target3)
    print(f"输入: nums = {nums3}, target = {target3}")
    print(f"输出: {result3}")