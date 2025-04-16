from collections import deque

"""
Utility functions for binary tree operations in Python.

Provides:
- `TreeNode`: Basic binary tree node structure.
- `build_tree()`: Constructs a tree from a level-order traversal list.
- `get_tree_values()`: Returns tree values in level-order sequence.

Example:
    >>> root = build_tree([1, 2, 3, None, 4])
    >>> get_tree_values(root)
    [1, 2, 3, None, 4]
"""


class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(node_list, node_type=TreeNode):
    """
    Build binary tree from level-order traversal list.
    """
    # return tree.build(node_list)  # import binarytree as tree
    while node_list and node_list[-1] is None:
        node_list.pop()

    if not node_list:
        return []
    elif type(node_list) not in (list, tuple):
        raise TypeError("Expected a list, got " +
                        str(type(node_list).__name__))

    root = node_type(node_list[0])
    queue = deque([root])
    index = 1

    while index < len(node_list):
        node = queue.popleft()

        # Assign the left child if available
        if index < len(node_list) and node_list[index] is not None:
            node.left = node_type(node_list[index])
            queue.append(node.left)
        index += 1

        # Assign the right child if available
        if index < len(node_list) and node_list[index] is not None:
            node.right = node_type(node_list[index])
            queue.append(node.right)
        index += 1

    return root


def get_tree_values(root):
    """
    Return tree node values in level order traversal format.
    """
    # return root.values  # import binarytree as tree
    if not root:
        return []

    values = []
    queue = deque([root])

    while any(queue):
        queue_for_level = deque()
        while queue:
            node = queue.popleft()
            values.append(node.val if node else None)
            queue_for_level.append(node.left if node else None)
            queue_for_level.append(node.right if node else None)
        queue = queue_for_level

    while values[-1] is None:
        values.pop()
    return values
