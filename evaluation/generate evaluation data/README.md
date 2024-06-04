
# Overview
This Folder contains several Python scripts designed to generate data for the evaluation.

## findRedundantConjectures.py

### Description
Identifies duplicate proof tasks within test data and overlaps between test and training datasets. It extracts conjectures using regex, categorizes them, and saves the results in a JSON file.

### Required directories
- `./testAxioms`: Folder with the axiom files only containing the files with the conjectures that where used to proof the specified output files.




### Usage
```bash
python findRedundantConjectures.py
```

## remOutputFiles.py

### Description
Removes specified output files that are identified as redundant so they dont have any impact on the evaluation.

### Usage
```bash
python remOutputFiles.py
```

## gatherInformation.py

### Description
Aggregates information from specified sources, processes it, and outputs it in a structured format. Useful for data analysis and consolidation tasks.

### Usage
```bash
python gatherInformation.py
```

## Requirements

- Python 3.x
- tqdm (for progress bars)
- json (for handling JSON files)