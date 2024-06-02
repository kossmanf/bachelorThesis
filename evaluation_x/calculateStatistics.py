import json
import numpy as np
import matplotlib.pyplot as plt 

# Reading JSON data from a file
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

# Function to gather the number of processed clauses with and without Learning Modules (LM)
def get_number_of_processed_clauses(data):
    clauses_without_lm, clauses_with_lm = [], []
    for normal_proof in data['proofsNormal']:
        if normal_proof['proofFound'] == 't' and normal_proof['Processed clauses']:
            for lm_proof in data['proofs']:
                if normal_proof['proofName'] == lm_proof['proofName'] and lm_proof['Processed clauses']:
                    clauses_without_lm.append(int(normal_proof['Processed clauses']))
                    clauses_with_lm.append(int(lm_proof['Processed clauses']))
    return {
        'numProcessedClausesWithoutLM': clauses_without_lm,
        'numProcessedClausesWithLM': clauses_with_lm
    }

# Function to count the total number of proofs and how many were completed
def get_number_of_solved_proofs(data):
    num_proofs_normal = len([proof for proof in data['proofsNormal'] if proof['proofFound'] == 't'])
    num_proofs_with_lm = len([proof for proof in data['proofs'] if proof['proofFound'] == 't'])
    return {
        'totalProofTasks': len(data['proofsNormal']),
        'solvedProofsWithoutLM': num_proofs_normal,
        'solvedProofsWithLM': num_proofs_with_lm
    }

# Function to calculate statistics about the number of processed clauses with and without LM
def calculate_clause_statistics(data):
    processed_clauses = get_number_of_processed_clauses(data)
    clauses_without_lm = processed_clauses['numProcessedClausesWithoutLM']
    clauses_with_lm = processed_clauses['numProcessedClausesWithLM']

    # Set up a figure with two subplots (1 row, 2 columns)
    plt.figure(figsize=(12, 6))  # Adjust the size as needed

    # Subplot 1: Clauses without language model
    plt.subplot(1, 2, 1)  # (rows, columns, subplot number)
    plt.bar(range(len(clauses_without_lm)), clauses_without_lm, color='gray')
    plt.title('Clauses Processed Without LM')
    plt.xlabel('Proof process')
    plt.ylabel('Number of Clauses')

    # Subplot 2: Clauses with language model
    plt.subplot(1, 2, 2)
    plt.bar(range(len(clauses_with_lm)), clauses_with_lm, color='gray')
    plt.title('Clauses Processed With LM')
    plt.xlabel('Proof process')
    plt.ylabel('Number of Clauses')

    # Show the figure with both subplots
    plt.tight_layout()  # Adjust subplots to fit into figure area.
    plt.show()

    return {
        'clauseStatisticsWithoutLM':{
            'totalProcessedClausesWithoutLM': sum(clauses_without_lm),      
            'meanProcessedClausesWithoutLM': np.mean(clauses_without_lm),
            'stdDevProcessedClausesWithoutLM': np.std(clauses_without_lm),
            'medianProcessedClausesWithoutLM': np.median(clauses_without_lm),
        },
        'clauseStatisticsWithLM':{
            'totalProcessedClausesWithLM': sum(clauses_with_lm),
            'meanProcessedClausesWithLM': np.mean(clauses_with_lm),
            'stdDevProcessedClausesWithLM': np.std(clauses_with_lm),
            'medianProcessedClausesWithLM': np.median(clauses_with_lm)
        }
    }

# Function to calculate percentage reductions between clauses processed with and without LM
def calculate_clause_reduction_proportions(data):
    fewer_clauses_without_lm, similar_clauses, fewer_clauses_with_lm = 0, 0, 0
    for normal_proof in data['proofsNormal']:
        if normal_proof['proofFound'] == 't' and normal_proof['Processed clauses']:
            for lm_proof in data['proofs']:
                if normal_proof['proofName'] == lm_proof['proofName'] and lm_proof['Processed clauses']:
                    normal_count = int(normal_proof['Processed clauses'])
                    lm_count = int(lm_proof['Processed clauses'])
                    if normal_count < lm_count:
                        fewer_clauses_without_lm += 1
                    elif normal_count == lm_count:
                        similar_clauses += 1
                    else:
                        fewer_clauses_with_lm += 1

    total_comparisons = fewer_clauses_without_lm + similar_clauses + fewer_clauses_with_lm
    return {
        'percentageFewerClausesWithoutLM': (fewer_clauses_without_lm / total_comparisons) * 100,
        'percentageSimilarClauses': (similar_clauses / total_comparisons) * 100,
        'percentageFewerClausesWithLM': (fewer_clauses_with_lm / total_comparisons) * 100
    }

def calc_average_percentage_reduction(xData, yData):
    # Convert inputs to numpy arrays of type float to ensure numerical operations can be performed
    xData = np.array(xData, dtype=float)
    yData = np.array(yData, dtype=float)

    if not np.all(xData):
        raise ValueError("xData contains zero elements, which will lead to division by zero.")

    trimValue =70

    # Calculate percentage reductions using numpy vectorization
    percentage_reductions = ((xData - yData) / xData) * 100

    sortedPercentageReduciton = np.sort(percentage_reductions)
    trimedPercentageReduciton = [x for x in percentage_reductions if x not in sortedPercentageReduciton[:trimValue]]

    # Set up a figure with two subplots (1 row, 2 columns)
    plt.figure(figsize=(12, 6))  # Adjust the size as needed

    plt.subplot(1, 2, 1)  # (rows, columns, subplot number)
    plt.scatter(range(len(percentage_reductions)), percentage_reductions, color='gray', s=5)
    plt.title('Clause reduction percentages')
    plt.xlabel('Proof process')
    plt.ylabel('Clause reduction percentage ')

    plt.subplot(1, 2, 2)
    plt.scatter(range(len(trimedPercentageReduciton)), trimedPercentageReduciton, color='gray', s=5)
    plt.title('Clause reduction percentages trimed')
    plt.xlabel('Proof process')
    plt.ylabel('Clause reduction percentage ')

    plt.show()

    # Compute the basic statistics
    return {
        'averagePercentageReduction': np.mean(percentage_reductions),
        'averagePercentageReductionStd': np.std(percentage_reductions),
        'medianPercentageReduction': np.median(percentage_reductions)
    }


# Collecting data and calculating reductions
proof_statistics = get_number_of_solved_proofs(data)
clause_statistics = calculate_clause_statistics(data)
clause_reduction_proportions = calculate_clause_reduction_proportions(data)
numberOfProcessedClauses = get_number_of_processed_clauses(data)
average_percentage_reduction = calc_average_percentage_reduction(numberOfProcessedClauses['numProcessedClausesWithoutLM'], numberOfProcessedClauses['numProcessedClausesWithLM'])


# Output summary information
print(f"Total proof tasks: {proof_statistics['totalProofTasks']}")
print(f"Tasks solved w/o LM: {proof_statistics['solvedProofsWithoutLM']}")
print(f"Tasks solved w/ LM: {proof_statistics['solvedProofsWithLM']}")

print(f"Total clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['totalProcessedClausesWithoutLM']}")
print(f"Total clauses w/ LM: {clause_statistics['clauseStatisticsWithLM']['totalProcessedClausesWithLM']}")

print(f"Mean clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['meanProcessedClausesWithoutLM']}")
print(f"Mean clauses w/ LM: {clause_statistics['clauseStatisticsWithLM']['meanProcessedClausesWithLM']}")

print(f"Std deviation of clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['stdDevProcessedClausesWithoutLM']}")
print(f"Std deviation of clauses w/ LM: {clause_statistics['clauseStatisticsWithLM']['stdDevProcessedClausesWithLM']}")

print(f"Median clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['medianProcessedClausesWithoutLM']}")
print(f"Median clauses w/ LM : {clause_statistics['clauseStatisticsWithLM']['medianProcessedClausesWithLM']}")

print(f"% fewer clauses w/o LM: {clause_reduction_proportions['percentageFewerClausesWithoutLM']}")
print(f"% fewer clauses w/ LM: {clause_reduction_proportions['percentageFewerClausesWithLM']}")
print(f"% similar clauses: {clause_reduction_proportions['percentageSimilarClauses']}")

print(f"Avg reduction of clauses: {average_percentage_reduction['averagePercentageReduction']}")
print(f"Std deviation of reduction: {average_percentage_reduction['averagePercentageReductionStd']}")
print(f"Median of reduction: {average_percentage_reduction['medianPercentageReduction']}")

# Save results to a JSON file
results = {
    "proofStatistics": proof_statistics,
    "clauseStatisticsWithoutLM": clause_statistics['clauseStatisticsWithoutLM'],
    "clauseStatisticsWithLM": clause_statistics['clauseStatisticsWithLM'],
    "clauseReductionProportions": clause_reduction_proportions, 
    "averagePercentageReduction": average_percentage_reduction
}
with open('statistics.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

