# Importing necessary modules
import os
import re
from tqdm import tqdm
import json

# Program description
# This program checks for duplicate proof tasks in the test data.
# It also identifies proof tasks used in the test data and training data
# It saves the filenames to JSON file.

# Axiom files used for training and testing
filePath1 = './testAxioms'
filePath2 = './trainingAxioms'

# dictionary for storing the conjectures
conjecturesDict = {}

# This function retrieves conjectures from axiom files, labeling each with 'A' for testing and 'B' for training purposes. 
# It stores the conjectures in a dictionary, using the conjecture itself as the key and the filename of the containing file as the value.
def extractConjectures(filePath):
    # Determine the tag for files based on their path: 'A' if part of 'testAxioms', otherwise 'B'.
    fileTag = "A" if "testAxioms" in filePath else "B"

    # Iterate over each category of proof conjectures in the given directory
    for proofCategory in tqdm(os.listdir(filePath), desc=f'Processing {filePath}'):
        # Iterate over each file in the conjecture category
        for fileName in tqdm(os.listdir(os.path.join(filePath, proofCategory)), desc=f'Files in {proofCategory}'):
            # Open and read the file
            with open(os.path.join(filePath, proofCategory, fileName), 'r') as file:
                # removing tabs and newlines for clean processing.
                lines = file.read()
                lines = lines.replace('\t', '').replace('\n', '')

                # Extract conjecture using regex 
                match = re.findall('(?<=conjecture,)(.*)(?=\)\.)', lines)

                # If a conjecture is found, process it.
                if match:
                    # Remove spaces from the conjecture for consistency.
                    conjecture = match[0].replace(' ','')
                    # If this conjecture hasn't been recorded, initialize its list in the dictionary.
                    if conjecture not in conjecturesDict:
                        conjecturesDict[conjecture] = []
                    # Append the file tag and path to the list of files containing this conjecture.
                    conjecturesDict[conjecture].append(f"{fileTag}:{os.path.join(proofCategory, fileName)}")


# extracting the conjectures
extractConjectures(filePath1)
extractConjectures(filePath2)


# Finding duplicates within the same file path 
# Iterate over conjectures in the dictionary to find multiple file paths starting with 'A' (test data) that include the conjecture.
duplicates = {conj: files for conj, files in conjecturesDict.items() if sum(1 for f in files if f.startswith("A:")) > 1}

# Finding common conjectures across both file paths
# Iterate over the dictionary's conjectures to check if their file paths start with 'A' (test data) and 'B' (training data) which contain the conjecture.
commonConjectures = {conj: files for conj, files in conjecturesDict.items() if any("A:" in f for f in files) and any("B:" in f for f in files)}

# Save the duplicates to a JSON file
with open('duplicates.json', 'w') as jsonFile:
    json.dump(duplicates, jsonFile, indent=4)

# Optionally, save the common conjectures to a separate JSON file
with open('commonConjectures.json', 'w') as jsonFile:
    json.dump(commonConjectures, jsonFile, indent=4)

# Print the common conjectures and their files
for conjecture, files in commonConjectures.items():
    filesFromA = [f for f in files if f.startswith("A:")]
    filesFromB = [f for f in files if f.startswith("B:")]
    print(f"Conjecture: '{conjecture}'")
    print(f"  Appears in filePath1 in: {filesFromA}")
    print(f"  Appears in filePath2 in: {filesFromB}")
