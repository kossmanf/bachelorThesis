
# Goal Categorization Script

## Overview
This script automates the categorization of goal files from the Adimen SUMO project. It sorts these files into corresponding folders based on their names, facilitating easier management and analysis of the goals. The program handles directory setup, cleanup, and reorganization of files to suit project needs.

## Features
- **Directory Management**: Automatically checks for and cleans up the existing directory structure before categorization.
- **File Organization**: Categorizes goal files into dedicated folders based on predefined categorization logic, making it easier to locate and analyze specific types of goals.

## Requirements
- Python 3.x
- OS module
- RE module (Regular Expression)
- SHUTIL module (Shell Utilities)

## Setup
1. Ensure Python 3.x is installed on your system.
2. Place the script in the root directory where the goal files are stored.

## Usage
To run the script, navigate to the script's directory in your terminal and execute:
```bash
python categorizeGoals.py
```

## How It Works
The script performs the following operations:
1. Checks for the presence of a directory named `categorizedGoals`. If it exists, the script cleans it by removing all files and subdirectories.
2. Reads goal file names from a predefined source directory.
3. Categorizes each file based on its name into the corresponding folder within the `categorizedGoals` directory.

## Caution
Before running the script, ensure that you have backups of your data as it deletes existing files in the `categorizedGoals` folder to prevent duplication and maintain organization.
