from collections import deque
from typing import List, Optional
class Tree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def build_tree_bfs(values: List[Optional[int]], index: int = 0):
    if index >= len(values) or values[index]== None:
        return
    
    curr = Tree(values[index])

    curr.left= build_tree_bfs(values, index*2 +1)
    curr.right= build_tree_bfs(values, index*2 +2)

    return curr
    
    


# Example usage:
arr = [10,20,30,40,50,60,70,80,90,100]
root = build_tree_bfs(arr)
def print_tree_levels(root):
    """Print each level of the tree on its own line."""
    if not root:
        return
    
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(str(node.val))
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # Join and print all nodes in this level
        print("".join(level_nodes))  # or " ".join(level_nodes) for spacing


# Example: print the BFS-built tree
print_tree_levels(root)
