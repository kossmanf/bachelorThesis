
# Readme about the scripts for the statistical analysis

This Folder contains the scripts used for the statistical analysis in the evaluation.

## calculateStatistics.py 

This program calculates various statistical measures based on the `extractedInformation.json` file to evaluate the performance and efficiency of solving proofs without the use of a Language Model (LM). The following are the statistics it calculates:

## Overview of Calculated Statistics:

1.  Total Proof Tasks: This indicates the total number of proof tasks that have been tried to solve.
2. Solved Proofs Without LM: It shows the count of proof tasks that were solved.

### Clause-related Statistics:

1. Total Processed Clauses Without LM: This measures the total number of clauses processed to solve all proofs  without the language model.
2. Mean Processed Clauses Without LM: This calculates the average number of clauses processed per tasks without the language models.
3. Standard Deviation of Processed Clauses Without LM: This computes the standard deviation of the number of processed clauses, providing a measure of variability.
4. Median Processed Clauses Without LM: This statistic shows the median number of clauses processed, indicating the central tendency.

### Output:

All computed statistics are then saved into a file named `statistics.json` for documentation and further analysis.

### Usage
1. Run the script:
   ```bash
   python calculateStatistics.py 

## calculateStatistics_comparison.py

This program calculates various statistical measures based on the `extractedInformation.json` file to evaluate the performance and efficiency of solving proofs without the use of a Language Model (LM) and with the use of a language model (LM) for a comparison. The following are the statistics it calculates:

## Overview of Calculated Statistics:

1.  Total Proof Tasks: This indicates the total number of proof tasks that have been tried to solve.
2. Solved Proofs without and with LM: It shows the count of proof tasks that were solved.

### Clause-related Statistics:

1. Total Processed Clauses with and without LM: This measures the total number of clauses processed to solve all proofs with and without the language model.
2. Mean Processed Clauses with and without LM: This calculates the average number of clauses processed per tasks with and without the language model.
3. Standard Deviation of Processed Clauses with and without LM: This computes the standard deviation of the number of processed clauses, providing a measure of variability.
4. Median Processed Clauses with and without LM: This statistic shows the median number of clauses processed, indicating the central tendency.

### Reduction Proportions:
Percentage Fewer Clauses Without LM and With LM: Reflects the reduction in the number of clauses processed when comparing methods without and with the language model.
Percentage Similar Clauses: Shows the percentage of tasks where the number of clauses processed were similar between methods.

### Overall Reduction Statistics:
Average Percentage Reduction: The average percentage reduction in the processed clauses with and without the use of the language model.
Average Percentage Reduction Std: Standard deviation of the percentage reductions in the procesessed clauses with and without the use of the language model, indicating variability in efficiency gains.
Median Percentage Reduction: Median of percentage reductions in the procesessed clauses with and without the use of the language model, providing a central tendency measure for efficiency gains.

### Visualization 

The number of processed clauses and the reduction percentages are visualized in a graph for a clearer graphical representation. 

### Output:

All computed statistics are then saved into a file named `statistics.json` for documentation and further analysis.

### Usage
1. Run the script:
   ```bash
   python  calculateStatistics_comparison.py

## countProofs.py

This script counts the number of attempted proofs and the number of successful found proofs based on the `./proofs` folder which contains the eprover output files. The numbers are printed out on th console.

### Usage
1. Run the script:
   ```bash
   python  countProofs.py

## plotNumProcessedClauses.py

This script generates a visual representations of the number of processed clauses based on the `extractedInformation.json` file.

### Usage
1. Run the script:
   ```bash
   python  plotNumProcessedClauses.py

## plotProcessedClausesResiduals.py

This script generates a visual representations based on the `statistics.json` file of the residuals between the proofs found with the use of the language model and the proofs found without the use of the languge model.

### Usage
1. Run the script:
   ```bash
   python  plotProcessedClausesResiduals.py

### Requirements

The specified files which form the basis for calculating statistics and generating visualizations.







