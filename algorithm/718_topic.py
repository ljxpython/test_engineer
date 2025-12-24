"""

718. 最长重复子数组

给两个整数数组 nums1 和 nums2 ，返回 两个数组中 公共的 、长度最长的子数组的长度 。



示例 1：

输入：nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
输出：3
解释：长度最长的公共子数组是 [3,2,1] 。
示例 2：

输入：nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]
输出：5


提示：

1 <= nums1.length, nums2.length <= 1000
0 <= nums1[i], nums2[i] <= 100
"""


class Solution(object):
    def findLength(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        # 暴力解法,两层循环,之后比较元素相同,如果相同就停下来

        n1 = len(nums1)
        n2 = len(nums2)
        max_length = 0
        for i in range(n1):
            for j in range(n2):
                k1 = i
                k2 = j
                sub_length = 0
                while k1 < n1 and k2 < n2 and nums1[k1] == nums2[k2]:
                    k1 += 1
                    k2 += 1
                    sub_length += 1  # 这里需要增加子数组长度
                    max_length = max(sub_length,max_length)


        return max_length

