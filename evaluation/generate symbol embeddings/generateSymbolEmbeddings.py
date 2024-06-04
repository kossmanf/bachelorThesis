# Importing necessary modules
from transformers import AutoModel, AutoTokenizer
from torch.nn.functional import normalize 
import torch
import json
from torch.nn import CosineSimilarity

# Program description
# This program generates embeddings for logical symbols from the Adimen-SUMO ontology and saves them in  a text file.

# device and tokenizer 
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# load the fine tuned model
trained_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Load the saved state dict
state_dict = torch.load('state_dict_1.pt')

# Modify the state dictionary to remove 'embeddings.position_ids' if it's present but not needed
if 'embeddings.position_ids' in state_dict:
    del state_dict['embeddings.position_ids']

# Load model state dictionary
trained_model.load_state_dict(state_dict)

# Moving model to the GPU
trained_model.to(device)
print(f"model moved to {device}")

# setting the trained model in eval mode
trained_model.eval()

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def getEmbeddings(model, tokenizer, sentences):
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    #sentence_embeddings = normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings

def splitCamelCase(word):
    newWord = ''
    wordIndex = 0
    for i in range(0, len(word)):
        if(i == len(word)-1):
            newWord = newWord + word[wordIndex:len(word)]
        elif(i != 0 and word[i-1] != ' ' and word[i].isupper() and word[i+1].islower()):
            newWord = newWord + word[wordIndex:i] + ' '
            wordIndex = i
    return newWord

def splitAtUnderscores(word):
    newWord = ''
    for subword in word.split('_'):
        if(subword != ''):
            newWord = newWord + subword + ' '
    newWord = newWord[0:-1]
    return newWord



with open('./as_cn_mapping_test.json', 'r') as file:
    wordMapping = json.load(file)

embeddings = {}

for symbolName in wordMapping:
    word = splitCamelCase(splitAtUnderscores(wordMapping[symbolName][0])) 
    symbolEmbedding = getEmbeddings(trained_model, tokenizer, [word])
    embeddings[symbolName] = symbolEmbedding.tolist()[0]

# Assuming embeddings is a dictionary with words as keys and their embeddings as values
dimension = len(next(iter(embeddings.values())))  # Get the dimensionality of the embeddings

# Define the path to the text file where you want to save the embeddings
file_path = "embeddings.txt"

# Write embeddings to the text file
with open(file_path, "w") as file:
    file.write(f"{len(embeddings)} {dimension}\n")  # Write dimensions to the first line
    for symbol, embedding in embeddings.items():
        embedding_line = " ".join([str(val) for val in embedding])
        file.write(symbol + " " + embedding_line + "\n")
