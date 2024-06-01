import json
import torch
import math
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
from torch.nn.functional import normalize 
from torch.nn import CosineSimilarity
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import torch

# This program processes different backed-up epoch files by extracting the state disc to evaluate the trained model at each epoch.
# It assesses the performance of both the trained and untrained models using test data. 
# For each epoch, the program generates an evaluation file containing the calculated residuals (predicted score - actual score), along with the actual and predicted scores.

# device and tokenizer 
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# load the orginal model
original_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Moving model to the GPU
original_model.to(device)
print(f"model moved to {device}")

original_model.eval()

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Function ro generate the embeddings 
def getEmbeddings(model, tokenizer, sentences):
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    return sentence_embeddings

# Function to calculate the predicted score based with the cosine similarity based on the embeddings
def calculatePredictedScore(verbalizedGoal, symbol, tokenizer, model):
    # calculate the goal and the symbol embedding 
    goalEmbedding = getEmbeddings(model, tokenizer, [verbalizedGoal])
    symbolEmbedding = getEmbeddings(model, tokenizer, [symbol])

    # calculate the cosine similarity between the embeddings
    cos = CosineSimilarity()
    predictedScore = cos(goalEmbedding, symbolEmbedding).item()

    return predictedScore

# Load the test data
data = torch.load('testData.pt')
symbolNames = data['symbolNames']
verbalizedGoals = data['verbalizedGoals']
normalizedScores = data['normalizedScores']
amount_of_samples = len(verbalizedGoals)

# Set the target number of data points to randomly select
amount = 2000

# Generate a list of `amount` unique random indices from the dataset's range
indices = [random.randint(0, amount_of_samples - 1) for _ in range(0, amount)]

# Update verbalizedGoals, symbolNames, and normalizedScores with data at selected indices
verbalizedGoals = [verbalizedGoals[i] for i in indices]
symbolNames = [symbolNames[i] for i in indices]
normalizedScores = [normalizedScores[i] for i in indices]

# update the length
amount_of_samples = amount

# Iterate over checkpoint files
for epoch in tqdm(range(0, 3)):  
    # Construct checkpoint file path
    checkpoint_path = f"checkpoint_epoch_{epoch}.pt"

    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path)

    # Load the trained model
    trained_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    # Load model state dictionary
    state_dict = checkpoint['model_state_dict']

    # Modify the state dictionary to remove 'embeddings.position_ids' if it's present but not needed
    if 'embeddings.position_ids' in state_dict:
        del state_dict['embeddings.position_ids']

    trained_model.load_state_dict(state_dict, strict=False)
    
    # load model into memory
    trained_model.to(device)

    trained_model.eval()

    # Lists for saving the residuals for highest and lowest scores
    trainedResiduals = []
    untrainedResiduals = []
    predictedScores_trained = []
    predictedScores_untrained = []
    actualScores = []

    # Iterate over test data for highest scores
    for index in tqdm(range(amount_of_samples), desc=f"Epoch {epoch} (scores)"):
        # Extract data
        verbalizedGoal = verbalizedGoals[index]
        symbol = symbolNames[index]
        score = normalizedScores[index]
        actualScores.append(score)

        # Calculate trained model residual
        predictedScore = calculatePredictedScore(verbalizedGoal, symbol, tokenizer, trained_model)
        predictedScores_trained.append(predictedScore)
        trainedResidual = predictedScore - score
        trainedResiduals.append(trainedResidual)

        # Calculate untrained model residual
        predictedScore = calculatePredictedScore(verbalizedGoal, symbol, tokenizer, original_model)
        predictedScores_untrained.append(predictedScore)
        untrainedResidual = predictedScore - score
        untrainedResiduals.append(untrainedResidual)

    # Save residuals to separate JSON files for each epoch
    evaluation_data = {
        'trainedResiduals': trainedResiduals,
        'untrainedResiduals': untrainedResiduals,
        'actualScores': actualScores,
        'predictedScores_trained': predictedScores_trained,
        'predictedScores_untrained': predictedScores_untrained,
        'amountOfTestData': amount_of_samples,
    }

    # save the evaluation data for the epoch
    with open(f'evaluation_epoch_{epoch}.json', 'w') as f:
        json.dump(evaluation_data, f)
    
    # Remove the loaded model to free up memory
    del trained_model