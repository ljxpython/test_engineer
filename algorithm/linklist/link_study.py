'''
链表，先说一下什么是链表吧
    1. 和数组不同，其实链表的在内存里面是不连续的，它由一个个节点组成，每个节点都指向下一个地址
    2. 链表的插入和删除只需要调整指针的顺序就可以了，而不需要对其他节点进行操作
    3. 链表有单链表，双链表和循环链表


'''


# 由上面的定义可以可以知道，每个节点有值和节点指向两个元素需要定义,我们可以做如下定义
class ListNode:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

# node 定义好之后，我们就可以尝试来定义一个链表了，链表就是有一个个 node 组成的
# 下面是一个单链表,我们需要实现什么功能，主要为链表的增删改查
class SingleLinkList:

    # 初始化链表时，头部为空
    def __init__(self):
        self.head = None

    # 判断链表是否为空


