# Folder Descriptions for Generating Test, Training, and Analysis Data

This directory is organized into several folders, each containing scripts and tools for different stages of generating test, training, and analysis data for language models. Below is a detailed explanation of the contents and purpose of each folder.

## Folder Structure

1. **categorizing goals**
2. **generate axioms**
3. **generate proofs**
4. **processing output files**
5. **generate pre training data**
6. **generate test and training data**

### 1. categorizing goals

This folder contains scripts for categorizing the Adimen-SUMO goals. These scripts organize the goals into specific categories.

### 2. generate axioms

This folder contains scripts designed to generate axiom files which can be solved by the eprover. Each axiom file consists of a set of axioms and one conjecture.

### 3. generate proofs

This folder includes scripts that attempt to solve the axiom files created in the `generate axioms` folder. The primary purpose of these scripts is to generate proofs for the conjectures based on the provided axioms.

### 4. processing output files

This folder contains scripts for processing the output files generated by the proof attempts in the `generate proofs` folder. The main tasks performed by these scripts include:
- Splitting the output files into those used for training and those used for analysis.

### 5. generate pre training data

This folder generates the pre training data. Each data point in the pre-training set includes a goal, a symbol, and a score that indicates how well the symbol aligns with the goal.

### 6. generate test and training data

This folder contains scripts to generate the final test and training data for the language model.