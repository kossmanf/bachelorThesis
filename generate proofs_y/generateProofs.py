# Importing necessary modules
import os
import re
import math
import shutil
import subprocess
import json

# Program description
# This program creates a file structure for proofs and attempts to find proofs using E prover for all the axioms files, storing the output in the proofs file structure.

# Configuration Constants

# Important ! a folder named proofLog has to be created manually

# Path to the directory containing the axioms
_axiomsPath = './axioms'

# Path to the Eprover executable
_eproverPath = '/home/fabian/Schreibtisch/eprover_2.6/E/PROVER/eprover'

# Parameters for the E prover
# Use '--auto' to set heuristics and other settings automatically
# Use '--silent' to minimize terminal output
# Use '--training-examples' to mark positive and negative examples for training
# Use '--proof-object' to output the proof object if a proof is found
# Use '--cpu-limit' to limit the CPU calculation time per proof
# Use '-R' to print the resources used
_parameters = ['--auto', '--silent', '--training-examples=3', '--proof-object', '--cpu-limit=15', '-R']

# Path to the log file for storing proofs
_proofLogFilePath = './proofLog/proofLog.txt'

# Generate parameter string
parameters_string = ' '.join(_parameters)

# Check if the proof log file exists
if not os.path.exists(_proofLogFilePath):
    # If it doesn't exist, create the proofs folder
    if os.path.exists('./proofs'):
        # Delete existing proofs
        for category in os.listdir('./proofs'):
            category_path = os.path.join('./proofs/', category)
            for proof in os.listdir(category_path):
                os.remove(os.path.join(category_path, proof))
            os.rmdir(category_path)
    else:
        os.mkdir('./proofs')

    # Create the proof log file
    open(_proofLogFilePath, "w")

# Open the proof log file
with open(_proofLogFilePath, "r+") as proof_log:
    
    # Read the log file to get proofs done so far
    proofs_done = [proof.rstrip('\n') for proof in proof_log.readlines()]

    # If there are completed proofs, redo the last one
    if len(proofs_done) > 0:
        last_proof_done = proofs_done.pop()
        # Remove the last proof file if it exists
        if os.path.exists(last_proof_done):
            os.remove(last_proof_done)

    # Check if the directory containing axioms exists
    if os.path.exists(_axiomsPath):
        
        # Loop through categories in the axioms directory
        for category in os.listdir(_axiomsPath):

            # Create a folder for the category in the proofs folder if it doesn't exist
            category_proof_path = os.path.join('.', 'proofs', category)
            if not os.path.exists(category_proof_path):
                os.mkdir(category_proof_path)

            # Loop through axioms files in the category
            for axiom in os.listdir(os.path.join(_axiomsPath, category)):

                # Split the name of the axioms file
                split_axiom_name = axiom.replace('.', '_').split('_')

                # Generate the name for the proof file
                proof_name = 'proof_' + split_axiom_name[1] + '.' + split_axiom_name[2] + '.tstp'
                proof_file_path = os.path.join(category_proof_path, proof_name)

                # Check if the proof is not already done
                if proof_file_path not in proofs_done:
                    # Generate the path to the axioms file
                    _axiomsPath = os.path.join(_axiomsPath, category, axiom)

                    # Write the proof name to the log file
                    proof_log.write(proof_file_path + "\n")
                    proof_log.truncate()

                    print('Trying to prove ' + split_axiom_name[1])

                    # Start the E prover with the axioms file and output the result to a text file
                    os.system(f"{_eproverPath} {parameters_string} {_axiomsPath} --output-file={proof_file_path}")
