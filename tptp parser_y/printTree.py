# Functions for printing a tree data structure.

# Print tree in inorder traversal.
# parse_tree: the parse tree to be printed
def print_tree_inorder(parse_tree):
    """Prints the tree in inorder traversal."""
    print('---------------------------------------------------')
    inorder_traversal(parse_tree)
    print('---------------------------------------------------')

# Traverse tree recursively inorder and print each node.
# node: the first node of the parse tree for traversing the tree recursively
def inorder_traversal(node):
    """Recursively traverses the tree inorder and prints each node."""
    # Print node value.
    print(node.value)

    # Recursively traverse child nodes.
    for child_node in node.nodes:
        inorder_traversal(child_node)