"""

541. 反转字符串 II
简单
相关标签
premium lock icon
相关企业
给定一个字符串 s 和一个整数 k，从字符串开头算起，每计数至 2k 个字符，就反转这 2k 字符中的前 k 个字符。

如果剩余字符少于 k 个，则将剩余字符全部反转。
如果剩余字符小于 2k 但大于或等于 k 个，则反转前 k 个字符，其余字符保持原样。


示例 1：

输入：s = "abcdefg", k = 2
输出："bacdfeg"
示例 2：

输入：s = "abcd", k = 2
输出："bacd"


提示：

1 <= s.length <= 104
s 仅由小写英文组成
1 <= k <= 104

"""


def reverseStr( s:str, k):
    """
    :type s: str
    :type k: int
    :rtype: str
    """

    def revers(text):
        left = 0
        right = len(text) -1
        while left <right:
            text[left], text[right] = text[right], text[left]
            left += 1
            right -= 1
        return text
    s_list = list(s)
    print(s_list)
    n = len(s)
    for i in range(0,n,2*k):
        print(i)
        s_list[i:i+2] = revers(s_list[i:i+2])
    return ''.join(s_list)

if __name__ == '__main__':
    s = "abcdefg"
    res =reverseStr(s,k=2)
    print(res)
    # list1 = [1,2,3,4,5,6]
    # print(list1[2:3])
    # list1[2:3] =[9]
    # print(list1)


