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
      
        # Remove only the file paths tagged with 'A'.
        # It's important to differentiate because the list 'common_conjecture_file_paths' also includes paths tagged with 'B.
        # Paths tagged with 'B' were oly used for training purposes and should not be removed.
        if tag == 'A':
            # generate the file name of the output file from the eprover
            category, fileName = filePath.split('/')
            fileName = 'proof_' + fileName.split('_')[1]
            full_path = os.path.join(folderPath, category, fileName)

            # delete the output file beloning to the conjecture
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Deleted file: {full_path}")
            else:
                print(f"Not deleted file: {full_path}")

# Load duplicate and common conjectures data
duplicates = readJson('duplicates.json')
common_conjectures = readJson('commonConjectures.json')

# Prepare list of file paths from duplicates
# This is accomplished by keeping the first file path from the list of duplicates and adding all subsequent ones for removal.
duplicate_file_paths = [file for files in duplicates.values() for file in files[1:]]

# Prepare list of file paths from common conjectures
# This is done by adding all the file paths in the list for removal
common_conjecture_file_paths = [file for files in common_conjectures.values() for file in files]

# deleting the files 
deleteFiles(duplicate_file_paths, folderPath1)
deleteFiles(common_conjecture_file_paths, folderPath1)
deleteFiles(duplicate_file_paths, folderPath2)
deleteFiles(common_conjecture_file_paths, folderPath2)