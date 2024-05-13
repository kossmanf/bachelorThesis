import json
import numpy as np
import random
from tqdm import tqdm

# This function performs bootstrapping on given data to generate statistical estimates.
def bootstrapping(data, num_samples, func):
    bootstrapedValues = []
    n = len(data)  # The size of the dataset

    # Generate bootstrap samples and compute the desired statistic
    for _ in tqdm(range(num_samples), desc="Bootstrapping samples"):
        # Randomly sample with replacement from the original data
        bootstrap_sample = [random.choice(data) for _ in range(n)]
        
        # Apply the statistical function to the sample
        value = func(bootstrap_sample)
        
        # Store the calculated value
        bootstrapedValues.append(value)
    
    return bootstrapedValues

# Lists to store aggregated bootstrapped values for positive and negative residuals
meanErrors = []
meanAbsoluteErrors = []
standardDevAbsoluteErrors = []

# Statistical functions defined using lambda expressions
me =  lambda data: np.mean(data)  # Mean of the data
mae =  lambda data: np.mean(np.abs(data))  # Mean absolute error
aeStd = lambda data: np.std(np.abs(data), ddof=1)  # Standard deviation of the absolute errors

    # Load evaluation data from a JSON file corresponding to the 0 epoch
with open(f'evaluation_epoch_{0}.json', 'r') as file:
    # Load evaluation data from a JSON file corresponding to the current epoch
    json_data = json.load(file)
    untrainedResiduals = json_data['untrainedResiduals']

# Calculate and store bootstrapped statistics for positive residuals
me_val = bootstrapping(untrainedResiduals, 50, me)
meanErrors.append(np.mean(me_val))
mae_val = bootstrapping(untrainedResiduals, 50, mae)
meanAbsoluteErrors.append(np.mean(mae_val))
aeStd_val = bootstrapping(untrainedResiduals, 50, aeStd)
standardDevAbsoluteErrors.append(np.mean(aeStd_val))


# Process multiple evaluation files, one for each epoch, with progress displayed
for epoch in tqdm(range(0, 5), desc="Processing evaluation files"):
    # Load evaluation data from a JSON file corresponding to the current epoch
    with open(f'evaluation_epoch_{epoch}.json', 'r') as file:
        json_data = json.load(file)
        trainedResiduals = json_data['trainedResiduals']

    # Calculate and store bootstrapped statistics for positive residuals
    me_val = bootstrapping(trainedResiduals, 50, me)
    meanErrors.append(np.mean(me_val))
    mae_val = bootstrapping(trainedResiduals, 50, mae)
    meanAbsoluteErrors.append(np.mean(mae_val))
    aeStd_val = bootstrapping(trainedResiduals, 50, aeStd)
    standardDevAbsoluteErrors.append(np.mean(aeStd_val))

# Construct dictionary with all bootstrapped values
bootstrapped_data = {
    "meanErrors": meanErrors,
    "meanAbsoluteErrors": meanAbsoluteErrors,
    "standardDevAbsoluteErrors": standardDevAbsoluteErrors,
}

# Save the results to a JSON file
with open("bootstrapped_data.json", "w") as outfile:
    json.dump(bootstrapped_data, outfile)