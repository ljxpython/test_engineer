"""

给定一组非负整数 nums，重新排列每个数的顺序（每个数不可拆分）使之组成一个最大的整数。

注意：输出结果可能非常大，所以你需要返回一个字符串而不是整数。



示例 1：

输入：nums = [10,2]
输出："210"
示例 2：

输入：nums = [3,30,34,5,9]
输出："9534330"


提示：

1 <= nums.length <= 100
0 <= nums[i] <= 109

https://leetcode.cn/problems/largest-number/solutions/716400/fu-xue-ming-zhu-zhuan-cheng-zi-fu-chuan-mm2s6/

"""


class Solution(object):
    def largestNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: str
        """
        from functools import cmp_to_key
        
        def compare(x, y):
            if x + y > y + x:
                return -1  # x 优先于 y
            elif x + y < y + x:
                return 1   # y 优先于 x
            else:
                return 0

        # 转化为字符串
        str_nums = [str(i) for i in nums]
        
        # 按自定义规则排序
        str_nums.sort(key=cmp_to_key(compare))
        
        # 处理全零情况
        if str_nums[0] == "0":
            return "0"
        
        res = ''.join(str_nums)
        return res