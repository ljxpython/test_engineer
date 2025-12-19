"""

给你两个 版本号字符串 version1 和 version2 ，请你比较它们。版本号由被点 '.' 分开的修订号组成。修订号的值 是它 转换为整数 并忽略前导零。

比较版本号时，请按 从左到右的顺序 依次比较它们的修订号。如果其中一个版本字符串的修订号较少，则将缺失的修订号视为 0。

返回规则如下：

如果 version1 < version2 返回 -1，
如果 version1 > version2 返回 1，
除此之外返回 0。


示例 1：

输入：version1 = "1.2", version2 = "1.10"

输出：-1

解释：

version1 的第二个修订号为 "2"，version2 的第二个修订号为 "10"：2 < 10，所以 version1 < version2。

示例 2：

输入：version1 = "1.01", version2 = "1.001"

输出：0

解释：

忽略前导零，"01" 和 "001" 都代表相同的整数 "1"。

示例 3：

输入：version1 = "1.0", version2 = "1.0.0.0"

输出：0

解释：

version1 有更少的修订号，每个缺失的修订号按 "0" 处理。





题解:
感觉这道题要完成这几个步骤:
1. 先将版本号字符串按照点号分割成修订号列表
2. 遍历两个列表，比较每个修订号的大小
3. 根据比较结果返回相应的整数
感觉这里还要姐姐,如果没有s[x]时的场景,及两个列表比大小
"""


class Solution(object):
    def compareVersion(self, version1, version2):
        """
        :type version1: str
        :type version2: str
        :rtype: int
        """
        version1_list = version1.split('.')
        version2_list = version2.split('.')
        max_length = max(len(version1_list),len(version2_list))
        for i in range(max_length):
            v1 = int(version1_list[i]) if i < len(version1_list) else 0
            v2 = int(version2_list[i]) if i < len(version2_list) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


if __name__ == '__main__':
    s = '001'
    print(int(s))
    print(s[3])
