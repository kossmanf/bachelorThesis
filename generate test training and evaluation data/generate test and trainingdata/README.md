
#  Scripts for generating test and training data 

## Overview

This repository contains three Python scripts for generating training and test datasets from pre-training data. Each script handles the data splitting differently:

## Requirements for all scripts
- Python 3.x
- PyTorch
- tqdm

### generateTestAndTrainingData_all.py

This script splits all pre-training data into training and test sets. Each data point consists of a triplet: goal, score, and symbol. All data points are used for both training and testing.

#### Usage
1. Run the script with the desired percentage of data for training:

```sh
python generateTestAndTrainingData_all.py
```

#### Example

```python
genTestAndTrainingData(80, preTrainingData)
```

### generateTestAndTrainingData_random.py

This script randomly selects a specified amount of data points from the pre-training data for training and test sets.

#### Usage
1. Run the script with the desired percentage of data for training:

```sh
python generateTestAndTrainingData_random.py
```

#### Example

```python
genTestAndTrainingData(80, preTrainingData)
```

### 3. generateTestAndTrainingData_ratio.py

This script splits the data based on a specified ratio of positive and neutral symbols to negative symbols for training and testing.

#### Usage
1. Run the script with the desired percentage of data for training and the desired ratio:

```sh
python generateTestAndTrainingData_ratio.py
```

## Required folders from the scripts
Each script requires the following Folders:
- `./preTrainingDataCollection`: Directory containing a file for each conjecture which contains the conjecture the postive symbols with scores, the negative symbols with scores and the neutral sybols with scores. 

## Output from the scripts
Each script generates the following files:

- `trainingData.json`: JSON file containing the training data.
- `testData.json`: JSON file containing the test data.
- `trainingData.pt`: PyTorch tensor file containing the training data.
- `testData.pt`: PyTorch tensor file containing the test data.