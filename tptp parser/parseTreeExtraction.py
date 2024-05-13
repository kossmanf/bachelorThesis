# this file contains function to extract infomration from the parse tree

# Recursively retrieves operators of a specified type from a parse tree.
def getOP(node, opType):
    # Collects operators of the specified type.
    operators = []
    # Recursively traverse child nodes.
    for childNode in node.nodes:
        # merge already collected operators with the curren operator
    	operators = operators + getOP(childNode, opType)
    
    # If current node matches specified operator type, append the operator.
    if(node.value['opType'] == opType):
        operators.append(node.value['op'])

    # return the collected operators
    return operators