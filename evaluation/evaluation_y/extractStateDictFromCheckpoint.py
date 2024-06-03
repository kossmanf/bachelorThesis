import torch
from transformers import AutoModel

epoch = 1

# Construct checkpoint file path
checkpoint_path = f"checkpoint_epoch_{epoch}.pt"

# Load the checkpoint
checkpoint = torch.load(checkpoint_path)

# Load the model
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Load model state dictionary
state_dict = checkpoint['model_state_dict']

# Modify the state dictionary to remove 'embeddings.position_ids' if it's present but not needed
if 'embeddings.position_ids' in state_dict:
    del state_dict['embeddings.position_ids']

model.load_state_dict(state_dict, strict=False)

# Saving the final model
torch.save(model.state_dict(), f'state_dict_{epoch}.pt')
