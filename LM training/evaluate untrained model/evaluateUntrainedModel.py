# Importing necessary modules
import json
import torch
from transformers import AutoModel, AutoTokenizer
from torch.nn import CosineSimilarity
from tqdm import tqdm

# Program description
# This program evaluates the untrained model with the testing data.
# It assesses the performance of the untrained model using test data. 
# The program generates an evaluation file containing the calculated residuals (predicted score - actual score), along with the actual and predicted scores.

# device and tokenizer 
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# load the original model
original_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Moving model to the GPU
original_model.to(device)
print(f"Model loaded and moved to {device}")

# set the original model into eval mode
original_model.eval()

# Mean Pooling - Take attention mask into account for correct averaging
# model_output: Tensor containing token embeddings from a language model.
# attention_mask: Tensor that specifies which tokens should be considered and which are padding.
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Function to generate sentence embeddings using a model and tokenizer.
# model: language model used to compute embeddings.
# tokenizer: Tokenizer corresponding to the model to process and encode sentences.
# sentences: List of textual sentences to be converted into embeddings.
# Tokenize sentences
def getEmbeddings(model, tokenizer, sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])

# Function to calculate the predicted score based on cosine similarity between embeddings.
# verbalizedGoal: A string representing the verbalized goal to be embedded.
# symbol: A string representing a symbol to be compared against the goal.
# tokenizer: Tokenizer used to process and encode the strings into tokens.
# model: language model used to compute embeddings.
def calculatePredictedScore(verbalizedGoal, symbol, tokenizer, model):
    goalEmbedding = getEmbeddings(model, tokenizer, [verbalizedGoal])
    symbolEmbedding = getEmbeddings(model, tokenizer, [symbol])
    cos = CosineSimilarity()
    return cos(goalEmbedding, symbolEmbedding).item()

# Load the test data
data = torch.load('testData.pt')
symbolNames = data['symbolNames']
verbalizedGoals = data['verbalizedGoals']
normalizedScores = data['normalizedScores']

# load the amount of samples
amount_of_samples = len(verbalizedGoals)

# lists for the the actual values, the predicted scores and the residuals
untrainedResiduals = []
predictedScores_untrained = []
actualScores = []

# Itterating over the testing data
for index in tqdm(range(amount_of_samples), desc="Evaluating model"):
    # Extract data
    verbalizedGoal = verbalizedGoals[index]
    symbol = symbolNames[index]
    score = normalizedScores[index]
    actualScores.append(score)

    # Calculate untrained model residual
    predictedScore = calculatePredictedScore(verbalizedGoal, symbol, tokenizer, original_model)
    predictedScores_untrained.append(predictedScore)
    untrainedResidual = predictedScore - score
    untrainedResiduals.append(untrainedResidual)


# Save results
evaluation_data = {
    'untrainedResiduals': untrainedResiduals,
    'actualScores': actualScores,
    'predictedScores_untrained': predictedScores_untrained,
    'amountOfTestData': amount_of_samples,
}

with open('evaluation_original_model.json', 'w') as f:
    json.dump(evaluation_data, f)
