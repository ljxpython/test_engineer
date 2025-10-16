# 京东面试题 - 链表反转 (LeetCode 206)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    """
    反转链表
    思路：使用三个指针(prev, current, next)逐个节点反转
    """
    prev = None
    current = head
    
    while current:
        # 保存下一个节点
        next_temp = current.next
        # 反转当前节点的指向
        current.next = prev
        # 移动指针
        prev = current
        current = next_temp
    
    return prev

def reverse_list_recursive(head):
    """
    递归方式反转链表
    """
    # 递归终止条件
    if not head or not head.next:
        return head
    
    # 递归反转剩余部分
    reversed_head = reverse_list_recursive(head.next)
    
    # 调整指针关系
    head.next.next = head
    head.next = None
    
    return reversed_head

def create_linked_list(values):
    """创建链表"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head

def print_linked_list(head):
    """打印链表"""
    values = []
    current = head
    while current:
        values.append(current.val)
        current = current.next
    return values

# 测试用例
def test_reverse_list():
    print("=== 链表反转测试 ===")
    
    # 测试用例1：正常链表
    head1 = create_linked_list([1, 2, 3, 4, 5])
    print(f"原始链表: {print_linked_list(head1)}")
    reversed1 = reverse_list(head1)
    print(f"反转后: {print_linked_list(reversed1)}")
    
    # 测试用例2：单个节点
    head2 = create_linked_list([1])
    print(f"\n原始链表: {print_linked_list(head2)}")
    reversed2 = reverse_list(head2)
    print(f"反转后: {print_linked_list(reversed2)}")
    
    # 测试用例3：空链表
    head3 = create_linked_list([])
    print(f"\n原始链表: {print_linked_list(head3)}")
    reversed3 = reverse_list(head3)
    print(f"反转后: {print_linked_list(reversed3)}")
    
    # 测试递归方法
    head4 = create_linked_list([1, 2, 3, 4])
    print(f"\n递归反转测试")
    print(f"原始链表: {print_linked_list(head4)}")
    reversed4 = reverse_list_recursive(head4)
    print(f"反转后: {print_linked_list(reversed4)}")

if __name__ == "__main__":
    test_reverse_list()