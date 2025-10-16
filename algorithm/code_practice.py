"""
451
给定一个字符串 s ，根据字符出现的 频率 对其进行 降序排序 。一个字符出现的 频率 是它出现在字符串中的次数。


示例 1:

输入: s = "tree"
输出: "eert"
解释: 'e'出现两次，'r'和't'都只出现一次。
因此'e'必须出现在'r'和't'之前。此外，"eetr"也是一个有效的答案。

"""
from collections import Counter,defaultdict


class Solution(object):
    def frequencySort(self, s):
        """
        :type s: str
        :rtype: str
        """
        # 先统计,后排序
        # 字典 + 排序
        counter_dict = Counter(s)
        # 字典根据key或者value进行升序和降序排列
        sorted_chars = sorted(counter_dict.items(),key=lambda x:x[1],reverse=True)

        return ''.join(i[0]*i[1] for i  in sorted_chars)


if __name__ == '__main__':
    solve = Solution()
    str = 'tree'
    resp = solve.frequencySort(s=str)
    print(resp)