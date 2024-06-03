
# Goal Categorization Script

## Overview
This script automates the categorization of goal files from the Adimen SUMO project. It sorts these files into corresponding folders based on their names, facilitating easier management and analysis of the goals. The program handles directory setup, cleanup, and reorganization of files to suit project needs.

## Requirements
- Python 3.x
- OS module
- RE module (Regular Expression)
- SHUTIL module (Shell Utilities)

### Required Directories
- `./goals`: Directory which contains the Adimen-SUMO goals.

### Rquired Folders
- `./axioms`: Folder which contains the axiom files which contain the adimen sumo axioms and a conjecture sorted by category.

### Output
- `./categorized goals`: Folder which contains the goals in seperated folders sorted by category.

## Usage
To run the script, navigate to the script's directory in your terminal and execute:
```bash
python categorizeGoals.py
```

## Caution
Before running the script, ensure that you have backups of your data as it deletes existing files in the `categorizedGoals` folder to prevent duplication and maintain organization.
