# Extract state Dictionary from Checkpoint

This script, `extractStateDictFromCheckpoint.py`, is designed to extract the state dictionary from a checkpoint file for the analysis.

## Requirements
- `torch` - PyTorch library, used for model operations and loading checkpoints.
- `transformers` - Provides access to pre-trained models and utilities for working with them.

### Required Files and Directories
- `./checkpoint_epoch_[number].pt`: Checkpoint file generated after the training of a certaint epoch. The number specifies the trained epoch.

### Output
- `./state_dict_[number].pt`: File which contains the state dict of the model after the specified trained epoch. The number specifies the trained epoch.

## Usage
1. Ensure the checkpoint file for the desired epoch is named appropriately (e.g., `checkpoint_epoch_[number].pt`).
2. Run the script:
   ```bash
   python extractStateDictFromCheckpoint.py
