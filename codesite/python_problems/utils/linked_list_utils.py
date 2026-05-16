from typing import Optional, List


class ListNode:
    """
    Definition for singly-linked list.
    """

    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def build_linked_list(nums: List[int], cycle_position: int = -1) -> ListNode:
    """
    Build linked list with cycle from list.
    """
    anchor = node = ListNode()
    cycle_node = None

    for position, num in enumerate(nums):
        node.next = ListNode(num)
        node = node.next

        if position == cycle_position:
            cycle_node = node

    if cycle_node is not None:
        node.next = cycle_node

    return anchor.next


def serialize_linked_list(root: ListNode) -> List[int]:
    """
    Return linked list values in list.
    """
    values = []
    while root:
        values.append(root.val)
        root = root.next
    return values


def are_lists_equeal(root1: ListNode, root2: ListNode) -> bool:
    """
    Compare two linked lists value by value.
    """
    node1 = root1
    node2 = root2

    while node1 or node2:
        if node1 is None and node2 is None:
            return True
        elif (
            node1 is None or node2 is None or
            node1.val != node2.val
        ):
            return False

        node1 = node1.next
        node2 = node2.next
    return True
