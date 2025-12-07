from typing import Optional, List


class ListNode:
    """
    Definition for singly-linked list.
    """

    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def build_linked_list_deprecated(numbers: List[int]) -> ListNode:
    """
    Build linked list from list.
    """
    node = None
    for number in reversed(numbers):
        node = ListNode(number, node)
    return node


def build_linked_list(numbers: List[int], cycle_position: int = -1) -> ListNode:
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


def get_linked_list_values(root: ListNode) -> List[int]:
    """
    Return linked list values in list.
    """
    values = []
    while root:
        values.append(root.val)
        root = root.next
    return values


def are_linked_lists_equeal(root1: ListNode, root2: ListNode) -> bool:
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
