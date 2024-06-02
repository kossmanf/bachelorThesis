import os 
from tqdm import tqdm

# list for the test axiom names
testAxioms = []

# Collecting the test axiom names from the test proofs
for proofCategory in tqdm(os.listdir('./testProofs'), desc="Collecting Test Axioms"):
    for proofName in os.listdir(os.path.join('./testProofs', proofCategory)):
        testAxioms.append('axioms' + proofName[5:])
print(testAxioms)

# Removing axioms not present in test axiom names
for proofCategory in tqdm(os.listdir('./axioms'), desc="Removing Unused Axioms"):
    for axiomName in tqdm(os.listdir(os.path.join('./axioms', proofCategory)), desc="Processing Axioms"):
        if axiomName not in testAxioms:
            os.remove(os.path.join('./axioms', proofCategory, axiomName))
