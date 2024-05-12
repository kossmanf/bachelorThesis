from transformers import AutoTokenizer, AutoModel
import torch

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Load the model
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Save the fully loaded model to disk
torch.save(model.state_dict(), "original_model.pt")