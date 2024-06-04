# Importing necessary modules
import json
import numpy as np
import matplotlib.pyplot as plt 

# Program description
# This Program calculates the following statistical measures based on the extracted information about the number of processed clauses and whether a proof was found 
# These statistics provide insights into the performance and efficiency of the eprover, comparing methods with and without the use of Language Models (LM).
# `totalProofTasks`: Indicates the total number of proof tasks processed.
# `solvedProofsWithoutLM` and `solvedProofsWithLM`: Show the count of tasks solved without and with the aid of language models, respectively.
# Clause-related statistics:
# `totalProcessedClausesWithoutLM` and `totalProcessedClausesWithLM`: Total clauses processed without and with language models.
# `meanProcessedClausesWithoutLM` and `meanProcessedClausesWithLM`: Average number of clauses processed per task, without and with language models.
# `stdDevProcessedClausesWithoutLM` and `stdDevProcessedClausesWithLM`: Standard deviation of the number of processed clauses, providing a measure of variability.
# `medianProcessedClausesWithoutLM` and `medianProcessedClausesWithLM`: Median number of clauses processed, indicating the central tendency.
# Reduction proportions:
# `percentageFewerClausesWithoutLM` and `percentageFewerClausesWithLM`: Percentages indicating the reduction in the number of clauses processed when comparing methods without and with language models.
# `percentageSimilarClauses`: Indicates the percentage of tasks where the number of clauses processed were similar between methods.
# Overall reduction statistics:
# `averagePercentageReduction`: The average percentage reduction in clause processing across tasks.
# `averagePercentageReductionStd`: Standard deviation of the percentage reductions, indicating variability in efficiency gains.
# `medianPercentageReduction`: Median of percentage reductions, providing another measure of central tendency for efficiency gains.
# The reduction percentage and the number of processed clauses are visualized in graphs
# The statistics are then saved into a file.

# Reading JSON data from a file
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

# Function to gather the number of processed clauses with and without Learning Modules (LM)
def getNumberOfProcessedClauses(data):
    clausesWithoutLm, clausesWithLm = [], []
    for normalProof in data['proofsNormal']:
        if normalProof['proofFound'] == 't' and normalProof['Processed clauses']:
            for lmProof in data['proofs']:
                if normalProof['proofName'] == lmProof['proofName'] and lmProof['Processed clauses']:
                    clausesWithoutLm.append(int(normalProof['Processed clauses']))
                    clausesWithLm.append(int(lmProof['Processed clauses']))
    return {
        'numProcessedClausesWithoutLm': clausesWithoutLm,
        'numProcessedClausesWithLm': clausesWithLm
    }

# Function to count the total number of proofs and how many were completed
def getNumberOfSolvedProofs(data):
    numProofsNormal = len([proof for proof in data['proofsNormal'] if proof['proofFound'] == 't'])
    numProofsWithLm = len([proof for proof in data['proofs'] if proof['proofFound'] == 't'])
    return {
        'totalProofTasks': len(data['proofsNormal']),
        'solvedProofsWithoutLm': numProofsNormal,
        'solvedProofsWithLm': numProofsWithLm
    }

# Function to calculate statistics about the number of processed clauses with and without LM
def calculateClauseStatistics(data):
    processedClauses = getNumberOfProcessedClauses(data)
    clausesWithoutLm = processedClauses['numProcessedClausesWithoutLm']
    clausesWithLm = processedClauses['numProcessedClausesWithLm']

    # Set up a figure with two subplots (1 row, 2 columns)
    plt.figure(figsize=(12, 6))  # Adjust the size as needed

    # Subplot 1: Clauses without language model
    plt.subplot(1, 2, 1)  # (rows, columns, subplot number)
    plt.bar(range(len(clausesWithoutLm)), clausesWithoutLm, color='gray')
    plt.title('Clauses Processed Without LM')
    plt.xlabel('Proof process')
    plt.ylabel('Number of Clauses')

    # Subplot 2: Clauses with language model
    plt.subplot(1, 2, 2)
    plt.bar(range(len(clausesWithLm)), clausesWithLm, color='gray')
    plt.title('Clauses Processed With LM')
    plt.xlabel('Proof process')
    plt.ylabel('Number of Clauses')

    # Show the figure with both subplots
    plt.tight_layout()  # Adjust subplots to fit into figure area.
    plt.show()

    return {
        'clauseStatisticsWithoutLm':{
            'totalProcessedClausesWithoutLm': sum(clausesWithoutLm),      
            'meanProcessedClausesWithoutLm': np.mean(clausesWithoutLm),
            'stdDevProcessedClausesWithoutLm': np.std(clausesWithoutLm),
            'medianProcessedClausesWithoutLm': np.median(clausesWithoutLm),
        },
        'clauseStatisticsWithLm':{
            'totalProcessedClausesWithLm': sum(clausesWithLm),
            'meanProcessedClausesWithLm': np.mean(clausesWithLm),
            'stdDevProcessedClausesWithLm': np.std(clausesWithLm),
            'medianProcessedClausesWithLm': np.median(clausesWithLm)
        }
    }

# Function to calculate percentage reductions between clauses processed with and without LM
def calculateClauseReductionProportions(data):
    fewerClausesWithoutLm, similarClauses, fewerClausesWithLm = 0, 0, 0
    for normalProof in data['proofsNormal']:
        if normalProof['proofFound'] == 't' and normalProof['Processed clauses']:
            for lmProof in data['proofs']:
                if normalProof['proofName'] == lmProof['proofName'] and lmProof['Processed clauses']:
                    normalCount = int(normalProof['Processed clauses'])
                    lmCount = int(lmProof['Processed clauses'])
                    if normalCount < lmCount:
                        fewerClausesWithoutLm += 1
                    elif normalCount == lmCount:
                        similarClauses += 1
                    else:
                        fewerClausesWithLm += 1

    totalComparisons = fewerClausesWithoutLm + similarClauses + fewerClausesWithLm
    return {
        'percentageFewerClausesWithoutLm': (fewerClausesWithoutLm / totalComparisons) * 100,
        'percentageSimilarClauses': (similarClauses / totalComparisons) * 100,
        'percentageFewerClausesWithLm': (fewerClausesWithLm / totalComparisons) * 100
    }

def calcAveragePercentageReduction(xData, yData):
    # Convert inputs to numpy arrays of type float to ensure numerical operations can be performed
    xData = np.array(xData, dtype=float)
    yData = np.array(yData, dtype=float)

    if not np.all(xData):
        raise ValueError("xData contains zero elements, which will lead to division by zero.")

    trimValue = 70

    # Calculate percentage reductions using numpy vectorization
    percentageReductions = ((xData - yData) / xData) * 100

    sortedPercentageReduction = np.sort(percentageReductions)
    trimmedPercentageReduction = [x for x in percentageReductions if x not in sortedPercentageReduction[:trimValue]]

    # Set up a figure with two subplots (1 row, 2 columns)
    plt.figure(figsize=(12, 6))  # Adjust the size as needed

    plt.subplot(1, 2, 1)  # (rows, columns, subplot number)
    plt.scatter(range(len(percentageReductions)), percentageReductions, color='gray', s=5)
    plt.title('Clause reduction percentages')
    plt.xlabel('Proof process')
    plt.ylabel('Clause reduction percentage ')

    plt.subplot(1, 2, 2)
    plt.scatter(range(len(trimmedPercentageReduction)), trimmedPercentageReduction, color='gray', s=5)
    plt.title('Clause reduction percentages trimmed')
    plt.xlabel('Proof process')
    plt.ylabel('Clause reduction percentage ')

    plt.show()

    # Compute the basic statistics
    return {
        'averagePercentageReduction': np.mean(percentageReductions),
        'averagePercentageReductionStd': np.std(percentageReductions),
        'medianPercentageReduction': np.median(percentageReductions)
    }

# Collecting data and calculating reductions
proofStatistics = getNumberOfSolvedProofs(data)
clauseStatistics = calculateClauseStatistics(data)
clauseReductionProportions = calculateClauseReductionProportions(data)
numberOfProcessedClauses = getNumberOfProcessedClauses(data)
averagePercentageReduction = calcAveragePercentageReduction(numberOfProcessedClauses['numProcessedClausesWithoutLm'], numberOfProcessedClauses['numProcessedClausesWithLm'])

# Output summary information
print(f"Total proof tasks: {proofStatistics['totalProofTasks']}")
print(f"Tasks solved w/o LM: {proofStatistics['solvedProofsWithoutLm']}")
print(f"Tasks solved w/ LM: {proofStatistics['solvedProofsWithLm']}")

print(f"Total clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLm']['totalProcessedClausesWithoutLm']}")
print(f"Total clauses w/ LM: {clauseStatistics['clauseStatisticsWithLm']['totalProcessedClausesWithLm']}")

print(f"Mean clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLm']['meanProcessedClausesWithoutLm']}")
print(f"Mean clauses w/ LM: {clauseStatistics['clauseStatisticsWithLm']['meanProcessedClausesWithLm']}")

print(f"Std deviation of clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLm']['stdDevProcessedClausesWithoutLm']}")
print(f"Std deviation of clauses w/ LM: {clauseStatistics['clauseStatisticsWithLm']['stdDevProcessedClausesWithLm']}")

print(f"Median clauses w/o LM: {clauseStatistics['clauseStatisticsWithoutLm']['medianProcessedClausesWithoutLm']}")
print(f"Median clauses w/ LM : {clauseStatistics['clauseStatisticsWithLm']['medianProcessedClausesWithLm']}")

print(f"% fewer clauses w/o LM: {clauseReductionProportions['percentageFewerClausesWithoutLm']}")
print(f"% fewer clauses w/ LM: {clauseReductionProportions['percentageFewerClausesWithLm']}")
print(f"% similar clauses: {clauseReductionProportions['percentageSimilarClauses']}")

print(f"Avg reduction of clauses: {averagePercentageReduction['averagePercentageReduction']}")
print(f"Std deviation of reduction: {averagePercentageReduction['averagePercentageReductionStd']}")
print(f"Median of reduction: {averagePercentageReduction['medianPercentageReduction']}")

# Save results to a JSON file
results = {
    "proofStatistics": proofStatistics,
    "clauseStatisticsWithoutLm": clauseStatistics['clauseStatisticsWithoutLm'],
    "clauseStatisticsWithLm": clauseStatistics['clauseStatisticsWithLm'],
    "clauseReductionProportions": clauseReductionProportions, 
    "averagePercentageReduction": averagePercentageReduction
}
with open('statistics.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
