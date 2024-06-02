import os  
import json  
from tqdm import tqdm 

# Setting the directory where the JSON files are located
rootdir = './extractedSymbols'

# Creating a dictionary to store the extracted symbols
documents = {}
documents['documents'] = []

# Iterating over each file in the directory and displaying a progress bar
for fileName in tqdm(os.listdir(rootdir)):
    # Opening each JSON file in read mode
    with open(rootdir + '/' + fileName) as json_data:
        # Loading JSON data from the file
        data = json.load(json_data)
    # Appending the 'posSymbols' data from each file to the 'documents' dictionary
    documents['documents'].append(data['posSymbols'])

# Writing the aggregated data to a new JSON file
with open('./documents.json', "w") as json_file:
    json.dump(documents, json_file)