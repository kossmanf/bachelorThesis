# Importing necessary modules
import os
import re
import json

# Program description
# This program counts the conjectures attempted to be proven and the completed proofs

# This function counts the conjecutres and the completed proofs from the specified path
def countConjecturesAndCompletedProofs(path):
    # initialize the counters
    completedProofs = 0
    conjectures = 0

    # iteate over the categories and proof files
    for category in os.listdir(path):
        for proofFilePath in  os.listdir(os.path.join(path, category)):
            # open the file path
            with open(os.path.join(path, category, proofFilePath), "r") as file:
                # read the lines from the file
                lines = file.read()

                # Replace '\t' and '\n' characters with an empty string
                lines = lines.replace('\t', '').replace('\n', '')
                lines = lines.replace(' ', '')

                # Find all matches with #Prooffound!
                if len(re.findall('#Prooffound!', lines)) == 1:
                    # increase the proof found counter
                    completedProofs = completedProofs + 1

                # increase the conjectures counter
                conjectures = conjectures + 1

    # return the counter
    return {
        'conjectures': conjectures, 
        'completedProofs': completedProofs
    }

# count the conjectures and the completed proof
counts = countConjecturesAndCompletedProofs('./proofs')

# print the numbers
print(counts['conjectures'])
print(counts['completedProofs'])