# Importing necessary modules
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# Program description
# This Program calculates the following statistical measures based on the extracted information about the number of processed clauses and whether a proof was found 
# These statistics provide insights into the performance and efficiency of the eprover, without the use of Language Models (LM).
# `totalProofTasks`: Indicates the total number of proof tasks processed.
# `solvedProofsWithoutLM` : Show the count of tasks solved without the aid of language model, respectively.
# Clause-related statistics:
# `totalProcessedClausesWithoutLM` : Total clauses processed without the language model.
# `meanProcessedClausesWithoutLM` : Average number of clauses processed per task, without the language model.
# `stdDevProcessedClausesWithoutLM` : Standard deviation of the number of processed clauses, providing a measure of variability.
# `medianProcessedClausesWithoutLM` : Median number of clauses processed, indicating the central tendency.
# The the number of processed clauses is visualized in a graph
# The statistics are then saved into a file.

# Reading JSON data from a file
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

# Function to gather the number of processed clauses without language Modules (LM)
def getNumberOfProcessedClauses(data):
    clausesWithoutLM = []
    for normalProof in data['proofsNormal']:
        if normalProof['proofFound'] == 't' and normalProof['Processed clauses']:
                clausesWithoutLM.append(int(normalProof['Processed clauses']))
    return {
        'numProcessedClausesWithoutLM': clausesWithoutLM,
    }

# Function to count the total number of proofs and how many were completed
def getNumberOfSolvedProofs(data):
    numProofsNormal = len([proof for proof in data['proofsNormal'] if proof['proofFound'] == 't'])

    return {
        'totalProofTasks': len(data['proofsNormal']),
        'solvedProofsWithoutLM': numProofsNormal,
    }

# Function to calculate statistics about the number of processed clauses without LM
def calculateClauseStatistics(data):
    processedClauses = getNumberOfProcessedClauses(data)
    clausesWithoutLM = processedClauses['numProcessedClausesWithoutLM']

    return {
        'clauseStatisticsWithoutLM':{
            'totalProcessedClausesWithoutLM': sum(clausesWithoutLM),      
            'meanProcessedClausesWithoutLM': np.mean(clausesWithoutLM),
            'stdDevProcessedClausesWithoutLM': np.std(clausesWithoutLM),
            'medianProcessedClausesWithoutLM': np.median(clausesWithoutLM),
        }
    }

# Collecting data and calculating reductions
proofStatistics = getNumberOfSolvedProofs(data)
clauseStatistics = calculateClauseStatistics(data)
numberOfProcessedClauses = getNumberOfProcessedClauses(data)

# Output summary information
print(f"Total proof tasks: {proofStatistics['totalProofTasks']}")
print(f"Tasks solved w/o LM: {proofStatistics['solvedProofsWithoutLM']}")

print(f"Total clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLM']['totalProcessedClausesWithoutLM']}")

print(f"Mean clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLM']['meanProcessedClausesWithoutLM']}")

print(f"Std deviation of clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLM']['stdDevProcessedClausesWithoutLM']}")

print(f"Median clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLM']['medianProcessedClausesWithoutLM']}")

# Save results to a JSON file
results = {
    "proofStatistics": proofStatistics,
    "clauseStatisticsWithoutLM": clauseStatistics['clauseStatisticsWithoutLM'],
}
with open('statistics.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
