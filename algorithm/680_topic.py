"""

给你一个字符串 s，最多 可以从中删除一个字符。

请你判断 s 是否能成为回文字符串：如果能，返回 true ；否则，返回 false 。



示例 1：

输入：s = "aba"
输出：true
示例 2：

输入：s = "abca"
输出：true
解释：你可以删除字符 'c' 。
示例 3：

输入：s = "abc"
输出：false


提示：

1 <= s.length <= 105
s 由小写英文字母组成


"""

class Solution(object):
    def validPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        # 首先检查原字符串是否就是回文
        if s == s[::-1]:
            return True

        # 遍历字符串，逐个删除字符后检查
        for i in range(len(s)):
            # 创建删除第i个字符后的字符串
            temp = s[:i] + s[i + 1:]
            # 检查是否为回文
            if temp == temp[::-1]:
                return True

        # 所有可能都尝试过，都不是回文
        return False

    def validPalindrome_two_pointers(self, s):
        """
        :type s: str
        :rtype: bool
        """

        # 辅助函数：检查字符串s在[left, right]区间内是否为回文
        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        # 初始化双指针
        left = 0
        right = len(s) - 1

        # 双指针向中间移动，寻找不匹配的位置
        while left < right:
            # 发现不匹配的字符
            if s[left] != s[right]:
                # 模拟删除左边字符：检查[left+1, right]区间
                # 模拟删除右边字符：检查[left, right-1]区间
                # 只要其中一种情况能构成回文，就返回True
                return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)

            # 字符匹配，继续移动指针
            left += 1
            right -= 1

        # 整个字符串都是回文
        return True
