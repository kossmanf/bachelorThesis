import json
import matplotlib.pyplot as plt
import numpy as np

# Reading JSON data
with open('extractedInformation.json', 'r') as file:
    data = json.load(file)

xAxisData = []
yAxisData = []

ctr1 = 0
ctr2 = 0

for proofInformationDict1 in data['proofsNormal']:
    if proofInformationDict1['proofFound'] == 't' and proofInformationDict1['Processed clauses'] != '': 
        for proofInformationDict2 in data['proofs']:
            if proofInformationDict1['proofName'] == proofInformationDict2['proofName'] and proofInformationDict2['Processed clauses'] != '':
                p1 = int(proofInformationDict1['Processed clauses'])
                p2 = int(proofInformationDict2['Processed clauses'])
                xAxisData.append(p1)
                yAxisData.append(p2)

                if p1 < p2:
                    ctr1 = ctr1 + 1
                else:
                    ctr2 = ctr2 + 1

percentage1 = (ctr1/(ctr1 + ctr2)) *  100
percentage2 = (ctr2/(ctr1 + ctr2)) *  100

print(percentage1)
print(percentage2)




# Function to plot bisecting line and datasets
def plot_data(x_data, y_data):

    '''
    num_std = 3

    for i in range(0, len(x_data)-1):
        print(x_data)
        x_mean = np.mean(x_data)
        x_std = np.std(x_data)
        y_mean = np.mean(y_data)
        y_std = np.std(y_data)

        # Ausreißer identifizieren
        x_outlier = (np.abs(x_data[i] - x_mean) > num_std * x_std)
        y_outlier = (np.abs(y_data[i] - y_mean) > num_std * y_std)

        if x_outlier or y_outlier:
            print('yeah')
            del xAxisData[i]
            del yAxisData[i]
    '''

    # Create a figure and an axes.
    fig, ax = plt.subplots()

    # Calculating the minimum and maximum limits based on the data for a well-fit line.
    min_limit = min(min(x_data), min(y_data))
    max_limit = max(max(x_data), max(y_data))

    # Plotting the bisecting line
    ax.plot([min_limit, max_limit], [min_limit, max_limit], 'r--', label='Bisecting line')  # Red dashed bisecting line

    pointSize = 1.5

    # Plotting the data points
    ax.scatter(x_data, y_data, color='blue', label='Data points',  s=pointSize)  

    # Adding labels and title
    ax.set_xlabel('Processed without LM')
    ax.set_ylabel('Processed with LM')
    ax.set_title('Plot of Bisecting Line and Data Points')
    ax.legend()

    # Setting tick labels on x and y axis every 1000 units
    ax.set_xticks(range(int(min_limit), int(max_limit) + 1, 10000))
    ax.set_yticks(range(int(min_limit), int(max_limit) + 1, 10000))

    # Adjust axes to include a little extra space
    #ax.set_xlim(min_limit - 1, max_limit + 1)
    #ax.set_ylim(min_limit - 1, max_limit + 1)

    # Show the plot
    plt.show()


# Example datasets
x_dataset = xAxisData
y_dataset = yAxisData

# Call the function with the datasets
plot_data(x_dataset, y_dataset)
