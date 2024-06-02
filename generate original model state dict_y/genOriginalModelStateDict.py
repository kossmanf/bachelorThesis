# Modules to be imported
from transformers import AutoModel
import torch

# program description
# This script loads the original model from Hugging Face and stores its parameters in a state dictionary.
# The original model is utilized to assess whether training has enhanced the performance of the language model.

# Load the model
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Save the fully loaded model to disk
torch.save(model.state_dict(), "original_model.pt")