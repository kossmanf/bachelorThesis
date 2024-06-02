import json
import os

folderPath1 = 'proofs'
folderPath2 = 'proofsNormal'

def readJson(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def delete_files_with_conjectures(filesToRemove, folderPath):
    for file in filesToRemove:
        tag, filePath = file.split(':')
      
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


delete_files_with_conjectures(duplicate_file_paths, folderPath1)
delete_files_with_conjectures(common_conjecture_file_paths, folderPath1)
delete_files_with_conjectures(duplicate_file_paths, folderPath2)
delete_files_with_conjectures(common_conjecture_file_paths, folderPath2)