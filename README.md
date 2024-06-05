# Project Overview
Repository for the Bachelor's Thesis on the Topic of Goal-Directed Reasoning in First-Order Logic through Learning from Proofs Using Large Language Models at Trier University of Applied Sciences.

## Directories

### generate training test and evaluation data
Contains the programs used for generating the training and test data for the language model, as well as the data for evaluating the performance of the prover.

### language model
Contains programs to fine-tune the language model and evaluate the performance of the language model.

### evaluation
Contains programs to evaluate the performance of the prover with and without the fine-tuned language model as a heuristic.

### tptp parser
Contains programs to extract the symbols from a formula in TPTP format and translate a formula into natural language.

### hardware information
Contains programs to get information about the environment under which the evaluation and training of the language model was performed.

## Requirements
This project requires a local installation of the Eprover.  The Eprover can be downloaded from https://github.com/eprover/eprover

## Usage
Refer to the README.md files in each directory for detailed instructions on how to run the programs within. Ensure that you have the necessary Python environment and dependencies installed.

## License
This project is licensed under the MIT License.
