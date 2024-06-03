
# Generate Proofs Automation Script

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
python generateProofs.py
```

### Required directories
- `./axioms`: Folder which contains the axiom files which contain the adimen sumo axioms and a conjecture sorted by category.

## Output
The script will output proof results into a structured directory under `./proofs` based on the category of each axiom. Each proof attempt is logged in the `proofLog.txt` file.

## Notes
- It is important to ensure that the E Prover is compatible with your system and the paths are correctly set.
- The script automatically handles the creation and cleanup of directories and files related to proof storage.
- If the `proofLog.txt` file is deleted and the program is restarted, existing proofs will be deleted and regeneration will occur.

