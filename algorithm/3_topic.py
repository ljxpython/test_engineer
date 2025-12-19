"""
给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。



示例 1:

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。


提示：

0 <= s.length <= 5 * 104
s 由英文字母、数字、符号和空格组成

思路:
快慢指针
滑动窗口

"""


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        # 快慢指针解法
        n = len(s)
        # 定义最长子串的长度
        max_len = 0
        # i 作为子串的起始指针（慢指针）
        for i in range(n):
            sub_str = ''
            j = i  # j 作为扩展子串的快指针
            # 注意条件是 j < n，避免索引越界
            while j < n and s[j] not in sub_str:
                sub_str += s[j]
                j += 1
                max_len = max(max_len, len(sub_str))
        # 返回应该放在外层循环外面
        return max_len

    # 滑动窗口
    def other_solution(self,s):
        n = len(s)
        # 定义左边界
        left = 0
        # 定义最长边界
        max_len = 0
        # 定义窗口
        window = set()
        for right in range(n):
            while s[right] in window:
                window.remove(s[left])
                left += 1
            #扩展有边界
            window.add(s[right])
            # 最长子串长度
            max_len = max(max_len,right -left +1)
        return max_len


