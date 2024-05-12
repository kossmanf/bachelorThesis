import json
import matplotlib.pyplot as plt

# Load evaluation data from a JSON file corresponding to the 0 epoch
with open(f'evaluation_original_model.json', 'r') as file:
    # Load evaluation data from a JSON file corresponding to the current epoch
    json_data = json.load(file)
    predicted_values = json_data['predictedScores_untrained']
    actual_values = json_data['actualScores']

# Function to plot bisecting line and datasets
def plot_data(x_data, y_data):
    # Create a figure and an axes.
    fig, ax = plt.subplots()

    # Calculating the minimum and maximum limits based on the data for a well-fit line.
    min_limit = min(min(x_data), min(y_data))
    max_limit = max(max(x_data), max(y_data))

    # Plotting the bisecting line
    ax.plot([min_limit, max_limit], [min_limit, max_limit], 'black',  alpha=1, linestyle='--', label='Bisecting line')  # Gray dashed bisecting line

    pointSize = 1

    # Plotting the data points with lighter color
    ax.scatter(x_data, y_data, color='gray', alpha=1, label='Data points', s=pointSize)  # Lighter black data points

    # Adding labels and title
    ax.set_xlabel('Actual Value', color='black')
    ax.set_ylabel('Predicted Value', color='black')
    ax.set_title('Plot of Bisecting Line and Data Points', color='black')
    ax.legend()

    # Show the plot
    plt.show()


# Example datasets
x_dataset = actual_values
y_dataset = predicted_values

# Call the function with the datasets
plot_data(x_dataset, y_dataset)
