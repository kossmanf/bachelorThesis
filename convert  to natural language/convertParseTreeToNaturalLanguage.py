from tptpParser.parseTree import generateParseTree
from  tptpParser.parseTreeExtraction import getOP
from tptpParser.printTree import print_tree_inorder

# Function to split camel case words
def splitCamelCase(word):
    newWord = ''
    wordIndex = 0
    for i in range(0, len(word)):
        if(i == len(word)-1):
            newWord = newWord + word[wordIndex:len(word)]
        elif(i != 0 and word[i-1] != ' ' and word[i].isupper() and word[i+1].islower()):
            newWord = newWord + word[wordIndex:i] + ' '
            wordIndex = i
    return newWord

# Function to split words at underscores
def splitAtUnderscores(word):
    newWord = ''
    for subword in word.split('_'):
        if(subword != ''):
            newWord = newWord + subword + ' '
    newWord = newWord[0:-1]
    return newWord

# Function to generate natural language sentence from parse tree
def generateSentence(node, mapOperatorsToWords, wordMapping):
    sentence = ''
    
    # Recursively traverse all nodes in the parse tree

    # Handling parentheses
    if(node.value['opType'] == 'parentheses'):
        for childNode in node.nodes:
            sentence = sentence + generateSentence(childNode, mapOperatorsToWords, wordMapping)

    # Handling unary operators
    elif(node.value['opType'] == 'all' or node.value['opType'] == 'exists' or node.value['opType'] == 'not' or node.value['opType'] == 'true' or node.value['opType'] == 'false'):
        sentence = sentence + mapOperatorsToWords[node.value['opType']] + ' '
        sentence = sentence + generateSentence(node.nodes[0], mapOperatorsToWords, wordMapping)

    # Handling binary operators
    elif(node.value['opType'] == 'and' or node.value['opType'] == 'or' or node.value['opType'] == 'equal' or node.value['opType'] == 'notEQ' or node.value['opType'] == 'implies' or node.value['opType'] == 'equivalent'):
        sentence = sentence + generateSentence(node.nodes[0], mapOperatorsToWords, wordMapping) + ' '
        sentence = sentence + mapOperatorsToWords[node.value['opType']] + ' '
        sentence = sentence + generateSentence(node.nodes[1], mapOperatorsToWords, wordMapping)
    
    # Handling predicates and functions
    elif(node.value['opType'] == 'predicate' or node.value['opType'] == 'function'):
        predicateOrFunctionName = ''
        if(wordMapping.get(node.value['op'][0:-2])):
            predicateOrFunctionName = wordMapping.get(node.value['op'][0:-2])[0]
            predicateOrFunctionName = splitAtUnderscores(predicateOrFunctionName)
            predicateOrFunctionName = splitCamelCase(predicateOrFunctionName)
        else:
            predicateOrFunctionName = node.value['op'][0:-2].split('_')[-1]
            predicateOrFunctionName = splitCamelCase(predicateOrFunctionName)
        
        if(len(node.nodes) == 0):
            print(predicateOrFunctionName)
            sentence = sentence +  predicateOrFunctionName
        elif(node.nodes[0].value['opType'] != 'parameters'):
            sentence = sentence + predicateOrFunctionName + ' of ' + generateSentence(node.nodes[0], mapOperatorsToWords, wordMapping)
        elif(node.nodes[0].value['opType'] == 'parameters' and len(node.nodes[0].nodes) == 2):
            sentence = sentence + generateSentence(node.nodes[0].nodes[0], mapOperatorsToWords, wordMapping) + ' ' + predicateOrFunctionName + ' of ' + generateSentence(node.nodes[0].nodes[1], mapOperatorsToWords, wordMapping)
        else: 
            for childNode in node.nodes:
                sentence = sentence + generateSentence(childNode, mapOperatorsToWords, wordMapping)
    
    # Handling parameters
    elif(node.value['opType'] == 'parameters'):
        for childNode in node.nodes:
            sentence = sentence + generateSentence(childNode, mapOperatorsToWords, wordMapping)
            sentence = sentence + ' and '
        sentence = sentence[0:-5]

    # Handling variables and constants
    elif(node.value['opType'] == 'variable' or node.value['opType'] == 'constant'):
        if(wordMapping.get(node.value['term'])):
            predicateOrConstantName = wordMapping.get(node.value['term'])[0]
            predicateOrConstantName = splitAtUnderscores(predicateOrConstantName)
            predicateOrConstantName = splitCamelCase(predicateOrConstantName)
            sentence = sentence + predicateOrConstantName
        else:
            predicateOrConstantName = node.value['term'].split('_')[-1]
            predicateOrConstantName = splitCamelCase(predicateOrConstantName)
            sentence = sentence + predicateOrConstantName

    return sentence
