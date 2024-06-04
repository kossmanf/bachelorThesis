
# Symbol Embeddings scripts 

## Overview
This Folder contains two Python scripts for generating embeddings of logical symbols from the Adimen-SUMO ontology and returning them based on how similar they are two an other embedding.

### generateSymbolEmbeddings.py

#### Description
Generates embeddings for logical symbols using a fine-tuned sentence-transformer model and saves them to a text file.

## Requirements
- Python 3.x
- torch
- transformers
- JSON

### Required Files and Directories
- `./state_dict_[number].pt`: File which contains the state dict of the model after the specified trained epoch. The number specifies the trained epoch.
- `./as_cn_mapping_test.json`: File which maps Adimen-SUMO Symbols to natural language

### Output
- `./embeddings.txt`: Text file in which the embeddings for every symbol is stored readable with gensim.

#### Usage
Ensure you have the necessary dependencies installed and run:
```bash
python generateSymbolEmbeddings.py
```

### symbolsBySimilarities.py

#### Description
Computes the most and least similar embeddings from a symbol embeddings, based on cosine similarity.

## Requirements
- Python 3.x
- torch
- numpy
- gensim

### Required Files and Directories
- `./embeddings.txt`: Text file in which the embeddings for every symbol is stored readable with gensim.

### Required Parameters 
- `embeddingTensor1`: Tensor which the symbol embeddings should be compared to with the cosine similarity.

### Optional Parameters 
If the paramters are not set the 5 most similar and the 5 least simmilar symbols are returned
- `mostSimilar`: Number of most similar symbols to return.
- `leastSimilar`: Number of least similar symbols to return.
- `return_all`: Boolean if set to true all symbols will be returned and the number of specified most and least similar symbols is overwritten

### Output
- list with the specified symbols.

#### Usage
Adjust the input parameters as needed and execute:
```bash
python symbolsBySimilarities.py
```

