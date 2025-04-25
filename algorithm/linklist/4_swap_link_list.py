'''
力扣题目 24
https://leetcode.cn/problems/swap-nodes-in-pairs/description/
链表交换
给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。
先把最简单的方法学会，之后太考虑比较难想到的迭代法

做链表题：比如删除链表，设计链表的增删改查，都可以考虑设置一个虚拟头节点

'''


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def swapPairs(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy_head = ListNode(next=head)
        # 做交换的条件就是存在第n个和第n+1个节点
        current = dummy_head # a
        while current.next and current.next.next:
            # 注意，改变节点的指向时，要保存好原有的值
            tmp1 = current.next # b
            tmp2 = current.next.next # c
            tmp3 = current.next.next.next # d
            # 比如我要调转的 b 和 c
            # (before)a->b->c->d-> : a->c->b->d->
            current.next = tmp2 # b
            current.next.next = tmp1 # c
            current.next.next.next = tmp3
            # 最后为了下一次循环做值的交换
            current = current.next.next
        return dummy_head.next
