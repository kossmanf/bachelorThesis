import json
import torch
from transformers import AutoModel, AutoTokenizer
from torch.nn import CosineSimilarity
from tqdm import tqdm

# device and tokenizer 
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# load the original model
original_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
original_model.to(device)
original_model.eval()
print(f"Model loaded and moved to {device}")

# Define the mean pooling function
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Define function to calculate embeddings
def getEmbeddings(model, tokenizer, sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])

# Define function to calculate predicted score
def calculatePredictedScore(verbalizedGoal, symbol, tokenizer, model):
    goalEmbedding = getEmbeddings(model, tokenizer, [verbalizedGoal])
    symbolEmbedding = getEmbeddings(model, tokenizer, [symbol])
    cos = CosineSimilarity()
    return cos(goalEmbedding, symbolEmbedding).item()

# Load the test data
data = torch.load('testData_random_10pos_10neg.pt')
symbolNames = data['symbolNames']
verbalizedGoals = data['verbalizedGoals']
normalizedScores = data['normalizedScores']

# load the amount of samples
amount_of_samples = len(verbalizedGoals)

untrainedResiduals = []
predictedScores_untrained = []
actualScores = []

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
