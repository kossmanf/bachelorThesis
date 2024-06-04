# generateProofsWithOutLM.py

## Description
This Python script automates the generation of proofs using the E Prover software. It manages a file structure for storing proofs, attempts to find proofs for all the axioms files, and logs the outputs while maintaining the original categorical folder structure of the proof tasks.

## Requirements
- Python 3.x
- E Prover (Tested with version 2.6)
- Operating system with command-line interface
- Axiom files in the specified directory structure as per `_axiomsPath`

## Setup
1. Ensure E Prover is installed and the path to the E Prover executable is correctly set in the `_eproverPath` variable.
2. Create a directory named `proofLog` in the same directory as the script to store log files.

## Configuration
Edit the following variables in the script to match your environment:
- `_axiomsPath`: Path to the directory containing your axioms.
- `_proofLogFilePath`: Path where the proof logs will be stored.

## Running the Script
Execute the script in a command line interface:
```bash
python generateProofsWithOutLM.py
```

### Required directories
- `./axioms`: Folder with the axiom files to be proven.

## Output
The script will output proof results into a structured directory under `./proofsNormal` based on the category of each axiom. Each proof attempt is logged in the `proofLog.txt` file.

## Notes
- It is important to ensure that the E Prover is compatible with your system and the paths are correctly set.
- The script automatically handles the creation and cleanup of directories and files related to proof storage.
- If the `proofLog.txt` file is deleted and the program is restarted, existing proofs will be deleted and regeneration will occur.

# generateProofsWithLM.py

## Overview
`generateProofsWithLM.py` is a Python script that automates the process of generating proofs for axiomatic systems. It integrates Eprover, an automated theorem prover, with language model heuristics to enhance proof search. The script maintains a categorical file structure for organizing proofs and logs each proof attempt for the evaluation.

## Features
- **Automated Proof Generation**: Uses Eprover to automatically generate proofs.
- **Language Model Integration**: Enhances proof search with heuristics derived from a language model.
- **Structured Proof Management**: Organizes proofs into a structured file system based on categories.
- **Logging**: Logs each proof attempt in a dedicated log file.

## Requirements
- Python 3.8 or higher
- `tqdm`
- `transformers`
- `torch`
- A local installation of Eprover (specifically configured for the script).

## Setup
1. Ensure E Prover is installed and the path to the E Prover executable is correctly set in the `_eproverPath` variable.
2. Create a directory named `proofLog` in the same directory as the script to store log files.

## Configuration
- Configure paths and parameters within the script:
  - `_axiomsPath`: Directory containing axiom files.
  - `_eproverPath`: Path to the Eprover executable.
  - `_proofLogFilePath`: Path to the log file for recording proof attempts.

### Required imports from other programs`
- `from tptpParser.parseTree import generateParseTree`
- `from convertParseTreeToNaturalLanguage import generateSentence`
- `from symbolsBySimilarities import getSimilarities`

### Required Files and Directories
- `./state_dict_[number].pt`: File which contains the state dict of the model after the specified trained epoch. The number specifies the trained epoch.
- `./axioms`: Folder with the axiom files to be proven.

## Output
The script will output proof results into a structured directory under `./proofs` based on the category of each axiom. Each proof attempt is logged in the `proofLog.txt` file.

## Usage
To run the script:
```bash
python generateProofsWithLM.py
```
Ensure all configurations are set correctly as per your system's paths.

## Notice
The proofs without the language model is almost identical to the program that was used to generate the proofs for generating the traingn test and anaylsysis data
The Proofs with the language model and the proofs without the language model where conpared with each other
For trying to prove the conjectures from the `uncompletedProofs` the program ` generateProofsWithOutLM.py` 
For performing proofs without the auto paramter and without the languge model the progrm ` generateProofsWithOutLM.py`  was used as well

## Notice 

### Proof Generation Programs

Two primary two programs where used for the evaluation:

1. **Without the Language Model:**
   - `generateProofsWithOutLM.py` was utilized to generate proofs without using the language model. 

2. **With the Language Model:**
   - `generateProofsWithLM.py` was utilized to generate proofs with using the language model.
