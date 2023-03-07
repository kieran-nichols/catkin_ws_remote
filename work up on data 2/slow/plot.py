import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a pandas DataFrame
europa = pd.read_csv("europa_topic.csv")
#print(len(europa))
#europa = europa[143:652]
plt.figure(figsize=(13, 5))
plt.rcParams.update({'font.size': 20})
# Plot the data
for column in europa.columns[3:4]:
    plt.plot(europa[europa.columns[5]], europa[column]/10, label="Pylon Force\n(N)\n", linewidth=3.0, zorder=-1)
    #plt.plot(europa[column], label="Pylon Force (N)")

# Read the CSV data into a panda
# s DataFrame
imu = pd.read_csv("sensing_topic.csv")
#imu = imu[162:654]
# Plot the data
#for column in imu.columns[6:7]:
    #plt.plot( imu[imu.columns[9]], imu[column]*-10, label="10x Angular\n Velocity\nin Z\n(deg/s)\n", linewidth=3.0, zorder=-1)
    #plt.plot(imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")
for column in imu.columns[1:2]:
    #plt.plot(imu[column]*98, label="10x Acceleration pointing up\n in X (deg/s)")
    #plt.plot(imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")
    plt.plot(imu[imu.columns[9]], imu[column]*9.8, label="Acceleration\n Downwards")

#plotting IC in samples
#IC = [-203,-204, -209, -211, -213]
#ICs = [177.4,280,395.8,499.3, 607 ]

#TOs = [248.4, 350.4, 464.5, 570.3]
#TO = [-168,-181, -174, -179]
#plt.scatter( TOs, TO, label="TO\n", color='red', linewidth=7.0, zorder=1)
#plt.scatter( ICs, IC, label="IC\n", color='light', linewidth=7.0, zorder=1)


# Add labels and legend
plt.xlabel("Time (s)")
plt.title("Slow Walk")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

#plt.savefig('Angular Velocity in Z vs Fz of Shank 3 steps.png')

# Show the plot
plt.show()
