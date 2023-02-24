import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a pandas DataFrame
europa = pd.read_csv("europa_topic.csv")
#print(len(europa))
#europa = europa[143:652]
plt.figure(figsize=(10, 5))
# Plot the data
for column in europa.columns[3:4]:
    plt.plot(europa[column], label="Pylon Force (N)")
    #plt.plot(europa[column], label="Pylon Force (N)")

# Read the CSV data into a panda
# s DataFrame
imu = pd.read_csv("sensing_topic.csv")
#imu = imu[162:654]
# Plot the data
for column in imu.columns[6:7]:
    plt.plot( imu[column]*-10, label="10x Angular Velocity\n in Z (deg/s)")
    #plt.plot(imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")
#for column in imu.columns[1:2]:
    #plt.plot(imu[column]*98, label="10x Acceleration pointing up\n in X (deg/s)")
    #plt.plot(imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")


# Add labels and legend
#plt.xlabel("Time (ms)")
plt.title("Slow Walk")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

#plt.savefig('Angular Velocity in Z vs Fz of Shank 3 steps.png')

# Show the plot
plt.show()
