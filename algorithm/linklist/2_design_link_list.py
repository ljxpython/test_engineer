# 设计链表题目：https://leetcode.cn/problems/design-linked-list/description/

# 设计一个单链表和双链表，实现相关功能

# 这是一套比较基础的题目


# 单节点定义
class ListNode(object):
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

class MyLinkedList(object):

    def __init__(self):
        # 链表的基本元素，头和长度
        self.dummy_head = ListNode()
        self.size = 0

    def get(self, index):
        """
        获取链表中下标为 index 的节点的值。如果下标无效，则返回 -1 。
        :type index: int
        :rtype: int
        """
        # 先定义好异常的场景
        if index >= self.size or index<0:
            return -1
        current = self.dummy_head.next
        # 比如我想下标是 10，那么就是第 9 个 current的next，其 val 就是对应的值
        for i in range(index):
            current = current.next
        return current.val

    def addAtHead(self, val):
        """
        将一个值为 val 的节点插入到链表中第一个元素之前。在插入完成后，新节点会成为链表的第一个节点。
        :type val: int
        :rtype: None
        """
        # 我们可以在虚拟头部的下一个插入该值,之后长度记得+=1
        self.dummy_head.next = ListNode(val=val,next=self.dummy_head.next)
        self.size += 1

    def addAtTail(self, val):
        """
        将一个值为 val 的节点追加到链表中作为链表的最后一个元素。
        :type val: int
        :rtype: None
        """
        current = self.dummy_head
        while current.next:
            current = current.next
        current.next = ListNode(val=val)
        self.size += 1


    def addAtIndex(self, index, val):
        """
        将一个值为 val 的节点插入到链表中下标为 index 的节点之前。如果 index 等于链表的长度，那么该节点会被追加到链表的末尾。如果 index 比长度更大，该节点将 不会插入 到链表中。
        :type index: int
        :type val: int
        :rtype: None
        """

        if index < 0 or index > self.size:
            return
        current = self.dummy_head
        if index == self.size:
            while current.next:
                current = current.next
            current.next = ListNode(val=val)
            self.size += 1
        else:
            for i in range(index):
                current = current.next
            current.next = ListNode(val=val,next=current.next)
            self.size += 1



    def deleteAtIndex(self, index):
        """
        如果下标有效，则删除链表中下标为 index 的节点。
        :type index: int
        :rtype: None
        """
        if index < 0 or index >= self.size:
            return
        current = self.dummy_head
        for i in range(index):
            current = current.next
        # 下个节点就是需要删除的节点
        current.next = current.next.next
        # 删除完成记得size -=1
        self.size -= 1

'''
双链表：
    双链表和多链表相比，多了 prev 指向前面的指针

'''
class ListNode2(object):
    def __init__(self,val = 0 ,prev=None,next=None):
        self.val = val
        self.prev = prev
        self.next = next

class MyLinkList2(object):
    def __init__(self):
        '''
        双链表：相比于单链表，我们不需要使用虚拟头部了，而是用 self.prev
        '''
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, index):
        """
        获取链表中下标为 index 的节点的值。如果下标无效，则返回 -1 。
        :type index: int
        :rtype: int
        """
        if index < 0 or index >= self.size:
            return -1

        # 下面如果你不太清楚是不是:self.size - index -1,你不妨自己举一个例子，比如，倒数第二个元素应该如何取，最后一个元素应该如何取
        if index < self.size//2:
            current = self.head
            for i in range(index):
                current = current.next
        else:
            current = self.tail
            for i in range(self.size - index -1):
                current = current.prev



    def addAtHead(self, val):
        """
        将一个值为 val 的节点插入到链表中第一个元素之前。在插入完成后，新节点会成为链表的第一个节点。
        :type val: int
        :rtype: None
        """
        new_node = ListNode2(val=val,next=self.head)
        if self.head:
            # 插入到头部，相当于，newnode 没有头部了，self.head 指向了 new node
            self.head.prev = new_node
        else:
            # 对于尾部来说则是
            self.tail = new_node
        self.head = new_node
        self.size += 1


    def addAtTail(self, val):
        """
        将一个值为 val 的节点追加到链表中作为链表的最后一个元素。
        :type val: int
        :rtype: None
        """
        new_node = ListNode2(val=val,prev=self.head)
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1



    def addAtIndex(self, index, val):
        """
        将一个值为 val 的节点插入到链表中下标为 index 的节点之前。如果 index 等于链表的长度，那么该节点会被追加到链表的末尾。如果 index 比长度更大，该节点将 不会插入 到链表中。
        :type index: int
        :type val: int
        :rtype: None
        """
        if index <0 or index >self.size:
            return
        if index == 0:
            self.addAtHead(val=val)
        elif index == self.size:
            self.addAtTail(val=val)
        else:
            if index < self.size //2:
                current = self.head
                for i in range(index -1):
                    current = current.next
            else:
                current = self.tail
                for i in range(self.size -index):
                    current = current.prev
            new_node = ListNode2(val=val,prev=current,next=current.next)
            current.next.prev = new_node
            current.next = new_node
            self.size += 1





    def deleteAtIndex(self, index):
        """
        如果下标有效，则删除链表中下标为 index 的节点。
        :type index: int
        :rtype: None
        """
        if index < 0 or index >= self.size:
            return

        if index == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif index == self.size - 1:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            if index < self.size // 2:
                current = self.head
                for i in range(index):
                    current = current.next
            else:
                current = self.tail
                for i in range(self.size - index - 1):
                    current = current.prev
            current.prev.next = current.next
            current.next.prev = current.prev
        self.size -= 1

# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)