import torch
import matplotlib.pyplot as plt

# loading the dataset either test or training data
data = torch.load('trainingData.pt')  # Load data from file
actual_values = data['normalizedScores']  # Extract normalized scores

# Function to group data into chunks and calculate average
def group(list, groupSize):
    averages = []
    for i in range(0, len(list), groupSize):
        group = list[i:i+groupSize]
        groupAverage = sum(group) / len(group)
        averages.append(groupAverage)
    return averages

pointSize = 1  # Set point size for plotting

# Plot actual values in gray
plt.plot(group(actual_values, 10), 'o', color='gray', label='Actual Values', markersize=pointSize)

# Add labels and title
plt.xlabel('Data Point')  # Label for x-axis
plt.ylabel('Value')       # Label for y-axis
plt.title('Actual Values')  # Title of the plot

# Add legend
plt.legend()  # Show legend

# Show plot
plt.grid(True)  # Add grid
plt.show()      # Display the plot