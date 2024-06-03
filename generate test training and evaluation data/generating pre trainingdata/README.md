# Pre-Training Data Processing Scripts

This repository contains a set of Python scripts designed to process and prepare pre-training data for machine learning models. Below is an overview of each script and instructions on how to use them.

## generatePostiveAndNegativePreTrainingData.py

This program processes output files in the 'trainingProofs' folder, extracting conjectures and processed clauses. Clauses are sorted into two categories: those included in the proof, saved in 'posPreTrainingData', and those not included, saved in 'negPreTrainingData'. Each file's processed clauses are saved as separate JSON files in their respective folders.

### Required Directories
- `./trainingProofs`: Directory containing proofs from which the pre-training is generated.

### Output
- `./preTrainingData`: Directory containing the pre training data seperated into pos and neg pre training data.

### How to Use
1. Ensure that the training proofs where generated correctly from the completed proofs.
2. Run the script using the command:
    ```sh
    python generatePostiveAndNegativePreTrainingData.py
    ```

## extractSymbolsFromPreTrainingData.py

This program processes clauses that were previously separated into two groups: those that appear in the proof and those that do not. It extracts symbols from these clauses for further analysis.

### Required Directories
- `./preTrainingData`: Directory containing the pre training data seperated into pos and neg pre training data.

### Output
- `./preTrainingData`: Directory containing the pre training data in form documents containing the positive symbols, the negative symbols and the conjecture. 

### How to Use
1. Ensure the positive and negative pre-training data are seperated.
2. Run the script using the command:
    ```sh
    python extractSymbolsFromPreTrainingData.py
    ```

## collectDocuments.py

This program iterates over the positive symbols in generated documents, extracting them into lists. These lists, representing documents of positive symbols, are used to calculate TF-IDF scores, excluding negative and neutral symbols. The resulting documents are saved in a JSON file named "documents".

### Required Files and Directories
- Ensure directories are correctly set as per the script configuration.

### How to Use
1. Ensure the positive and negative pre-training data are seperated and the symbols are extracted.
2. Run the script using the command:
    ```sh
    python collectDocuments.py
    ```
    
### Output
- `./documents.json`: File containing the postive symbols of each document as a list in a list. 

## processPreTrainingData.py
This script generates pre-training data for each proof task by computing similarity scores for associated symbols.
Similarity scores are calculated as follows:
- For each positive symbol, compute the TF-IDF score. All the positive symbols from a proof process are treated as a document.
- For each negative symbol, count its occurrences within the proof process.
- For each neutral symbol, assign a score of zero.

### Required Files and Directories
-  `./preTrainingData`: Directory containing the pre training data in form documents containing the positive symbols, the negative symbols and the conjecture. 
-  `./documents.json`: File containing the postive symbols of each document as a list in a list. 

### Output
- `./preTrainingDataCollection`: Directory containing a file for each conjecture which contains the conjecture the postive symbols with scores, the negative symbols with scores and the neutral sybols with scores. 

### How to Use
1. Ensure the positive and negative pre-training data are seperated, the symbols are extracted and the `documents.json` file for calculating the tfidf scores was created.
2. Run the script using the command:
    ```sh
    python processPreTrainingData.py
    ```
