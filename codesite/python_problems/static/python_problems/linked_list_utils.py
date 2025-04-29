from typing import Optional, List


class ListNode:
    """
    Definition for singly-linked list.
    """

    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def build_linked_list_deprecated(numbers: List[int]):
    """
    Build linked list from list.
    """
    node = None
    for number in reversed(numbers):
        node = ListNode(number, node)
    return node


def build_linked_list(numbers: List[int], cycle_position: int = None):
    """
    Build linked list with cycle from list.
    """
    anchor = node = ListNode()
    has_cycle = False

    for position, number in enumerate(numbers):
        node.next = ListNode(number)
        node = node.next
        
        if position == cycle_position:
            cycle_node = node
            has_cycle = True

    if has_cycle:
        node.next = cycle_node
    return anchor.next


def get_linked_list_values(root):
    """
    Return linked list values in list.
    """
    values = []
    while root:
        values.append(root.val)
        root = root.next
    return values
