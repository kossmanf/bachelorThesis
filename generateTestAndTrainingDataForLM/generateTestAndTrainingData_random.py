from torch.utils.data import Dataset, DataLoader
import torch
import os
import json
import random
import math
from tqdm import tqdm

# Set the directory containing pre-training data
rootdir = './preTrainingDataCollection'

# Retrieve a list of file names from the specified directory
preTrainingData = os.listdir(rootdir)

def genTestAndTrainingData(percentage, preTrainingData, posSymbolAmount, negSymbolAmount, neutSymbolAmount):
    """
    This function generates training and test datasets from the provided list of pre-training data files.
    
    Args:
        percentage (float): Percentage of data to use for training.
        preTrainingData (list): List of filenames containing the data.
        posSymbolAmount (int): Number of positive symbol instances to select randomly.
        negSymbolAmount (int): Number of negative symbol instances to select randomly.
        neutSymbolAmount (int): Number of neutral symbol instances to select randomly.
    """

    # Initialize empty lists to store elements for the training and test datasets
    verbalizedGoals_training = []
    symbolNames_training = []
    normalizedScores_training = []

    verbalizedGoals_test = []
    symbolNames_test = []
    normalizedScores_test = []

    # Calculate the number of files to allocate to the training dataset
    training_amount = (percentage / 100) * len(preTrainingData)
    
    # Initialize a counter to track the number of files processed
    ctr = 0

    # Process each file in the list
    for fileName in tqdm(preTrainingData, desc="Processing data"):
        # Open and load JSON data from each file
        with open(f'{rootdir}/{fileName}') as json_data:
            data = json.load(json_data)
        
        # Extract relevant data from the loaded JSON object
        verbalizedGoal = data['verbalizedGoal']
        posScores = data['posSymbolScores']
        negScores = data['negSymbolScores']
        neutScores = data['neutralSymbolScores']

        # Temporary storage for training data from positive, negative, and neutral symbols
        posTd_tmp = []
        negTd_tmp = []
        neutTd_tmp = []

        # Append data to the temporary lists
        for symbolName, scores in posScores.items():
            posTd_tmp.append({
                'verbalizedGoal': verbalizedGoal,
                'symbolName': symbolName,
                'normalizedScore': scores['normalizedScore']
            })
        
        for symbolName, scores in negScores.items():
            negTd_tmp.append({
                'verbalizedGoal': verbalizedGoal,
                'symbolName': symbolName,
                'normalizedScore': scores['normalizedScore']
            })
        
        for symbolName, scores in neutScores.items():
            neutTd_tmp.append({
                'verbalizedGoal': verbalizedGoal,
                'symbolName': symbolName,
                'normalizedScore': scores['normalizedScore']
            })

        # Randomly select specified amount of positive, negative, and neutral symbols
        if posSymbolAmount <= len(posTd_tmp):
            posTd_tmp = random.sample(posTd_tmp, posSymbolAmount)
        if negSymbolAmount <= len(negTd_tmp):
            negTd_tmp = random.sample(negTd_tmp, negSymbolAmount)
        if neutSymbolAmount <= len(neutTd_tmp):
            neutTd_tmp = random.sample(neutTd_tmp, neutSymbolAmount)

        # Combine the samples to form the full set of training data for the current file
        trainingData = posTd_tmp + negTd_tmp + neutTd_tmp
        
        # Distribute the combined data into training or test datasets
        for td in trainingData:
            if ctr < training_amount:
                verbalizedGoals_training.append(td['verbalizedGoal'])
                symbolNames_training.append(td['symbolName'])
                normalizedScores_training.append(td['normalizedScore'])
            else:
                verbalizedGoals_test.append(td['verbalizedGoal'])
                symbolNames_test.append(td['symbolName'])
                normalizedScores_test.append(td['normalizedScore'])
                
        # Increment the counter after processing each file
        ctr += 1

    # Print summary statistics of the training and test data
    print('Amount of proofs used for training data:', math.floor(training_amount))
    print('Amount of proofs used for test data:', ctr - math.floor(training_amount))

    # Store training and test data as JSON and PyTorch tensor files
    training_data = {'verbalizedGoals': verbalizedGoals_training, 'symbolNames': symbolNames_training, 'normalizedScores': normalizedScores_training}
    test_data = {'verbalizedGoals': verbalizedGoals_test, 'symbolNames': symbolNames_test, 'normalizedScores': normalizedScores_test}

    with open("trainingData.json", "w") as json_file:
        json.dump(training_data, json_file)
    with open("testData.json", "w") as json_file:
        json.dump(test_data, json_file)

    torch.save(training_data, 'trainingData.pt')
    torch.save(test_data, 'testData.pt')

genTestAndTrainingData(80, preTrainingData, 10, 15, 15)  

