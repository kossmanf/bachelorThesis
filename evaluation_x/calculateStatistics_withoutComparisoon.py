import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# Reading JSON data from a file
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

# Function to gather the number of processed clauses with and without Learning Modules (LM)
def get_number_of_processed_clauses(data):
    clauses_without_lm, clauses_with_lm = [], []
    for normal_proof in data['proofsNormal']:
        if normal_proof['proofFound'] == 't' and normal_proof['Processed clauses']:
                clauses_without_lm.append(int(normal_proof['Processed clauses']))
                clauses_with_lm.append(int(0))

    return {
        'numProcessedClausesWithoutLM': clauses_without_lm,
    }

# Function to count the total number of proofs and how many were completed
def get_number_of_solved_proofs(data):
    num_proofs_normal = len([proof for proof in data['proofsNormal'] if proof['proofFound'] == 't'])

    return {
        'totalProofTasks': len(data['proofsNormal']),
        'solvedProofsWithoutLM': num_proofs_normal,
    }

# Function to calculate statistics about the number of processed clauses with and without LM
def calculate_clause_statistics(data):
    processed_clauses = get_number_of_processed_clauses(data)
    clauses_without_lm = processed_clauses['numProcessedClausesWithoutLM']

    return {
        'clauseStatisticsWithoutLM':{
            'totalProcessedClausesWithoutLM': sum(clauses_without_lm),      
            'meanProcessedClausesWithoutLM': np.mean(clauses_without_lm),
            'stdDevProcessedClausesWithoutLM': np.std(clauses_without_lm),
            'medianProcessedClausesWithoutLM': np.median(clauses_without_lm),
        }
    }

# Collecting data and calculating reductions
proof_statistics = get_number_of_solved_proofs(data)
clause_statistics = calculate_clause_statistics(data)
numberOfProcessedClauses = get_number_of_processed_clauses(data)

# Output summary information
print(f"Total proof tasks: {proof_statistics['totalProofTasks']}")
print(f"Tasks solved w/o LM: {proof_statistics['solvedProofsWithoutLM']}")

print(f"Total clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['totalProcessedClausesWithoutLM']}")

print(f"Mean clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['meanProcessedClausesWithoutLM']}")

print(f"Std deviation of clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['stdDevProcessedClausesWithoutLM']}")

print(f"Median clauses w/o LM: {clause_statistics['clauseStatisticsWithoutLM']['medianProcessedClausesWithoutLM']}")

# Save results to a JSON file
results = {
    "proofStatistics": proof_statistics,
    "clauseStatisticsWithoutLM": clause_statistics['clauseStatisticsWithoutLM'],
}
with open('statistics.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

