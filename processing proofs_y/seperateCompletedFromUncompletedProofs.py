# Importing necessary modules
import os
import shutil

# Program description
# This program  processes eprover output files in the 'proofs' folder, sorting them into two distinct folders: 
# 'completed_proofs' for files where proofs were found, and 'uncompleted proofs' for those where proofs were not found.
# The 'completed_proofs' folder contains training data for the language model, testing data for model validation, and evaluation data for the research project.
# The 'uncompleted_proofs' folder holds files reserved for future evaluations, where the trained language model will be used as a heuristic to attempt solving the goals of the output files again.
# The original categorical folder structure will be maintained.

# Clean up existing folder structures for completed and uncompleted proofs, if they exist

# Delete the folder structure for completed proofs if it exists
if os.path.exists('./completedProofs'):
    # Iterate over categories in completed proofs
    for category in os.listdir('./completedProofs'):
        # Remove all files within each category folder
        for file_name in os.listdir(os.path.join('.', 'completedProofs', category)):
            os.remove(os.path.join('.', 'completedProofs', category, file_name))
        # Remove the category folder itself
        os.rmdir(os.path.join('.', 'completedProofs', category)) 
    # Remove the main completed proofs folder
    os.rmdir('./completedProofs') 

# Delete the folder structure for uncompleted proofs if it exists
if os.path.exists('./uncompletedProofs'):
    # Iterate over categories in uncompleted proofs
    for category in os.listdir('./uncompletedProofs'):
        # Remove all files within each category folder
        for file_name in os.listdir(os.path.join('.', 'uncompletedProofs', category)):
            os.remove(os.path.join('.', 'uncompletedProofs', category, file_name))
        # Remove the category folder itself
        os.rmdir(os.path.join('.', 'uncompletedProofs', category))
    # Remove the main uncompleted proofs folder
    os.rmdir('./uncompletedProofs')

# Create folders for completed and uncompleted proofs
os.mkdir('./completedProofs')
os.mkdir('./uncompletedProofs') 

# Check if proofs folder exists
if os.path.exists('./proofs'):
    # Iterate over categories in proofs
    for category in os.listdir('./proofs'):
        # Create corresponding category folders in completed and uncompleted proofs
        os.mkdir(os.path.join('.', 'completedProofs', category))
        os.mkdir(os.path.join('.', 'uncompletedProofs', category))
        
        # Iterate over proofs in each category
        for proof in os.listdir(os.path.join('./proofs', category)):
            with open(os.path.join('./proofs', category, proof), "r") as proofFile:
                lines = proofFile.readlines()
                noProofFound = True
                
                # Check if proof is completed by searching for '# Proof found!' string
                for line in lines:
                    if(line.strip() == '# Proof found!'):
                        noProofFound = False
                        break
                
                # Copy proofs to appropriate folders based on completion status
                if noProofFound:
                    print(f"Uncompleted proof: {proof.strip()}")
                    shutil.copy(os.path.join('./proofs', category, proof), os.path.join('./uncompletedProofs', category))
                else:
                    print(f"Completed proof: {proof.strip()}")
                    shutil.copy(os.path.join('./proofs', category, proof), os.path.join('./completedProofs', category))