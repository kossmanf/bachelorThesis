import os
import re
import json

# Define the path to the proof folder
_path_to_proof_folder = './trainingProofs'

# Function to remove existing pre-training data
def remove_existing_pretraining_data():
    # Remove positive pre-training data
    if os.path.exists('./preTrainingData/posPreTrainingData'):
        for category in os.listdir('./preTrainingData/posPreTrainingData'):
            category_path = os.path.join('./preTrainingData/posPreTrainingData', category)
            for file in os.listdir(category_path):
                os.remove(os.path.join(category_path, file))
            os.rmdir(category_path)
        os.rmdir('./preTrainingData/posPreTrainingData')

    # Remove negative pre-training data
    if os.path.exists('./preTrainingData/negPreTrainingData'):
        for category in os.listdir('./preTrainingData/negPreTrainingData'):
            category_path = os.path.join('./preTrainingData/negPreTrainingData', category)
            for file in os.listdir(category_path):
                os.remove(os.path.join(category_path, file))
            os.rmdir(category_path)
        os.rmdir('./preTrainingData/negPreTrainingData')

    # Remove the preTrainingData folder
    if os.path.exists('./preTrainingData'):
        os.rmdir('./preTrainingData')

# Create the preTrainingData folder
os.mkdir('./preTrainingData')

# Create the posPreTrainingData folder
os.mkdir('./preTrainingData/posPreTrainingData')

# Create the negPreTrainingData folder
os.mkdir('./preTrainingData/negPreTrainingData')

# Check if the proof folder exists
if os.path.exists(_path_to_proof_folder):
    # Loop through categories in the proof folder
    for category in os.listdir(_path_to_proof_folder):
        # Create folders for positive and negative pre-training data
        os.mkdir(f'./preTrainingData/posPreTrainingData/{category}')
        os.mkdir(f'./preTrainingData/negPreTrainingData/{category}')

        # Loop through proofs in the current category
        for proof in os.listdir(os.path.join(_path_to_proof_folder, category)):
            pos_pre_training_data = {}
            neg_pre_training_data = {}
            pos_pre_training_data_conjecture = []
            neg_pre_training_data_conjecture = []

            # Open the proof file
            with open(os.path.join(_path_to_proof_folder, category, proof), "r") as proof_file:
                lines = proof_file.readlines()

                conjecture = ''
                # Loop through lines in the proof file
                for line in lines:
                    # Extract conjecture formula
                    if len(line) > 3:
                        prefix = line[:3]
                        if prefix == 'fof':
                            formula_type = re.findall('\w+(?=,)', line)[1]
                            if formula_type == 'conjecture':
                                conjecture = re.findall('(?<=conjecture, )(.*)(?=, file)', line)[0]

                    # Extract positive and negative training data
                    if len(line) > 9:
                        suffix = line[-9:].strip()
                        if suffix == "trainpos":
                            ptd = line[:-11].strip()
                            ptd = re.findall('(?:plain, |negated_conjecture, )(.+)(?=\).)', ptd)
                            if len(ptd) == 1:
                                pos_pre_training_data_conjecture.append(ptd[0])
                        elif suffix == "trainneg":
                            ntd = line[:-10].strip()
                            ntd = re.findall('(?:plain, |negated_conjecture, )(.+)(?=\).)', ntd)
                            if len(ntd) == 1:
                                neg_pre_training_data_conjecture.append(ntd[0])

            # Store positive and negative pre-training data
            pos_pre_training_data[conjecture] = pos_pre_training_data_conjecture
            neg_pre_training_data[conjecture] = neg_pre_training_data_conjecture

            # Save positive pre-training data
            if len(pos_pre_training_data_conjecture) > 0:
                with open(f'./preTrainingData/posPreTrainingData/{category}/posPreTrainingData_owa_{proof[:-5]}.json', 'w') as file:
                    json.dump(pos_pre_training_data, file)

            # Save negative pre-training data
            if len(neg_pre_training_data_conjecture) > 0:
                with open(f'./preTrainingData/negPreTrainingData/{category}/negPreTrainingData_owa_{proof[:-5]}.json', 'w') as file:
                    json.dump(neg_pre_training_data, file)