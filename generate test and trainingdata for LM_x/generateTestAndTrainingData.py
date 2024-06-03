# Importing necessary modules
from torch.utils.data import Dataset, DataLoader
import torch
import os
import json
import random
import math
from tqdm import tqdm

# program description
# This program splits the pre training data into test and training sets, each data point is a triplet of goal, score, and symbol.
# The data points are selected randomly, based on the specified ratio of neutral and negative symbols to positive symbols.
# The triplet data is organized into three lists: goals, scores, and symbols. Each element at a given index across these lists forms one complete data point.

# path for the pre training data
rootdir = './preTrainingDataCollection'

# Initialize lists to store training and test data
verbalizedGoals_training = []
symbolNames_training = []
normalizedScores_training = []

verbalizedGoals_test = []
symbolNames_test = []
normalizedScores_test = []

# load the pre training data
preTrainingData = os.listdir(rootdir)

# Generates training and test datasets from pre-training data.
# percentage : The percentage of data to use for training.
# preTrainingData : List of data filenames to be processed.
# k : Ratio of negative and neutral to positive samples.
def genTestAndTrainingData(percentage, preTrainingData, k):

    # Calculate the number of files to be used for training
    training_amount = (percentage / 100) * len(preTrainingData)
    
    # Counter to track the number of processed files for splitting into training/test
    ctr = 0

    # Process each file
    for fileName in tqdm(preTrainingData, desc="Processing data"):
        # Load JSON data from the file
        with open(f'{rootdir}/{fileName}') as json_data:
            data = json.load(json_data)
        
        # Extract the verbalized goal and positive/negative scores
        verbalizedGoal = data['verbalizedGoal']
        posScores = data['posSymbolScores']
        negScores = data['negSymbolScores']
        neutScores = data['neutralSymbolScores']


        # Create temporary lists for positive and negative training data
        posTd_tmp = []
        negTd_tmp = []
        neutTd_tmp = []

        # Collect training data for each symbol with scores
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
   
        
        # appending the neutral symbols to the negative symbols to select n * k symbols from the negative and neutral symbols 
        for symbolName, scores in neutScores.items():
            negTd_tmp.append({
                'verbalizedGoal': verbalizedGoal,
                'symbolName': symbolName,
                'normalizedScore': scores['normalizedScore']
            })

        # Adjust the amount of negative and neutral samples based on the ratio k
        n = len(posTd_tmp)

        # calculate the amount of negative and neutral symbols based on the ratio
        negNeutSymbAmount = int(n * k)
        
        # select randomly the number of symbols based on the ratio
        negTd_tmp = random.sample(negTd_tmp, negNeutSymbAmount) if negNeutSymbAmount < len(negTd_tmp) else negTd_tmp


        # Combine positive and negative data
        trainingData = posTd_tmp + neutTd_tmp + negTd_tmp
        
        # Assign data to training or test sets based on the training percentage
        for td in trainingData:
            if ctr < training_amount:
                verbalizedGoals_training.append(td['verbalizedGoal'])
                symbolNames_training.append(td['symbolName'])
                normalizedScores_training.append(td["normalizedScore"])
            else:
                verbalizedGoals_test.append(td['verbalizedGoal'])
                symbolNames_test.append(td['symbolName'])
                normalizedScores_test.append(td["normalizedScore"])
                
        ctr += 1

    # Print summary statistics of the training and test data
    print('Amount of proofs used for training data:', math.floor(training_amount))
    print('Amount of proofs used for test data:', ctr - math.floor(training_amount))

    # Store training and test data as JSON and PyTorch tensor files
    training_data = {'verbalizedGoals': verbalizedGoals_training, 'symbolNames': symbolNames_training, 'normalizedScores': normalizedScores_training}
    test_data = {'verbalizedGoals': verbalizedGoals_test, 'symbolNames': symbolNames_test, 'normalizedScores': normalizedScores_test}

    # save the test and training data
    with open("trainingData.json", "w") as json_file:
        json.dump(training_data, json_file)
    with open("testData.json", "w") as json_file:
        json.dump(test_data, json_file)

    torch.save(training_data, 'trainingData.pt')
    torch.save(test_data, 'testData.pt')

# generate the test and training data
genTestAndTrainingData(80, preTrainingData, 2)  
