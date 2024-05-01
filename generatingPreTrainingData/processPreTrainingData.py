
import os
import json
import math
from tqdm import tqdm
from tptpParser.parseTree import generateParseTree
from convertParseTreeToNaturalLanguage import generateSentence

# Function to calculate term frequency
def termFrequency(word, document):
    occurence = 0
    for wordInDocument in document:
        if(word == wordInDocument):
            occurence = occurence + 1
    if(occurence > 0):
        return 1 + math.log10(occurence)
    else:
        return 0

# Function to calculate the inverse document frequency
def inverseDocumentFrequency(word, documents):
    return math.log10(len(documents)/documentFrequency(word, documents))

# Function to calculate the document frequency
def documentFrequency(word, documents):
    frequency = 0
    for document in documents:
        if(word in document):
            frequency = frequency + 1
    return frequency

# Function to calculate the TF-IDF
def tfIdf(word, document, documents):
    return termFrequency(word, document) * inverseDocumentFrequency(word, documents) 

# Function to count word occurrences in a document
def countWordOccurencesInDocument(document):
    return {item: document.count(item) for item in document}

# Function to get minimum and maximum occurrences
def getMinMax(occurences):
    firstItter = False

    for element in occurences:
        if firstItter == False:
            min = occurences[element]
            max = occurences[element]
            firstItter = True

        if(occurences[element] > max):
            max = occurences[element]
        if(occurences[element] < min):
            min = occurences[element]
    
    return {'min':min, 'max':max}

# Function to normalize data
def normalizeData(data, domainMin, domainMax, rangeMin, rangeMax):
        if(domainMax - domainMin == 0):
            return rangeMin
        normalizedData = (((data-domainMin)*(rangeMax - rangeMin))/(domainMax - domainMin)) + rangeMin
        return normalizedData

# Creating directories if not exist
if not os.path.exists('./preTrainingDataCollection'):
    os.mkdir('./preTrainingDataCollection')

if not os.path.exists('./preTrainingDataCollectionLog'):
    os.mkdir('./preTrainingDataCollectionLog')
    open('./preTrainingDataCollectionLog/logFile', 'w')

# Loading word mapping and documents
with open('./as_cn_mapping_test.json', 'r') as file:
    wordMapping = json.load(file)

with open(os.path.join('./documents.json')) as file:
    documents = json.load(file)['documents']

# Mapping operators to verbal representations
mapOperatorsToWords = {
    'and': 'and', 
    'or': 'or', 
    'not': 'not', 
    'equal': 'is equal to', 
    'notEQ': 'is not equal to', 
    'equivalent': 'is equivalent to', 
    'implies': 'implies that', 
    'all': 'for all', 
    'exists': 'there exists at least one', 
    'true': 'is true', 
    'false': 'is false',
}

# Processing files
with open('./preTrainingDataCollectionLog/logFile', 'r+') as logFile:
    
    # Removing files based on log
    proofsDone = [proof[:-1] for proof in logFile.readlines()]
    lastProofDone = None
    for fileName in os.listdir(os.path.join('./preTrainingDataCollection')):
        if fileName not in proofsDone:
            os.remove(os.path.join('./preTrainingDataCollection', fileName))
        else:
            lastProofDone = fileName

    # If last proof exists, remove it from log and delete
    if lastProofDone and os.path.exists(os.path.join('./preTrainingDataCollection', lastProofDone)):
        proofsDone.remove(lastProofDone)
        os.remove(os.path.join('./preTrainingDataCollection', lastProofDone))

    # Iterating over files in the directory
    for fileName in tqdm(os.listdir('./extractedSymbols')):

        # if the proof was not already done
        if fileName[16:] not in proofsDone:
            with open(os.path.join('./extractedSymbols',fileName)) as f:
                
                # get the extracted symbols
                extractedSymbolsFromProof = json.load(f)

                # create da dictionary for all the scores 
                scores = {}
                
                # Calculating scores for positive symbols
                posSymbolScores = {}

                # get the extracted postive symbols
                posSymbols = extractedSymbolsFromProof['posSymbols']
                
                # calculate the tf-idf for every symbol 
                uniqueWordsInDocument = list(set(posSymbols))
                for word in uniqueWordsInDocument:
                    posSymbolScores[word] = tfIdf(word, posSymbols, documents)
                
                # if the at least one positive symbol exists get the minimum and the maximum score
                if posSymbolScores:
                    minMax = getMinMax(posSymbolScores)

                # for every normalize the score based on min-max normalization for every symbol and save it in scores and postive symbol scores
                for element in posSymbolScores:
                    scores[element] = {
                        'score': posSymbolScores[element],
                        'normalizedScore': normalizeData(posSymbolScores[element], minMax['min'], minMax['max'],0 ,1)
                    }
                    posSymbolScores[element] = {
                        'score': posSymbolScores[element],
                        'normalizedScore': normalizeData(posSymbolScores[element], minMax['min'], minMax['max'],0 ,1)
                    }

                # Calculating scores for negative symbols
                negSymbolScores = {}

                # get the extracted negative symbols
                negSymbols = extractedSymbolsFromProof['negSymbols']

                # count the occurence of each symbol
                occurences = countWordOccurencesInDocument(negSymbols)

                # if there is at least one negative occurence get the minimum and maximum occurence
                if occurences:
                    minMax = getMinMax(occurences)
            
                # for every symbol normalize the occurence based on min-max normalization and save it in scores and negative symbol scores
                for element in occurences:
                    scores[element] = {
                        'score': occurences[element],
                        'normalizedScore': normalizeData(occurences[element], minMax['min'], minMax['max'], 0, -1)
                    }
                    negSymbolScores[element] = {
                        'score': occurences[element],
                        'normalizedScore': normalizeData(occurences[element], minMax['min'], minMax['max'], 0, -1)
                    }

                # Calculating scores for neutral symbols
                neutralSymbolScores = {}

                neutralSymbols = extractedSymbolsFromProof['neutralSymbols']

                for element in neutralSymbols:
                    scores[element] = {
                        'score': 0,
                        'normalizedScore': 0
                    }
                    neutralSymbolScores[element] = {
                        'score': 0,
                        'normalizedScore': 0
                    }

                # verbalize the goal 
                parseTree = generateParseTree(extractedSymbolsFromProof['goal'])
                verbalizedGoal = generateSentence(parseTree, mapOperatorsToWords, wordMapping)
                
                # save the converted pre-training data
                preTainingData = {
                'proofName': extractedSymbolsFromProof['proofName'][19:],
                'proofCategory': extractedSymbolsFromProof['proofCategory'],
                'goal': extractedSymbolsFromProof['goal'],
                'verbalizedGoal': verbalizedGoal,
                'scores': scores,
                'posSymbolScores': posSymbolScores,
                'negSymbolScores': negSymbolScores,
                'neutralSymbolScores': neutralSymbolScores
                }

                # Writing pre-training data to file
                with open(os.path.join('./preTrainingDataCollection', fileName[16:]), 'w') as file:
                    json.dump(preTainingData, file, indent=4)
                
                # Writing  the proof name to the log file
                logFile.write(fileName[16:] + "\n")
                logFile.truncate()