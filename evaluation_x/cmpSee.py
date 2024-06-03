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

conjecturesDict = {}

def processFiles(filePath):
    fileTag = "A" if "testAxioms" in filePath else "B"
    for proofCategory in tqdm(os.listdir(filePath), desc=f'Processing {filePath}'):
        for fileName in tqdm(os.listdir(os.path.join(filePath, proofCategory)), desc=f'Files in {proofCategory}'):
            with open(os.path.join(filePath, proofCategory, fileName), 'r') as file:
                lines = file.read()
                lines = lines.replace('\t', '').replace('\n', '')
                match = re.findall('(?<=conjecture,)(.*)(?=\)\.)', lines)
                if match:
                    conjecture = match[0].replace(' ','')
                    if conjecture not in conjecturesDict:
                        conjecturesDict[conjecture] = []
                    conjecturesDict[conjecture].append(f"{fileTag}:{os.path.join(proofCategory, fileName)}")

processFiles(filePath1)
processFiles(filePath2)


# Finding duplicates within the same file path
#duplicates = {conj: files for conj, files in conjecturesDict.items() if len(files) > 1}
duplicates = {conj: files for conj, files in conjecturesDict.items() if sum(1 for f in files if f.startswith("A:")) > 1}

# Finding common conjectures across both file paths
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
