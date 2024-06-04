# Filter Axioms Program

## Overview

The Filter Axioms program is a Python script designed to optimize the storage and processing of axiom files in proof evaluation environments. It selectively removes axiom files that are not used in designated proof evaluations, specifically test proofs or uncompleted proofs, thus conserving storage and improving processing efficiency.

## Caution

**This script will delete files!** It's designed to remove axioms not used in test proofs, which means it will permanently delete files from the `./axioms` directory that are not listed in the test proofs. 

## Requirements
- Python 3.x
- `tqdm` library for progress bars (install with `pip install tqdm`)

### Required Files and Directories
- `./uncompletedProofs` or `./testProofs`: Folter with the eprover output files from which the axioms should be filtered.

### Output
- `./axioms`: Folder with the axiom files only containing the files with the conjectures that where used to proof the specified output files.

## Usage
1. Ensure the checkpoint file for the desired epoch is named appropriately (e.g., `checkpoint_epoch_[number].pt`).
2. Run the script:
   ```bash
   python filterAxioms.py
