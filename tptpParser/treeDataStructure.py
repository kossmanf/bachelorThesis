# this file contains a tree data structure representation in python 

# tree representation
class Node:
    def __init__(self, value = None):
        # parameter which holds the child nodes
        self.nodes = []
        # parameter which holds the value of the node
        self.value = value