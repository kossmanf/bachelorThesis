# Modules to be imported
import os
import re
import shutil

# program description
# This program categorizes goals based on their names.

# Configuration constants

# Path to the goals in Adimen SUMO
_adimenSumoGoalsPath = './ApplyingCWA/1.OWA/E-KIFtoFOF/Goals'

# Deleting the goal data folder

# If the 'categorizedGoals' folder exists, go into each category folder in it,
# delete the goals within each category folder, then delete the category folder,
# and finally delete the 'categorizedGoals' folder itself.
if os.path.exists('./categorizedGoals'):
    for category in os.listdir('./categorizedGoals'):
        for goal in os.listdir(os.path.join('.', 'categorizedGoals', category)):
            os.remove(os.path.join('.', 'categorizedGoals', category, goal))
        os.rmdir(os.path.join('.', 'categorizedGoals', category))
    os.rmdir('./categorizedGoals')

# Creating the folder for the categorizedGoals
os.mkdir('./categorizedGoals')

# Creating a dictionary with categories as keys and the different goals that belong to each category as values
categories = dict()

# Creating the dictionary
# For every goal
for goal in os.listdir(_adimenSumoGoalsPath):
    # Extracting the category from the name of the goal
    category = re.split(r'(\d+)', goal)[0]
    # If the category is not in the dictionary, create the category as a key
    # and add the goal as a value. Otherwise, add the goal to the category's
    # list of values.
    if category not in categories:
        categories[category] = [goal]
    else:
        categories[category].append(goal)

# Iterate over every category in the 'categories' dictionary
for category in categories:
    # Create a folder for the category
    os.mkdir(os.path.join('categorizedGoals', category))
    # Copy the goals that belong to the category into the category folder
    for goal in categories[category]:
        print('Copying goal: ' + goal)
        shutil.copy(os.path.join(_adimenSumoGoalsPath, goal), os.path.join('.', 'categorizedGoals', category))
