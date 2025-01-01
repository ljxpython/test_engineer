# 二分法查找算法实现：https://programmercarl.com/0704.%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE.html#%E5%85%B6%E4%BB%96%E8%AF%AD%E8%A8%80%E7%89%88%E6%9C%AC

# 力扣题目： https://leetcode.cn/problems/binary-search/description/

class Solution(object):
    def search(self, nums:list, target:int):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left,right = 0, len(nums)-1 # 定义target在左闭右开的区间里，即：[left, right)
        while left < right:
            middle = left + (right - left)//2
            if nums[middle] < target:
                left = middle  # target在右区间，所以[middle + 1, right]
            elif nums[middle] > target:
                right = middle  # target在左区间，所以[left, middle - 1]
            else:
                return middle
        return -1



if __name__ == '__main__':
    s = Solution()
    resp = s.search([-1,0,3,5,9,12],2)
    print(resp)