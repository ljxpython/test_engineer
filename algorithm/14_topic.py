"""

编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。



示例 1：

输入：strs = ["flower","flow","flight"]
输出："fl"
示例 2：

输入：strs = ["dog","racecar","car"]
输出：""
解释：输入不存在公共前缀。


提示：

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] 如果非空，则仅由小写英文字母组成


"""


class Solution(object):
    def longestCommonPrefix(self, strs:list[str]):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ''

        # 把第一个字符串当成前缀
        prefix = strs[0]
        for i in strs:
            while not i.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ''

        return prefix


