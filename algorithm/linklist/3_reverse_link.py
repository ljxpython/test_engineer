# 反转链表类题目
# https://leetcode.cn/problems/reverse-linked-list/description/
# 题解： https://leetcode.cn/problems/reverse-linked-list/solutions/1/206-fan-zhuan-lian-biao-shuang-zhi-zhen-r1jel/

'''
先说一下双指针的迭代法
反转链表说白了，就是指针不断换位置的方式，最终实现的结果就是，从做左到右的指针变成从右到左
那么思路就是：
    A -> B -> C -> D -> None

    定义 current  prev tmp
    最开始 从 head 的部分开始
    current -> tmp -> .... -> None(prev)
    经过第一次
    None(prev) <- current <- tmp ...

    最后：
    None <- A <- B <- C <- D


'''
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def reverseList(self, head):
        """
        双指针法(迭代法)
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        cur = head # 当前的节点
        pre = None # 前一个节点
        # 开始迭代
        while cur:
            # 最开始迭代时，保存头部的下个节点，之后局势当前要替换的下个节点
            tmp = cur.next
            # 改变当前指针的指向
            cur.next = pre
            # 前一个节点变成当前节点
            pre = cur
            # 当前节点移动到下一个节点
            cur = tmp
        return pre




