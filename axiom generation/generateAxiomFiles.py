# Importing necessary modules
import shutil
import os

# Program description
# This program takes the Adimen-SUMO axioms and a goal and combines them into a file that can be solved by the Eprover.

# Configuration constants

# Paths to the adimen sumo axioms and training goals
_adimenSumoAxiomsPath = './ApplyingCWA/1.OWA/E-KIFtoFOF/Axioms/adimen.sumo.tstp'
_trainingDataPath = './categorizedGoals'

# Deleting existing axiom folder and its contents

# Check if the axiom folder exists
if os.path.exists('./axioms'):
    # Iterate over each category in the axiom folder
    for category in os.listdir('./axioms'):
        # Iterate over each axioms file in the category folder
        for ax in os.listdir(os.path.join('./axioms/', category)):
            # Remove the axioms file
            os.remove(os.path.join('./axioms/', category, ax))
        # Remove the category folder
        os.rmdir(os.path.join('./axioms/', category))
    # Remove the axiom folder
    os.rmdir('./axioms')

# Creating the axiom folder
os.mkdir('./axioms')

# If the folder for the training data exists
if os.path.exists(_trainingDataPath):

    # Iterate over each category in the training data
    for category in os.listdir(_trainingDataPath):
        
        # Create a folder for axioms files corresponding to the category
        os.mkdir(os.path.join('./axioms/', category))

        # For every goal in the category
        for goal in os.listdir(os.path.join(_trainingDataPath, category)):

            # Create a new file for combined axioms and goal in the category folder
            with open(os.path.join('.','axioms', category, 'axioms_' + goal), 'w') as outfile:

                # Add the adimen sumo axioms to the new file
                with open(_adimenSumoAxiomsPath) as infile:
                    outfile.write(infile.read())

                # Add a newline separator
                outfile.write("\n")

                # Print a message indicating axiom generation
                print('Generating axiom ' + 'axioms_' + goal)

                # Add the goal to the new file
                with open(os.path.join(_trainingDataPath, category, goal)) as infile:
                    outfile.write(infile.read())
