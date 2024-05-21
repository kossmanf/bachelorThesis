# Modules to be imported
import json
import matplotlib.pyplot as plt

# Program description
#  This program takes the mean error the mean absolute error and the standard deviation of the absolute error over the trained epochs and plots them in a line chart

# Load the bootstrapped data from JSON file
with open("bootstrapped_data.json", "r") as infile:
    bootstrapped_data = json.load(infile)

# Extract data for all statistics
mean_errors = bootstrapped_data["meanErrors"]
mean_absolute_errors = bootstrapped_data["meanAbsoluteErrors"]
std_dev_absolute_errors = bootstrapped_data["standardDevAbsoluteErrors"]

# Generate epochs range for x-axis
epochs = range(len(mean_errors))  # This assumes all lists are the same length

# Create a figure and a set of subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# Define plot styling to be black
color = 'black'
marker_style = 'o'
line_style = '-'

# Plot Mean Errors
axs[0].plot(epochs, mean_errors, color=color, linestyle=line_style, marker=marker_style, label="Residuals Mean Error")
axs[0].set_title("Mean Errors", y=1.05, color=color)
axs[0].set_xlabel("Epochs", color=color)
axs[0].set_ylabel("Mean Error", color=color)
axs[0].legend()
axs[0].grid(True, color=color)

# Plot Mean Absolute Errors
axs[1].plot(epochs, mean_absolute_errors, color=color, linestyle=line_style, marker=marker_style, label="Residuals MAE")
axs[1].set_title("Mean Absolute Errors", y=1.05, color=color)
axs[1].set_xlabel("Epochs", color=color)
axs[1].set_ylabel("Mean Absolute Error", color=color)
axs[1].legend()
axs[1].grid(True, color=color)

# Plot Standard Deviation of Absolute Errors
axs[2].plot(epochs, std_dev_absolute_errors, color=color, linestyle=line_style, marker=marker_style, label="Residuals Std Dev of Abs Errors")
axs[2].set_title("Standard Deviation of Absolute Errors", y=1.05, color=color)
axs[2].set_xlabel("Epochs", color=color)
axs[2].set_ylabel("Standard Deviation", color=color)
axs[2].legend()
axs[2].grid(True, color=color)

# Adjust layout and display the plot
plt.subplots_adjust(hspace=0.5)
plt.show()
