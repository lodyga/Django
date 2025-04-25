from typing import Optional, List


class ListNode:
    """
    Definition for singly-linked list.
    """

    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def build_linked_list(numbers: List[int]):
    """
    Build linked list from list.
    """
    node = None
    for number in reversed(numbers):
        node = ListNode(number, node)
    return node


def get_linked_list_values(root):
    """
    Return linked list values in list.
    """
    values = []
    while root:
        values.append(root.val)
        root = root.next
    return values
