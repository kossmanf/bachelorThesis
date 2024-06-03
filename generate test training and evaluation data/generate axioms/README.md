
# Axiom File Generator

## Description
This Python script automates the preparation of axiom files for use with the Eprover theorem solver. It primarily handles axiom files from Adimen-SUMO, organizing them with specified training goals into a coherent structure that can be processed efficiently.

## Features
- Deletes existing axiom directories and their contents to ensure a fresh start.
- Automatically combines Adimen-SUMO axioms with specified goals.
- Organizes combined files into a structure suited for theorem solving with Eprover.

## Installation
Clone the repository to your local machine:
```bash
git clone [URL-to-your-repository]
cd [repository-name]
```

## Requirements
- Python 3.x
- shutil (standard library)
- os (standard library)

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
