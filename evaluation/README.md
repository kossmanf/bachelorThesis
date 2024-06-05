# Evaluation Tools

This Folder contains organized folders, each dedicated to a specific aspect of the evaluation process.

## Folder Descriptions

### generate eval state dict
This folder contains programs necessary for extracting state dictionaries from specific epoch training  checkpoint. This state dict is used for model evaluation.

### generate evaluation axiom files
This folder contains tools to create axiom files that are essential for the evaluation process. Each file contains the Adimen-SUMO axioms with a proof task.

### generate symbol embeddings
This folder contains programs  to generate symbol embeddings, which help the language model predict the relevance of symbols in relation to proof tasks.

### generate Proofs
This folder contains programs that generate proofs using the axiom files prepared earlier. These proofs are used for further evaluation.

### generate evaluation Data
This folder contains programs that process the generated proofs to produce structured evaluation data. This data is used for the analysis.

### statistical analysis
This folder contains tools for performing statistical analysis on the evaluation data. The analysis helps in understanding the performance of the eprover.
