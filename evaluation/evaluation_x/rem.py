# Importing necessary modules
import json
import os

# Program description
# This program deletes output files generated from similar proof tasks to remove duplicates.
# It also removes output files from proof tasks that were used in the training of the language model.

# file path from where the ouput files should should be deleted
folderPath1 = 'proofs'
folderPath2 = 'proofsNormal'

# funtion to read the 
def readJson(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# this function deletes the specifies files from the path
def deleteFiles(filesToRemove, folderPath):
    for file in filesToRemove:
        # getting the tag from the path
        tag, filePath = file.split(':')
      
        # checking if the tag co
        if tag == 'A':
            category, fileName = filePath.split('/')
            fileName = 'proof_' + fileName.split('_')[1]
            full_path = os.path.join(folderPath, category, fileName)

            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Deleted file: {full_path}")
            else:
                print(f"Not deleted file: {full_path}")

# Load duplicate and common conjectures data
duplicates = readJson('duplicates.json')
common_conjectures = readJson('commonConjectures.json')

# Prepare list of files from duplicates
duplicate_file_paths = [file for files in duplicates.values() for file in files[1:]]

# Prepare list of files from common conjectures
common_conjecture_file_paths = [file for files in common_conjectures.values() for file in files]

# deleting the files 
deleteFiles(duplicate_file_paths, folderPath1)
deleteFiles(common_conjecture_file_paths, folderPath1)
deleteFiles(duplicate_file_paths, folderPath2)
deleteFiles(common_conjecture_file_paths, folderPath2)