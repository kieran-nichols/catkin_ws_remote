import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a pandas DataFrame
df = pd.read_csv("linear_moments.csv")

# Plot the data
for column in df.columns[12:15]:
    plt.plot(df[df.columns[0]], df[column], label=column)

# Add labels and legend
plt.xlabel("Time (sec)")
plt.ylabel("Acceleration")
plt.legend()

# Show the plot
plt.show()
plt.savefig('Xsense accel in shank.png')
