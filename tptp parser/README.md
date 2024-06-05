
# Parse tree processing scripts

This repository contains several Python scripts that manage and interact with parse tree data structures.

1. **parseTree.py**
   - Contains functions for  generating a parse tree based on a formula. 

2. **parseTreeExtraction.py**
   - Includes functions to extract specific information from a parse tree. It recursively retrieves operators of a specified type, collecting these as it traverses the tree.

3. **printTree.py**
   - Designed to print tree structures, focusing on inorder traversal. It provides functions for recursive traversal and node printing during the traversal process.

4. **treeDataStructure.py**
   - Defines a basic tree data structure for the parse tree in Python with a class `Node` that can store values and child nodes, supporting the creation and manipulation of tree-like structures.

5. **parseFormulas.py**
   - Takes the parse tree of a formula and a mapping for the the operators and a mapping form Adimen-SUMO Symbols to natural language and generates a sentence in natural language for the formula.

## Usage

Each script can be run independently, depending on the specific tree processing needs. Ensure that Python 3 is installed and that each script is in the same directory for proper module interaction.
