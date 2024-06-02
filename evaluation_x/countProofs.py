import os
import re
import json

def countProofs(path):

    completedProofs = 0
    allProofs = 0

    for category in os.listdir(path):
        for proofFilePath in  os.listdir(os.path.join(path, category)):

            with open(os.path.join(path, category, proofFilePath), "r") as file:
                # read the lines from the file
                lines = file.read()

                # Replace '\t' and '\n' characters with an empty string
                lines = lines.replace('\t', '').replace('\n', '')
                lines = lines.replace(' ', '')

                # Find all matches with #Prooffound!
                if len(re.findall('#Prooffound!', lines)) == 1:
                    completedProofs = completedProofs + 1
                                    
                allProofs = allProofs + 1


    return {
        'allProofs': allProofs, 
        'completedProofs': completedProofs
    }


counts = countProofs('./proofs')
print(counts['allProofs'])
print(counts['completedProofs'])