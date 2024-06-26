# Importing necessary modules
import json
import matplotlib.pyplot as plt
import numpy as np

# Program description
# This script plots the residuals of processed clauses using Eprover, comparing results with and without the integration of a language model.

# Reading JSON data
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

# xData are the processed clauses without the integration of the languge mdoel and yData the processed clauses with the use of the language model
xAxisData = []
yAxisData = []

# Iterating over all the extrcted information finding the number of processed clauses of proofs which have been found with and without the use of the language model
for proofInformationDict1 in data['proofsNormal']:
    if proofInformationDict1['proofFound'] == 't' and proofInformationDict1['Processed clauses'] != '': 
        for proofInformationDict2 in data['proofs']:
            if proofInformationDict1['proofName'] == proofInformationDict2['proofName'] and proofInformationDict2['Processed clauses'] != '':
                p1 = int(proofInformationDict1['Processed clauses'])
                p2 = int(proofInformationDict2['Processed clauses'])
                xAxisData.append(p1)
                yAxisData.append(p2)

# Function to plot bisecting line and datasets
def plot_data(dataset):

    # Plotting the residuals as a bar chart
    plt.figure(figsize=(10, 6))  # Setting the figure size
    plt.bar(range(len(residuals)), residuals, color='gray')  # Creating a bar chart
    plt.xlabel('Index')  # Label for the x-axis
    plt.ylabel('Residuals (Processed Clauses Difference)')  # Label for the y-axis
    plt.title('Residuals of Processed Clauses')  # Title of the chart
    plt.axhline(0, color='black', linestyle='--')  # Adding a horizontal line at zero for reference
    plt.show()  # Display the plot

    # Show the plot
    plt.show()


# Calculate residuals
residuals = np.array(yAxisData) - np.array(xAxisData)

# Call the function with the datasets
plot_data(residuals)
