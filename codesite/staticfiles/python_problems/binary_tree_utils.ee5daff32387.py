from collections import deque
from typing import Optional, List  # Use types from typing


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
    """
    Definition for a binary tree node.
    """
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(node_list: List[int], node_type: TreeNode = TreeNode, with_lookup: bool = False) -> TreeNode:
    """
    Build binary tree from level order traversal list.

    If with_lookup=True, returns (root, lookup)
    where lookup is node value to node map.
    """
    # if tree.Node from binarytree is used
    # if node_type == tree.Node:
    #     return tree.build2(node_list)

    while node_list and node_list[-1] is None:
        node_list.pop()

    if not node_list:
        return None
    elif type(node_list) not in (list, tuple):
        raise TypeError(
            "Expected a list, got " + str(type(node_list).__name__)
        )

    root = node_type(node_list[0])
    queue = deque([root])
    index = 1
    lookup = {root.val: root} if with_lookup else None

    while index < len(node_list):
        node = queue.popleft()

        # Assign the left child if available
        if (
            index < len(node_list) and
            node_list[index] is not None
        ):
            node.left = node_type(node_list[index])
            queue.append(node.left)
            if with_lookup:
                lookup[node.left.val] = node.left
        index += 1

        # Assign the right child if available
        if (
            index < len(node_list) and
            node_list[index] is not None
        ):
            node.right = node_type(node_list[index])
            queue.append(node.right)
            if with_lookup:
                lookup[node.right.val] = node.right
        index += 1

    return (root, lookup) if with_lookup else root


def get_tree_values(root: TreeNode) -> List[int]:
    """
    Return tree node values in level order traversal format.
    """
    if not root:
        return []
    elif type(root) not in (TreeNode, ):
        raise TypeError("Expected tree node, got " + str(type(root).__name__))
    elif root.val == root.left == root.right == None:
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


def is_same_tree(root1: TreeNode, root2: TreeNode) -> bool:
    """
    Time complexity: O(n)
    Auxiliary space complexity: O(n)
    Tags: binary tree, dfs, recursion
    """
    def dfs(node1, node2):
        if node1 is None and node2 is None:
            return True
        elif node1 is None or node2 is None:
            return False

        if node1.val != node2.val:
            return False

        left = dfs(node1.left, node2.left)
        right = dfs(node1.right, node2.right)
        return left and right

    return dfs(root1, root2)
