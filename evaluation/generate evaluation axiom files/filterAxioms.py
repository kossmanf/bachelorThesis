# Importing necessary modules
import os
from tqdm import tqdm

# Program description
# This program removes any axioms that are not used for evaluation.
# It iterates over the output files from the epover that are designated for evaluation (test proofs or uncompleted proofs) to generate the necessary axiom files.
# Caution: Using this program will result in the deletion of all other axioms!

#  Collect axiom names from specified proof directory.
def collectAxiomNames(proofDirectory):
    # list for the test axiom names
    axiomNames = []

    for proofCategory in tqdm(os.listdir(proofDirectory), desc="Collecting Axioms from Proofs"):
        for proofName in os.listdir(os.path.join(proofDirectory, proofCategory)):
            # generate the axiom file based on the eprover output file
            axiomNames.append('axioms' + proofName[5:])
    return axiomNames

# # Removing axioms not present in test axiom names
def removeUnusedAxioms(axiomDirectory, usedAxioms):
    for proofCategory in tqdm(os.listdir(axiomDirectory), desc="Removing Unused Axioms"):
        for axiomName in tqdm(os.listdir(os.path.join(axiomDirectory, proofCategory)), desc="Processing Axioms"):
            if axiomName not in usedAxioms:
                os.remove(os.path.join(axiomDirectory, proofCategory, axiomName))
                print(f"Removed: {axiomName}")

proofDirectory = './uncompletedProofs'
#proofDirectory = './testProofs'
#proofDirectory = './trainingProofs'

# Collecting the axiom names 
usedAxioms = collectAxiomNames(proofDirectory)

# Removing axioms not present in collected axiom names
removeUnusedAxioms('./axioms', usedAxioms)
