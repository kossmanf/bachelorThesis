# Importing necessary modules
import os 
from tqdm import tqdm

# Program description
# This program removes any axioms that are not used for evaluation.
# It iterates over the output files from the epover that are designated for evaluation (test proofs) to generate the necessary axiom files.
# Caution: Using this program will result in the deletion of all other axioms!

# list for the test axiom names
testAxioms = []

# Collecting the test axiom names from the test proofs
for proofCategory in tqdm(os.listdir('./testProofs'), desc="Collecting Test Axioms"):
    for proofName in os.listdir(os.path.join('./testProofs', proofCategory)):
        testAxioms.append('axioms' + proofName[5:])

# Removing axioms not present in test axiom names
for proofCategory in tqdm(os.listdir('./axioms'), desc="Removing Unused Axioms"):
    for axiomName in tqdm(os.listdir(os.path.join('./axioms', proofCategory)), desc="Processing Axioms"):
        if axiomName not in testAxioms:
            os.remove(os.path.join('./axioms', proofCategory, axiomName))
