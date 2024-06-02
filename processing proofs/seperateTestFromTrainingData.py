# Importing necessary modules
import math
import shutil
import random
import json

# Program description
# This script processes the 'completed proofs' folder containing successful eprover outputs.
# It distributes a specified percentage of proofs from each category into a 'training proofs' folder and the remainder into a 'test proofs' folder.
# The original categorical folder structure will be maintained.

# The 'completed_proofs' folder contains training data for the language model, testing data for model validation.
# The 'uncompleted_proofs' folder holds files reserved for future evaluations, where the trained language model will be used as a heuristic to attempt solving the goals of the output files again.

# Configuration Constants

# Percentage of goals to be chosen as trainingGoals of each category
_percentage = 80

# Deleting the trainingGoals and testGoals folder if they exist

# If the trainingProofs folder exists, delete its contents and the folder itself
if os.path.exists('./trainingProofs'):
    for category in os.listdir('./trainingProofs'):
        for goal in os.listdir(os.path.join('.', 'trainingProofs', category)):
            os.remove(os.path.join('.', 'trainingProofs', category, goal))
        os.rmdir(os.path.join('.', 'trainingProofs', category))
    os.rmdir('./trainingProofs')

# If the testProofs folder exists, delete its contents and the folder itself
if os.path.exists('./testProofs'):
    for category in os.listdir('./testProofs'):
        for ted in os.listdir(os.path.join('.', 'testProofs', category)):
            os.remove(os.path.join('.', 'testProofs', category, ted))
        os.rmdir(os.path.join('.', 'testProofs', category))
    os.rmdir('./testProofs')

# Creating the folders for the training goals and the test goals
os.mkdir('./trainingProofs')
os.mkdir('./testProofs')

# Creating a dictionary with categories as keys and the different goals that belong to the category as values
categories = dict()

# Creating the dictionary
# For every category in the completedProofs folder
for category in os.listdir('completedProofs'):
    for goal in os.listdir(os.path.join('.', 'completedProofs', category)):
        # If the category is not in the dictionary, create the category as a key and add the goal as value; otherwise, add the goal to the category as a value
        if not (category in categories):
            categories[category] = [goal]
        else:
            categories[category].append(goal)

# Randomly sorting the categories to select random categories as training and testing data
# For every category in the dictionary
for category in categories:
    random.shuffle(categories[category])

# For every category in the dictionary
for category in categories:

    # Calculate the amount of goals to be chosen as training data
    amount = math.ceil((_percentage / 100) * len(categories[category]))

    # Create a folder for the category in the trainingProofs folder and in the testProofs folder
    os.mkdir(os.path.join('.', 'trainingProofs', category))
    os.mkdir(os.path.join('.', 'testProofs', category))

    # Count variable for the goals to choose the amount of goals for the training data
    count = 0

    # For every goal in a category
    for goal in categories[category]:

        # Increment the count
        count = count + 1

        # If the count is less than the amount of goals for the training goals, add the goal to the category folder in the trainingProofs folder; otherwise, add it to the category in the testProofs folder
        if(count < amount):
            print('Copying training goal: ' + goal)
            shutil.copy(os.path.join('.', 'completedProofs', category, goal), os.path.join('.', 'trainingProofs', category))
        else:
            print('Copying test goal: ' + goal)
            shutil.copy(os.path.join('.', 'completedProofs', category, goal), os.path.join('.', 'testProofs', category))

# Printing the dictionary containing categories and their corresponding goals
print(categories)