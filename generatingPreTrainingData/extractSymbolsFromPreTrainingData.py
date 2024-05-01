import os
import re
import math
import shutil
import subprocess
import json
from collections import Counter
from parseTree import generateParseTree
from parseTreeExtraction import getOP
from printTree import print_tree_inorder
from parseFormulas import generateSentence

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

# Loading word mapping from a JSON file
with open('./as_cn_mapping_test.json', 'r') as file:
    wordMapping = json.load(file)

# Function to map symbol names
def mapSymbolname(symbolName):
    if(wordMapping.get(symbolName)):
        return wordMapping.get(symbolName)[0]

# Function to extract symbols from a clause
def getSymbols(clause):
    symbols = []
    clauseParseTree = generateParseTree(clause)

    # Extracting function symbols
    functionSymbols = getOP(clauseParseTree, 'function')
    for functionSymbol in functionSymbols:
        if(mapSymbolname(functionSymbol[:-2])):
            functionSymbol = mapSymbolname(functionSymbol[:-2])
            functionSymbol = splitAtUnderscores(functionSymbol)
            functionSymbol = splitCamelCase(functionSymbol)
            symbols.append(functionSymbol)

    # Extracting constant symbols
    constantSymbols = getOP(clauseParseTree, 'constant')
    for constantSymbol in constantSymbols:
        if(mapSymbolname(constantSymbol)):
            constantSymbol = mapSymbolname(constantSymbol)
            constantSymbol = splitAtUnderscores(constantSymbol)
            constantSymbol = splitCamelCase(constantSymbol)
            symbols.append(constantSymbol)

    # Extracting predicate symbols
    predicateSymbols = getOP(clauseParseTree, 'predicate')
    for predicateSymbol in predicateSymbols:
        if(mapSymbolname(predicateSymbol[:-2])):
            predicateSymbol = mapSymbolname(predicateSymbol[:-2])
            predicateSymbol = splitAtUnderscores(predicateSymbol)
            predicateSymbol = splitCamelCase(predicateSymbol)
            symbols.append(predicateSymbol)
            
    return symbols

# Creating a list of all symbols from the word mapping
allSymbols = list(set([splitCamelCase(splitAtUnderscores(wordMapping[key][0])) for key in wordMapping]))

# Creating directories if they don't exist
if not os.path.exists('./extractedSymbols'):
    os.mkdir('./extractedSymbols')

if not os.path.exists('./extractedSymbolsLog'):
    os.mkdir('./extractedSymbolsLog')

# Creating a log file
if not os.path.exists('./extractedSymbolsLog/logFile'):
    open('./extractedSymbolsLog/logFile', 'w')

# Opening the log file for reading and appending
with open('./extractedSymbolsLog/logFile', 'r+') as proofLog:
    # Creating an array out of the log file with all proofs done so far
    proofsDone = [proof[:-1] for proof in proofLog.readlines()]

    # Removing the last done proof if one was done and redoing it in case it wasn't finished
    if(len(proofsDone) > 0):
        lastProofDone = proofsDone.pop()
        # If the proof file exists it will be removed 
        if os.path.exists(os.path.join('./extractedSymbols','extractedSymbols' + lastProofDone)):
            os.remove(os.path.join('./extractedSymbols','extractedSymbols' + proofsDone))

    # Looping through positive pre-training data
    for category in  os.listdir('./preTrainingData/posPreTrainingData'):
        for proof in os.listdir(os.path.join('./preTrainingData/posPreTrainingData', category)):

            # Creating a new file to write extracted symbols
            with open(os.path.join('./extractedSymbols','extractedSymbols' + proof[3:]), 'w') as file:
                if not proof[3:] in proofsDone:
                    documents = dict()
                    documents['documents'] = []

                    print('extracting symbols from proof: ' + proof[3:])
                    print('no: ' + str(len(proofsDone)+1))

                    posSymbols = []
                    negSymbols = []

                    # Opening positive pre-training data file
                    with open(os.path.join('./preTrainingData/posPreTrainingData', category, proof)) as proofFile:
                        posData = json.load(proofFile)
                        posClauses = posData[list(posData.keys())[0]]
                        # Extracting symbols from positive clauses
                        for posClause in posClauses:
                            posSymbols.extend(getSymbols(posClause))

                    # Checking if negative pre-training data file exists
                    if os.path.exists(os.path.join('./preTrainingData/negPreTrainingData', category, 'neg' + proof[3:])):
                        with open(os.path.join('./preTrainingData/negPreTrainingData', category, 'neg' + proof[3:])) as proofFile:
                            negData = json.load(proofFile)
                            negClauses = negData[list(negData.keys())[0]]
                            # Extracting symbols from negative clauses
                            for negClause in negClauses:
                                negSymbols.extend(getSymbols(negClause))
                            
                    # Filtering out symbols present in negative data from positive symbols
                    negSymbols = [negSymbol for negSymbol in negSymbols if negSymbol not in posSymbols]
                    
                    # Extracting symbols present in neither positive nor negative data
                    neutralSymbols = [symbol for symbol in allSymbols if symbol not in posSymbols and symbol not in negSymbols]

                    # Constructing documents dictionary
                    documents['documents'].append({
                        'proofName': proof,
                        'proofCategory': category,
                        'goal': list(posData.keys())[0],
                        'posSymbols': posSymbols,
                        'negSymbols': negSymbols,
                        'neutralSymbols': neutralSymbols
                    }) 
                    
                    # Writing the proof name in the log file
                    proofLog.write(proof[3:] + "\n")
                    proofLog.truncate()

                    # Writing the documents dictionary to the file
                    json.dump(documents, file)