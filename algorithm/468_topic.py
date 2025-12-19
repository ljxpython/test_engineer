"""

给定一个字符串 queryIP。如果是有效的 IPv4 地址，返回 "IPv4" ；如果是有效的 IPv6 地址，返回 "IPv6" ；如果不是上述类型的 IP 地址，返回 "Neither" 。

有效的IPv4地址 是 “x1.x2.x3.x4” 形式的IP地址。 其中 0 <= xi <= 255 且 xi 不能包含 前导零。例如: “192.168.1.1” 、 “192.168.1.0” 为有效IPv4地址， “192.168.01.1” 为无效IPv4地址; “192.168.1.00” 、 “192.168@1.1” 为无效IPv4地址。

一个有效的IPv6地址 是一个格式为“x1:x2:x3:x4:x5:x6:x7:x8” 的IP地址，其中:

1 <= xi.length <= 4
xi 是一个 十六进制字符串 ，可以包含数字、小写英文字母( 'a' 到 'f' )和大写英文字母( 'A' 到 'F' )。
在 xi 中允许前导零。
例如 "2001:0db8:85a3:0000:0000:8a2e:0370:7334" 和 "2001:db8:85a3:0:0:8A2E:0370:7334" 是有效的 IPv6 地址，而 "2001:0db8:85a3::8A2E:037j:7334" 和 "02001:0db8:85a3:0000:0000:8a2e:0370:7334" 是无效的 IPv6 地址。



示例 1：

输入：queryIP = "172.16.254.1"
输出："IPv4"
解释：有效的 IPv4 地址，返回 "IPv4"
示例 2：

输入：queryIP = "2001:0db8:85a3:0:0:8A2E:0370:7334"
输出："IPv6"
解释：有效的 IPv6 地址，返回 "IPv6"
示例 3：

输入：queryIP = "256.256.256.256"
输出："Neither"
解释：既不是 IPv4 地址，又不是 IPv6 地址


提示：

queryIP 仅由英文字母，数字，字符 '.' 和 ':' 组成。



这题的解题思路:
根据.和:区分是ipv4还是ipv6
ipv4的要求:
四段
xi不能前导零
范围: 0 <= xi <= 255
ipv6的要求:
每个xi长度在0到4位数之间
可以前导零
范围: 包含数字、小写英文字母( 'a' 到 'f' )和大写英文字母( 'A' 到 'F' )


"""

class Solution(object):
    def validIPAddress(self, queryIP):
        """
        :type queryIP: str
        :rtype: str
        """
        if '.' in queryIP:
            parts = queryIP.split('.')
            if len(parts) != 4:
                return "Neither"
            for part in parts:
                if not part:
                    return "Neither"
                if not part.isdigit():
                    return "Neither"
                if len(part) > 0 and part[0] =='0':
                    return "Neither"
                if int(part) < 0 or int(part) >255:
                    return "Neither"
            return "IPv4"
        elif ':' in queryIP:
            parts = queryIP.split(':')
            if len(parts) != 8:
                return "Neither"
            hex_chars = set('0123456789abcdefABCDEF')
            for part in parts:
                if len(part) < 0 or len(part) >4:
                    return "Neither"
                for c in part:
                    if c not in hex_chars:
                        return "Neither"
            return "IPv6"
        else:
            return "Neither"