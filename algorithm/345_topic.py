"""
给你一个字符串 s ，仅反转字符串中的所有元音字母，并返回结果字符串。

元音字母包括 'a'、'e'、'i'、'o'、'u'，且可能以大小写两种形式出现不止一次。



示例 1：

输入：s = "IceCreAm"

输出："AceCreIm"

解释：

s 中的元音是 ['I', 'e', 'e', 'A']。反转这些元音，s 变为 "AceCreIm".

示例 2：

输入：s = "leetcode"

输出："leotcede"



提示：

1 <= s.length <= 3 * 105
s 由 可打印的 ASCII 字符组成


"""

class Solution(object):
    def reverseVowels(self, s):
        """
        你的方法：收集元音再替换
        时间复杂度: O(n) - 需要遍历两次字符串
        空间复杂度: O(n) - 需要存储元音列表和字符列表
        :type s: str
        :rtype: str
        """
        # 改进1: 使用set而不是list来存储元音，提高查找效率
        vowels = set('aeiouAEIOU')
        
        # 收集所有元音字母
        vowel_list = []
        for char in s:
            if char in vowels:
                vowel_list.append(char)
        
        # 反转元音列表
        vowel_list.reverse()
        
        # 构建结果字符串
        result = []
        vowel_index = 0
        for char in s:
            if char in vowels:
                result.append(vowel_list[vowel_index])
                vowel_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def reverseVowels_optimized(self, s):
        """
        优化版本：双指针法（推荐）
        时间复杂度: O(n) - 只需遍历一次字符串
        空间复杂度: O(n) - 需要将字符串转换为列表
        :type s: str
        :rtype: str
        """
        vowels = set('aeiouAEIOU')
        s_list = list(s)  # 将字符串转换为列表以便修改
        left, right = 0, len(s) - 1
        
        while left < right:
            # 从左边找到元音字母
            while left < right and s_list[left] not in vowels:
                left += 1
            # 从右边找到元音字母
            while left < right and s_list[right] not in vowels:
                right -= 1
            
            # 交换两个元音字母
            if left < right:
                s_list[left], s_list[right] = s_list[right], s_list[left]
                left += 1
                right -= 1
        
        return ''.join(s_list)
    
    def reverseVowels_your_method(self, s):
        """
        保留你的原始方法并稍作改进
        :type s: str
        :rtype: str
        """
        # 使用set提高查找效率
        vowels = set('aeiouAEIOU')
        vowel_list = []
        
        # 收集所有元音字母
        for char in s:
            if char in vowels:
                vowel_list.append(char)
        
        # 反转元音列表
        vowel_list.reverse()
        
        # 转换为列表进行修改
        s_list = list(s)
        for i, char in enumerate(s_list):
            if char in vowels:
                s_list[i] = vowel_list.pop(0)  # 从前面取出元音
        
        return ''.join(s_list)
