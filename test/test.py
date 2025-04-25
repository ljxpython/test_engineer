



class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def removeElements(self, head, val):
        """
        删除链表
        :type head: Optional[ListNode]
        :type val: int
        :rtype: Optional[ListNode]
        """
        # 建立一个虚拟头部节点
        dummy_haed = ListNode(next=head)

        current = dummy_haed.next
        while current:
            if current.val == val:
                current.next = current.next.next
        return dummy_haed.next

    def reverseList(self, head):
        '''
        反转链表的
        三个值
        abc
        a-b-c-d-none

        链表的特性就是 val 和 next

        我们反转应该有一个顺序
        比如第一次反转，我们应该先从 none a b
        :param head:
        :return:
        '''
        # 第一次
        prev = None
        current = head

        # 当什么时候就停止呢？应该是判断到 current.next == None的时候吧
       # 判断的标准是当前值是否存在，而不是下一个节点
        while current.next:
            tmp = current.next
            # 反转主要是指针的变化, a->b->c   :    a<-b<-c
            # 也就是 current 先变化 然后 tmp,但也要注意保存之前指针指向的值, # 每次只做一个操作，把当前的指针修改为上一个prev
            current.next = prev
            # 之后为了下一次迭代做准备
            prev = current
            current = tmp
        return prev