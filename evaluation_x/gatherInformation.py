import os
import re
import json

def extractInformation(path, informationFilter):
    information = []

    for category in os.listdir(path):
        for proofFilePath in  os.listdir(os.path.join(path, category)):
            with open(os.path.join(path, category, proofFilePath), "r") as file:
                # read the lines from the file
                lines = file.read()

                # Replace '\t' and '\n' characters with an empty string
                lines = lines.replace('\t', '').replace('\n', '')
                lines = lines.replace(' ', '')

                informationDict = {}

                # extracting the proof name from the proof file path
                proofName = re.findall("(?<=proof_)(.*?)(?=.adimen)", proofFilePath)

                informationDict['proofName'] = proofName[0]
                informationDict['proofFound'] = 'f'

                # Find all matches with #Prooffound!
                if len(re.findall('#Prooffound!', lines)) == 1:
                    informationDict['proofFound'] = 't'
                
                for information_key in informationFilter:
                    information_key_tmp = information_key.replace(' ', '')
                    matcher = f"(?<=#{information_key_tmp}:)([^#]*)(?=#)"
                    info = re.findall(matcher, lines)

                    # if the information was found
                    if len(info) == 1:
                        informationDict[information_key] = info[0]
                    else:
                        informationDict[information_key] = ''
                
                information.append(informationDict)
    
    return information

informationFilter = ['Processed clauses']

# Writing JSON data
with open('extractedInformation.json', 'w') as file:
    json.dump({
        'proofsNormal':  extractInformation('proofsNormal', informationFilter),
        'proofs': extractInformation('proofs', informationFilter)
    }, file, indent=4) 


