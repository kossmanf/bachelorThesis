import torch
import json
import os
import math
from torch.utils.data import Dataset, DataLoader
from torch.nn.functional import cosine_similarity, normalize
from torch.nn import MSELoss
from torch.nn import CosineEmbeddingLoss
import torch.optim as optim
from transformers import AutoModel, AutoTokenizer
from torch.nn import CosineSimilarity
import numpy as np
from tqdm import tqdm  

# function to load dataset
class CustomDataset(Dataset):
    def __init__(self, data_file): 
        # loading the data
        data = torch.load(data_file)

        # creating the attributes for the data
        self.verbalizedGoals = data['verbalizedGoals']
        self.symbolNames = data['symbolNames']
        self.normalizedScores = data['normalizedScores']
        self.length = len(self.verbalizedGoals)

    # returning the feature and label at a specific index
    def __getitem__(self, index):
        verbalizedGoal = self.verbalizedGoals[index]
        symbolName = self.symbolNames[index]
        label = self.normalizedScores[index]
        return verbalizedGoal, symbolName, label

    # returning the sample size
    def __len__(self):
        return self.length

# function to create dataloader
def create_dataloader(data_file, batch_size):
    dataset = CustomDataset(data_file)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)

# function to create model and optimizer
def create_model_and_optimizer():
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    optimizer = optim.AdamW(model.parameters(), lr=5e-5)
    return model, optimizer

# function to calculate mean pooling from huggingface
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0].to(attention_mask.device)
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# Inside the train_model() function
def train_model(model, optimizer, dataloader, criterion, device, epochs, start_epoch=0, start_loss=0.0, lossPoints=[]):

    # set the model into training mode
    model.train()

    # training loop
    for epoch in range(start_epoch, epochs):
        total_loss = start_loss

        for ctr, batch in enumerate(tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}", leave=False)):
            # extracting the goals, symbols and labels
            verbalizedGoals, symbolNames, labels = batch

            # zeroing the gradients
            optimizer.zero_grad()

            # tokenize the goals and the symbols
            tokenizedGoals = tokenizer([goal for goal in verbalizedGoals], padding=True, truncation=True, return_tensors='pt')
            tokenizedSymbols = tokenizer([symbol for symbol in symbolNames], padding=True, truncation=True, return_tensors='pt')

            # Move labels to the device
            labels = torch.tensor([label.float() for label in labels], device=device)

            # Move tokenized goals and symbols to the device
            tokenizedGoals = {key: value.to(device) for key, value in tokenizedGoals.items()}
            tokenizedSymbols = {key: value.to(device) for key, value in tokenizedSymbols.items()}

            # forward path of the goals and symbols
            goalsOutput = model(**tokenizedGoals)
            symbolsOutput = model(**tokenizedSymbols)

            # generating the embeddings for the goals and the symbols
            goalEmbeddings = mean_pooling(goalsOutput, tokenizedGoals['attention_mask'])
            symbolEmbeddings = mean_pooling(symbolsOutput, tokenizedSymbols['attention_mask'])

            # calculating the cosine similarity between the goals and the symbols
            cos = CosineSimilarity(dim=1)
            cosSim = cos(goalEmbeddings, symbolEmbeddings)

            # calculating the loss
            loss = criterion(cosSim, labels)

            # do backpropagation 
            loss.backward()

            # optimize the weights
            optimizer.step()

            # add the loss to the total loss
            total_loss += loss.item()

            # # create a checkpoint
            # if (ctr + 1) % backup_freq == 0:

        save_file_name = f"checkpoint_epoch_{epoch}.pt"
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': total_loss,
            'lossPoints': lossPoints
        }, save_file_name)
        
        # append the total loss to the total loss function
        lossPoints.append(total_loss)

if __name__ == "__main__":

    # training parameters
    data_file = './trainingData.pt'
    batch_size = 8
    epochs = 5

    # device and tokenizer 
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    dataloader = create_dataloader(data_file, batch_size)

    # creating the model and the optimizer
    model, optimizer = create_model_and_optimizer()

    # Moving model and optimizer to the GPU
    model.to(device)
    print(f"model moved to {device}")
    optimizer_state_dict = optimizer.state_dict()
    for state in optimizer_state_dict['state'].values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.to(device)

    # specifying the criterion
    criterion = MSELoss()

    # Check if there's a backed-up model and load it
    # checkpoint_file = 'checkpoint.pt'
    start_epoch = 0
    start_loss = 0.0
    lossPoints = []

    # check if a checkpoint exists
    # if os.path.exists(checkpoint_file):
    #     checkpoint = torch.load(checkpoint_file)
    #     model.load_state_dict(checkpoint['model_state_dict'])
    #     optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    #     start_epoch = checkpoint['epoch']
    #     lossPoints = checkpoint['lossPoints']

    # training the model
    train_model(model, optimizer, dataloader, criterion, device, epochs, start_epoch, start_loss, lossPoints)

    # Saving the final model
    torch.save(model.state_dict(), 'final_model.pt')

    # Saving the final loss function 
    with open('lossFunctionPoints.json', 'w') as file:
        json.dump({'lossPoints': lossPoints}, file, indent=4)

# check the file 
# 