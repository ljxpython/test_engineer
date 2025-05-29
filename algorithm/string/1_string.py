

'''
滑动窗口类的题解:

我喜欢把问题归类,但是不喜欢思维定势,不喜欢不思考直接套题解,我希望你能真正的懂一道算法题的思想,而不是套题解 :

绝大部分滑动窗口类题目本质上真的不算是难题，经过有效的训练就可以熟练掌握。给大家分享一套滑动窗口的思维框架 (共五步-五连鞭)，非常好记和容易理解。掌握它之后，你可以一口气秒杀12道中等难度 的同类型题目 (卧槽？12道？是的，而且给全解析，再不点赞还是人？)，从而帮助你再遇见滑动窗口类型题目的时候不再胆怯！

PS：在这里我就不教大家什么是滑动窗口啦，这个概念并不难，leetcode上类似的科普文也有很多，所以我就不班门弄斧了。如果读者完全没有听说过这个概念，烦请先花10分钟弄懂个大概后再来阅读本文

废话不多说，直接上框架 (伪代码)

class Solution:
    def problemName(self, s: str) -> int:
        # Step 1: 定义需要维护的变量们 (对于滑动窗口类题目，这些变量通常是最小长度，最大长度，或者哈希表)
        x, y = ..., ...

        # Step 2: 定义窗口的首尾端 (start, end)， 然后滑动窗口
        start = 0
        for end in range(len(s)):
            # Step 3: 更新需要维护的变量, 有的变量需要一个if语句来维护 (比如最大最小长度)
            x = new_x
            if condition:
                y = new_y


            ------------- 下面是两种情况，读者请根据题意二选1 -------------

            # Step 4 - 情况1
            # 如果题目的窗口长度固定：用一个if语句判断一下当前窗口长度是否达到了限定长度
            # 如果达到了，窗口左指针前移一个单位，从而保证下一次右指针右移时，窗口长度保持不变,
            # 左指针移动之前, 先更新Step 1定义的(部分或所有)维护变量
            if 窗口长度达到了限定长度:
                # 更新 (部分或所有) 维护变量
                # 窗口左指针前移一个单位保证下一次右指针右移时窗口长度保持不变

            # Step 4 - 情况2
            # 如果题目的窗口长度可变: 这个时候一般涉及到窗口是否合法的问题
            # 如果当前窗口不合法时, 用一个while去不断移动窗口左指针, 从而剔除非法元素直到窗口再次合法
            # 在左指针移动之前更新Step 1定义的(部分或所有)维护变量
            while 不合法:
                # 更新 (部分或所有) 维护变量
                # 不断移动窗口左指针直到窗口再次合法

        # Step 5: 返回答案
        return ...






'''



"""
1. 无重复字符的最长子串

题目:给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

"""

from collections import defaultdict


# 暴力解法:

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        '''
        第一次从第一个元素开始查找,查找其对应的最小子串
        从第二个元素查找
        :param s:
        :return:
        '''
        if len(s)==1:
            return 1
        length = 0
        sub_str = ''
        left = 0
        while left < len(s):
            for i in s[left::]:
                if i not in sub_str:
                    sub_str += i
                else:
                    length = max(len(sub_str),length)
                    sub_str = ''
                    break
            left += 1
        return length


# 双指针解法
# 解题思路: https://leetcode.cn/problems/longest-substring-without-repeating-characters/solutions/876061/yi-ge-mo-ban-miao-sha-10dao-zhong-deng-n-sb0x
class Solution1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        '''
        双指针的解法就是快慢指针
        我们需要注意的是,什么时候慢指针移动

        pwwkew为例
        1. 开始快慢指针在p的位置,之后快指针移动到w,在移动到下一个w的时候,慢指针判断有重复的,所以慢指针要移动过去到第二个w的位置
        2. 接着快指针再次移动当移动到第三个w的之后停下,快指针进行操作

        综上,也就是快指针遇到与之前相同的元素时,慢指针就开始换位置了,我们要保证窗口里面的值都是不重复的,这就是本题的思路了


        :param s:
        :return:
        '''

        # 定义快慢指针
        fast = 0
        slow = 0
        # 最小子串
        sub_str = ''
        # 最长子串长度
        min_len = 0
        print(s)
        for index,i in enumerate(s):
            # print(i,index)
            # fast = i
            if i not in sub_str:
                sub_str += i
                print("当前sub_str:",sub_str)
                min_len = max(len(sub_str), min_len)
            else:
                # 先记录子串的长度
                # print(sub_str)
                min_len = max(len(sub_str),min_len)
                sub_str += i
                print(f"sub_str:{sub_str}, del:{i}")
                # 慢指针移动过来
                # print(sub_str)
                print(s[slow:index])
                for slow_index,j in enumerate(s[slow:index]):
                    if j == i :
                        # 如果相等,则删除子串的该元素,跳出循环
                        sub_str = sub_str[1:]
                        print(sub_str)
                        slow += 1
                        break
                    if j != i:
                        # 如果不相等,则代表需要删除该元素,继续循环
                        sub_str = sub_str[1:]
                        print(sub_str)
                        slow += 1
                    # 记录慢指针的位置
                    # slow = slow_index
                print("删除后:",sub_str)
        # print(sub_str)
        return min_len



# 20.有效括号
# https://leetcode.cn/problems/valid-parentheses/
class Solution2(object):
    def isValid(self, s:str):
        """
        这个题目可以这样考虑:
        使用栈的思路:
            接下来要处理什么情况下入栈什么情况下出站
            当匹配({[时入栈,其余情况出栈
        :type s: str
        :rtype: bool
        """
        if len(s) == 1:
            return False
        left_list = []
        str_map = {
            "(":")",
            "{":"}",
            "[":"]",
            "}":"{",
            ")": "(",
            "]": "[",
        }
        for i in s:
            # 入栈情况
            if i in "({[":
                left_list.append(i)
            # 出栈考虑
            else:
                # 判断最后一个元素是否为预期值
                if left_list:
                    if i == str_map[left_list[-1]]:
                        left_list.pop()
                    else:
                        return False
                else:
                    # 括号不匹配
                    return False
        # 最后如果全部匹配通过left_list应该为空
        if len(left_list) == 0:
            return True
        else:
            return False

# 两数之和
# https://leetcode.cn/problems/two-sum/
class Solution3(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        思路: 两层遍历,排除自己

        进阶思路: 滑动窗口
        """
        for index_a,a in enumerate(nums):
            for index_b,b in enumerate(nums):
                if index_b != index_a and a+b == target:
                    return [index_a,index_b]


# 206.反转链表
# https://leetcode.cn/problems/reverse-linked-list/
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution4(object):
    def reverseList(self, head:ListNode):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        a -> b -> c ->d

        cur = a
        pre = None

        1.
        tmp(b) = a.next

        2.
        a.next = pre

        3. next loop
        pre(a) = cur
        cur(b) = tmp
        none <- a   b(cur) -> c -> d

        """
        # 定义当前节点和下一个节点
        cur = head
        pre = None
        # 当有下一个节点时
        while cur:
            tmp = cur.next
            cur.next = pre
            # 调换 tmp 指向当前的值
            tmp.next = cur






if __name__ == '__main__':
    # s = "abcabcbb"
    # s = "bbbbb"
    # s = "pwwkew"
    # s = " "
    # s = 'au'
    # s = 'aabaab!bb'
    # length = Solution1().lengthOfLongestSubstring(s)
    # print(length)
    # print(len(" "))
    # for i in enumerate(s):
    #     print(i)
    # s = "([])"
    # s = "["
    # s = "){"
    # print(Solution2().isValid(s))
    nums = [3, 3]
    target = 6
    res = Solution3().twoSum(nums=nums,target=target)
    print(res)

