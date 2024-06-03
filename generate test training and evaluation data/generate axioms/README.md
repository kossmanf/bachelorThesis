
# Axiom File Generator

## Description
This Python script automates the preparation of axiom files for use with the Eprover theorem solver. Each axiom folder contains the axioms from Adimen-SUMO and a conjecture to be proven.

## Requirements
- Python 3.x
- shutil (standard library)
- os (standard library)

### Required Files and Directories
- `./categorized goals`: Folder which contains the goals in seperated folders sorted by category.
- `adimen.sumo.tstp`: File which contains the axioms from Adimen-SUMO.

### Output
- `./axioms`: Folder which contains the axiom files which contain the adimen sumo axioms and a conjecture sorted by category.

## Usage
To run the script, navigate to the script's directory and execute:
```bash
python generateAxiomFiles.py
```

Ensure that you have the necessary paths configured correctly, especially the paths to Adimen-SUMO axioms and training goals.

## Configuration
Modify the paths in the script to point to your local directories:
- `_adimenSumoAxiomsPath`: Path to Adimen-SUMO axioms.
- `_trainingDataPath`: Path to categorized goals.
