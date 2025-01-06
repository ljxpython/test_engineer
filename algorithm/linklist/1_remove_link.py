# 删除链表元素题目
# https://leetcode.cn/problems/remove-linked-list-elements/description/
'''
链表有，单链表，双链表和环链表
我们就先说最简单的单链表
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
每个节点两个元素：值和下一个节点的指针


删除链表元素通用解题思路：
    1. 添加一个虚拟的头部，这样每次就不需要考虑删除头部的操作了
    那么删除的时候，就是，如果当前的下一个节点 val = target
    那么： node.next.val == target -> node.next = node.next.next (也就是跳过下一次的节点)





'''
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def removeElements(self, head:ListNode, val):
        """
        :type head: Optional[ListNode]
        :type val: int
        :rtype: Optional[ListNode]
        """
        dummy_head = ListNode(next=head)
        current = dummy_head
        while current.next:
            if current.next == val:
                current.next = current.next.next
            else:
                current = current.next
        return dummy_head.next


if __name__ == '__main__':
    s = Solution()
    l = ListNode(val=1)
    l.next=ListNode(val=2)
    l.next.next = ListNode(val=3)
    resp = s.removeElements(head=l,val=2)
    print(resp)
        
