"""
459. 重复的子字符串

题目描述：
给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。
给定的字符串只含有小写英文字母，并且长度不超过10000。

示例 1:
输入: "abab"
输出: True
解释: 可由子字符串 "ab" 重复两次构成。

示例 2:
输入: "aba"
输出: False

示例 3:
输入: "abcabcabcabc"
输出: True
解释: 可由子字符串 "abc" 重复四次构成。 (或者子字符串 "abcabc" 重复两次构成。)

解题思路：
如果一个字符串s是由重复的子串构成的，那么将两个s拼接在一起（s+s），
然后去掉首尾字符，得到的字符串中仍然包含原始的s。
"""

class Solution(object):
    def repeatedSubstringPattern(self, s):
        """
        :type s: str
        :rtype: bool
        
        巧妙解法：如果s包含重复子串，那么在(s+s)[1:-1]中一定能找到s
        """
        return s in (s + s)[1:-1]

def explain_solution():
    """
    详细解释这个巧妙的解法
    """
    print("459. 重复的子字符串 - 解法详解")
    print("="*50)
    
    # 示例1：包含重复子串的情况
    s1 = "abab"
    print(f"示例1: s = '{s1}' (包含重复子串)")
    print(f"s + s = '{s1 + s1}'")
    print(f"(s+s)[1:-1] = '{(s1 + s1)[1:-1]}'")
    print(f"'{s1}' in '{(s1 + s1)[1:-1]}' = {s1 in (s1 + s1)[1:-1]}")
    print(f"结果: {Solution().repeatedSubstringPattern(s1)}")
    print()
    
    # 示例2：不包含重复子串的情况
    s2 = "aba"
    print(f"示例2: s = '{s2}' (不包含重复子串)")
    print(f"s + s = '{s2 + s2}'")
    print(f"(s+s)[1:-1] = '{(s2 + s2)[1:-1]}'")
    print(f"'{s2}' in '{(s2 + s2)[1:-1]}' = {s2 in (s2 + s2)[1:-1]}")
    print(f"结果: {Solution().repeatedSubstringPattern(s2)}")
    print()
    
    # 示例3：更复杂的例子
    s3 = "abcabc"
    print(f"示例3: s = '{s3}' (包含重复子串)")
    print(f"s + s = '{s3 + s3}'")
    print(f"(s+s)[1:-1] = '{(s3 + s3)[1:-1]}'")
    print(f"'{s3}' in '{(s3 + s3)[1:-1]}' = {s3 in (s3 + s3)[1:-1]}")
    print(f"结果: {Solution().repeatedSubstringPattern(s3)}")
    print()

def visualize_concept():
    """
    可视化解释这个概念
    """
    print("原理解析:")
    print("="*30)
    
    s = "abab"
    print(f"原始字符串 s = '{s}'")
    print(f"可以分解为子串 'ab' 重复 2 次")
    print()
    
    print("构造 s + s:")
    doubled = s + s
    print(f"'{s}' + '{s}' = '{doubled}'")
    print()
    
    print("去头去尾 (s+s)[1:-1]:")
    trimmed = doubled[1:-1]
    print(f"去掉首尾字符: '{trimmed}'")
    print()
    
    print("分析为什么在包含重复子串的情况下能找到原始字符串:")
    print(f"原始 s:   |a|b|a|b|")
    print(f"第一个 s:  a|b|a|b|")
    print(f"第二个 s:     a|b|a|b|")
    print(f"拼接结果:  a|b|a|b|a|b")
    print(f"去头去尾:   |b|a|b|a|")
    print(f"原始 s:      |a|b|a|b|  (在去头去尾的字符串中找到)")
    print()
    
    print("对于不包含重复子串的情况 'aba':")
    s2 = "aba"
    doubled2 = s2 + s2
    print(f"'{s2}' + '{s2}' = '{doubled2}'")
    print(f"去头去尾: '{doubled2[1:-1]}'")
    print(f"原始 s '{s2}' 无法在这个去头去尾的字符串中找到")
    print()

def prove_concept():
    """
    数学证明为什么这个方法有效
    """
    print("数学证明:")
    print("="*20)
    print("如果 s 由长度为 k 的子串重复 n 次构成，则 s = pattern * n")
    print("s + s = pattern * n + pattern * n = pattern * 2n")
    print("去掉首尾字符后，我们移除了 pattern 的首字符和末字符")
    print("剩余部分包含 pattern * (2n - 2) + pattern[1:-1] + pattern[1:-1]")
    print("由于 n >= 2，剩余部分仍然包含完整的 pattern * (2n-2)，足以重构原始 s")
    print()
    print("如果 s 不包含重复子串，则 s + s 去头去尾后无法重构原始 s")
    print("因为没有重复模式可以用来重新构建原始字符串")

# 测试函数
def test_solution():
    sol = Solution()
    test_cases = [
        ("abab", True),
        ("aba", False),
        ("abcabcabcabc", True),
        ("a", False),
        ("aa", True),
        ("ababab", True),
        ("abcabcab", False)
    ]
    
    print("测试结果:")
    print("="*20)
    for s, expected in test_cases:
        result = sol.repeatedSubstringPattern(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{s}' -> {result} (期望: {expected})")

if __name__ == "__main__":
    explain_solution()
    visualize_concept()
    prove_concept()
    test_solution()