# 删除链表元素题目
# https://leetcode.cn/problems/remove-linked-list-elements/description/
'''
链表有，单链表，双链表和环链表
我们就先说最简单的单链表,我们需要掌握的也就是单链表，其他的链表，我们理解
做链表题，有一个比较主要的思路就是，学会在初始化是，虚拟一个头部的节点，有的称之为哨兵节点
因为头节在操作时，是没有上一个节点的，如果虚拟一个头节点，就可以少考虑很多情况，把问题进行了统一


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
            # 如果值相等，那么我们把指针的指向改动一下
            if current.next.val == val:
                current.next = current.next.next
            # 如果不是我们寻找的值，那么下面相当于 a += 1，进入下一个节点的迭代
            else:
                current = current.next
        return dummy_head.next

# 变种题目： 删除链表倒数第n个节点
# https://leetcode.cn/problems/remove-nth-node-from-end-of-list/
    def removeNthFromEnd(self, head, n):
        """
        如果用暴力的做法，那么可能需要先遍历这个链表的长度，之后就可以查找到对应的第 n 个元素所对应的 index 了，
        之后再次删除这个元素，如果这样操作，那么时间复杂度为 O(n^2)
        下面我先实现这个，然后再用一次遍历的方式来完成
        :type head: Optional[ListNode]
        :type n: int
        :rtype: Optional[ListNode]
        """
        length = 0
        current = head
        while current:
            length += 1
            current.next = current
        # 所以我们需要第 index 个元素
        # 比如，我们需要删除倒数第二个元素 n = 2，链表的长度为 3，那么 index 其实为 1 即length -n
        index = length -n
        dummy_head = ListNode(next=head)
        need = dummy_head
        for i in range(index):
            need = need.next
        need.next = need.next.next
        return need

    def removeNthFromEnd_(self, head, n):
        """
        这道题还有双指针的解法
        怎么使用双指针呢？
        比如这个链表
        a -> b -> c -> d -> e : n = 2
        so i remove the
        fast slow
        fast move n+1 = 3 to c
        slow and fast move together
        until fast move  end
        fast to e
        slow to b

        :type head: Optional[ListNode]
        :type n: int
        :rtype: Optional[ListNode]
        """





if __name__ == '__main__':
    s = Solution()
    l = ListNode(val=1)
    l.next=ListNode(val=2)
    l.next.next = ListNode(val=3)
    resp = s.removeElements(head=l,val=2)
    print(resp)
        
