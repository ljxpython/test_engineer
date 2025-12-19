"""


给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：

左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
每个右括号都有一个对应的相同类型的左括号。


示例 1：

输入：s = "()"

输出：true

示例 2：

输入：s = "()[]{}"

输出：true

示例 3：

输入：s = "(]"

输出：false

示例 4：

输入：s = "([])"

输出：true

示例 5：

输入：s = "([)]"

输出：false



提示：

1 <= s.length <= 104
s 仅由括号 '()[]{}' 组成

两种正确的:
s = "([])"
s = "()[]{}"

"""

class Solution(object):
    def isValid(self, s):
        """
        这个题目可以这样考虑:
        使用栈的思路:
            接下来要处理什么情况下入栈什么情况下出站
            当匹配({[时入栈,其余情况出栈
        :type s: str
        :rtype: bool
        """
        # 仅由括号 '()[]{}' 组成
        bracket_map = {
            ')':"(",
            ']':'[',
            '}':'{'
        }
        stack = []
        for char in s:
            # 分为左括号和右括号
            # 右括号进行判断
            if char in bracket_map.keys():
                top_elment =  stack.pop() if stack else "#"
                if bracket_map[char] != top_elment:
                    return False
            else:
                stack.append(char)
        return not stack
