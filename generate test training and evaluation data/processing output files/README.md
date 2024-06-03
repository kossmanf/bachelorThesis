
# README for Python Scripts

## 1. separateCompletedFromUncompletedProofs.py

### Overview
This Python script processes eprover output files from the 'proofs' directory, sorting them into 'completed_proofs' and 'uncompleted_proofs' based on whether proofs were found.
The 'uncompmleted' proofs are used as analysis data.

### Requirements
- Python 3.x
- `os` module
- `shutil` module

### Required Directories
- `./proofs`: Directory containing the output files from the eprover.

### Output
- `./completed proofs`: Folder which holds the output files of proofs which where found.
- `./uncompleted proofs`: Folder which holds the output files of proofs which where not found.

### Usage
1. Run the script with the command:
   ```
   python separateCompletedFromUncompletedProofs.py
   ```

---

## 2. separateTestFromTrainingData.py

### Overview
This script divides proofs from the 'completedProofs' folder into 'trainingProofs' and 'testProofs' directories based on a specified percentage.
The 'test' proofs are used as analysis data.

### Requirements
- Python 3.x
- `os`, `shutil`, `random`, `math` modules

### Required Directories
- `./completed proofs`: Folder which holds the output files of proofs which where found.

### Output
- `./test proofs`: output files which are used for analysis.
- `./training proofs`: Folder which holds the output files which are used to generate the test and training data for training the language model.

### Configuration
- Set the desired percentage of training data at the beginning of the script. Default is typically set to 70%.

### Usage
1. Run the script with the command:
   ```
   python separateTestFromTrainingData.py
   ```
