# Importing necessary modules
import json
import matplotlib.pyplot as plt
import numpy as np

# Program description
# This script plots the number of processed clauses using Eprover, comparing results with and without the integration of a language model.

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
def plot_data(x_data, y_data):

    # Create a figure and an axes.
    fig, ax = plt.subplots()

    # Calculating the minimum and maximum limits based on the data for a well-fit line.
    min_limit = min(min(x_data), min(y_data))
    max_limit = max(max(x_data), max(y_data))

    # Plotting the bisecting line
    ax.plot([min_limit, max_limit], [min_limit, max_limit], 'r--', label='Bisecting line', color='black')  # Red dashed bisecting line
    
    # size of the datapoints
    pointSize = 1.5

    # Plotting the data points
    ax.scatter(x_data, y_data, color='gray', label='Data points',  s=pointSize)  

    # Adding labels and title
    ax.set_xlabel('Processed without LM')
    ax.set_ylabel('Processed with LM')
    ax.set_title('Plot of Bisecting Line and Data Points')

    # Setting tick labels on x and y axis every 1000 units
    ax.set_xticks(range(int(min_limit), int(max_limit) + 1, 10000))
    ax.set_yticks(range(int(min_limit), int(max_limit) + 1, 10000))

    # Show the plot
    plt.show()


# Example datasets
x_dataset = xAxisData
y_dataset = yAxisData

# Call the function with the datasets
plot_data(x_dataset, y_dataset)
