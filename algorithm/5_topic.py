"""

给你一个字符串 s，找到 s 中最长的 回文 子串。



示例 1：

输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
示例 2：

输入：s = "cbbd"
输出："bb"



"""

class Solution(object):
    def longestPalindrome(self, s:str):
        """
        :type s: str
        :rtype: str
        """
        # 特殊情况处理
        if not s:
            return ""
        if len(s) == 1:
            return s

        # 定义最长回文子串的起始位置和长度
        start, max_length = 0, 1
        n = len(s)
        
        # 中心扩展算法
        def expand_around_center(left, right):
            # 当左右指针在有效范围内且指向的字符相同时，继续扩展
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            # 返回有效回文的起始位置和长度
            return left + 1, right - left - 1
        
        # 遍历每个可能的中心点
        for i in range(n):
            # 奇数长度回文，以单个字符为中心
            left1, len1 = expand_around_center(i, i)
            # 偶数长度回文，以两个字符之间为中心
            left2, len2 = expand_around_center(i, i + 1)
            
            # 更新最长回文子串
            if len1 > max_length:
                start, max_length = left1, len1
            if len2 > max_length:
                start, max_length = left2, len2
        
        # 返回最长回文子串
        return s[start:start + max_length]