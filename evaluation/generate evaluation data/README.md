# Overview
This Folder contains several Python scripts designed to generate data for the evaluation.

## findRedundantConjectures.py

### Description
Identifies duplicate proof tasks within the axiom files for evaluation and overlaps between axiom files for ealuation and training datasets. It extracts conjectures using regex, categorizes them, and saves the results in a JSON file.

### Required directories
- `./trainingAxioms`: axiom files used for generating the training data and test data for the language model.
- `./testAxioms`: axiom files used to generate the proofs for the evaluation.

## Output
- `./duplicates.json`: contains the dublicate axiom file paths from the axioms that where used to generate the proofs for the evaluation.
- `./commonConjectures.json`: contains the axiom file paths that where used for genearting the training and test data for the language model and for generating the proofs for the evlaluation.

### Usage
```bash
python findRedundantConjectures.py
```

## remOutputFiles.py

### Description
Removes specified output files that are identified as redundant so they dont have any impact on the evaluation.

### Required directories and files
- `./duplicates.json`: contains the dublicate axiom file paths from the axioms that where used to generate the proofs for the evaluation.
- `./commonConjectures.json`: contains the axiom file paths that where used for genearting the training and test data for the language model and for generating the proofs for the evlaluation.
- `./proofs`: Folder with the eprover output files from where the output files which are redundant w.r.t. the conjectures should be removed.

## Output
- `./proofs`: Folder with the output files without the redundant output files.

### Usage
```bash
python remOutputFiles.py
```

## gatherInformation.py

### Description
Aggregates information about wheter a proof was found and other specified information such as the number of processed clauses to find a proof used for evaluation.

### Required directories and files
- `./proofs`: eprover output files that where created by using the eprover with the language model.
- `./proofsNormal`: eprover output files that where created by using the eprover without the language model.

## Output
- `./extractedInformation.json`: A dictionary containing the extracted information from both types of output files with `proofs` and `proofsNormal` as keys.

### Usage
```bash
python gatherInformation.py
```