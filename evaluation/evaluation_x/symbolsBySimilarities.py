# Importing necessary modules
from gensim.models import KeyedVectors
import numpy as np
import torch
from torch.nn import CosineSimilarity

# Program description
# This program takes an embedding as input and computes the specified number of most and least similar embeddings from a collection of embeddings. It uses cosine similarity to measure the similarity between embeddings.

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load embeddings using gensim
file_path = "embeddings.txt"

# Load the Word2Vec model from the specified file path
embeddings_model = KeyedVectors.load_word2vec_format(file_path, binary=False, encoding='utf-8')

# Define a function to calculate similarities between a given embedding tensor and all symbols in the Word2Vec model
def getSimilarities(embeddingTensor1: torch.Tensor, numMostCommon: int = 5, numMostUncommon: int = 5, return_all: bool = False):

    similarSymbols = {}
    cos = CosineSimilarity()  # Initialize cosine similarity function

    # Iterate manually over each symbol in the Word2Vec model
    for symbol in embeddings_model.index_to_key:
        # Calculate cosine similarity        
        embeddingTensor2 = torch.tensor([embeddings_model[symbol]], dtype=torch.float32).to(device)
        similarityPrediction = cos(embeddingTensor1, embeddingTensor2).item()
        similarSymbols[symbol] = similarityPrediction

    # Sort the symbols by their similarity scores in descending order
    sortedSymbols = sorted(similarSymbols.items(), key=lambda x: x[1], reverse=True)

    # Return either all symbols, a specified number of most common and most uncommon symbols, or a combination of both
    if return_all:
        return list(set(sortedSymbols))
    
    if numMostCommon == 0 and numMostUncommon == 0:
        return []
    
    if numMostCommon == 0:
        return sortedSymbols[-numMostUncommon:]
    elif numMostUncommon == 0:
        return sortedSymbols[:numMostCommon]
    
    return list(set(sortedSymbols[:numMostCommon] + sortedSymbols[-numMostUncommon:]))

