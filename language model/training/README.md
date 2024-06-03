
# README for training scripts

## training_lossFunctionComparison.py

### Overview
This program trains a machine learning model using PyTorch, comparing the performance of various loss functions. The script is designed to handle random subsets of a larger dataset, making it suitable for experiments with model training under different loss metrics.

### Requirements
- Python 3.x
- PyTorch
- transformers library
- tqdm
- numpy

### Dataset
The script requires a `.pt` file containing the dataset, structured with keys `verbalizedGoals`, `symbolNames`, and `normalizedScores`.

### Features
- Custom dataset loading.
- Random sampling of data points for training.
- Comparison of different loss functions such as MSE and Huber loss.
- Model checkpointing after each epoch.
- Model evaluation and final model saving.

### How to Run
1. Ensure that you have a dataset file named `trainingData.pt`.
2. Adjust the `data_file`, `batch_size`, and `epochs` variables as needed.
3. Run the script using a Python environment that satisfies the requirements.

### Configuration Options
- `data_file`: Path to the dataset file.
- `batch_size`: Number of samples per batch.
- `epochs`: Number of training epochs.
- `criterion`: Specifies the loss function used for model training. Options include `MSELoss`, `HuberLoss`, etc. Set this by modifying the `criterion` variable in the script.

### Output
- Checkpoint files for each epoch.
- A final model saved as `final_model.pt`.

## training_mseLoss.py

### Overview
This program trains a machine learning model with the MSE (Mean Squared Error) loss function using PyTorch. It's designed for evaluating and optimizing model performance specifically under MSE loss conditions.

### Requirements
- Python 3.x
- PyTorch
- transformers library
- tqdm
- numpy

### Dataset
The script expects a `.pt` file formatted with `verbalizedGoals`, `symbolNames`, and `normalizedScores`.

### Features
- Custom dataset loading with shuffling.
- MSE Loss specific training regime.
- Model checkpointing after each epoch with detailed loss tracking.
- Final model saving.

### How to Run
1. Prepare a dataset file named `trainingData.pt`.
2. Configure `data_file`, `batch_size`, and `epochs` variables as required.
3. Execute the script within a Python environment meeting all dependencies.

### Configuration Options
- `data_file`: Path to your dataset file.
- `batch_size`: Number of examples per batch.
- `epochs`: Total number of epochs for training.

### Output
- Epoch-specific checkpoint files containing model state and optimizer details.
- A final model saved in the file `final_model.pt`.
