# Importing necessary modules
import os  
import json  
from tqdm import tqdm 

# Program description
# This program iterates over the positive symbols of every generated 'document'.
# From each document the positive symbols are extracted in a list 
# A new list is generated which contains the lists with the positive symbols.
# This is done for the following reason: for the positive symbols the tfidf score is calculated later on.
# Every list of positive symbols can be seen as a document; therefore, the negative and neutral symbols are not necessary anymore for calculating the tfidf.
# These 'documents' used for calculating the tfidf scores are then saved in a JSON file named documents.

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