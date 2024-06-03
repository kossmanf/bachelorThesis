
# README for Python Scripts

## 1. separateCompletedFromUncompletedProofs.py

### Overview
This Python script processes eprover output files from the 'proofs' directory, sorting them into 'completed_proofs' and 'uncompleted_proofs' based on whether proofs were found.

### Requirements
- Python 3.x
- `os` module
- `shutil` module
- Input proofs should be in a directory named 'proofs' at the script's location.

### Usage
1. Run the script with the command:
   ```
   python separateCompletedFromUncompletedProofs.py
   ```

---

## 2. separateTestFromTrainingData.py

### Overview
This script divides proofs from the 'completedProofs' folder into 'trainingProofs' and 'testProofs' directories based on a specified percentage.

### Requirements
- Python 3.x
- `os`, `shutil`, `random`, `math` modules
- Input proofs should be organized in a directory named 'completedProofs'  at the script's location.

### Configuration
- Set the desired percentage of training data at the beginning of the script. Default is typically set to 70%.

### Usage
1. Run the script with the command:
   ```
   python separateTestFromTrainingData.py
   ```
