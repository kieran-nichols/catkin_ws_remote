#Thoughts:
# 1. put calibration protection to make sure calibration step was good




import pandas as pd

import csv

import matplotlib.pyplot as plt
import queue


prev_point = 0
prev_time = 0
# Open the CSV file
plt.figure(figsize=(10, 5))

plt.title("Isolated Step")
with open("sensing_topic.csv", "r") as file:
    # Create a CSV reader
    imu = csv.reader(file)
    
    # Skip the header row
    next(imu)
    
    # I need to divide it into 2 sections, calibrations and then analysis
    callibration_step1 = []
    callibration_step2 = []
    callibration_step3 = []
    callibration = [callibration_step1, callibration_step2, callibration_step3]
    callibration_time1 = []
    callibration_time2 = []
    callibration_time3 = []
    callibration_time = [callibration_time1,callibration_time2,callibration_time3]

    #hold only 2 steps at a time
    pos_peak = []
    neg_peak = []
    total_time = []

    #for testing in time
    peak = []
    TOs = []
    ICs = []
    minipeak = []

    #for graphing
    TOg = []
    ICg = []

    #
    first_zero = False
    second_zero = False
    step = 0

    calibrated = False
    at_max_peak = False
    toes_off = False
    heel_strike = False
    at_mini_peak = False

    # Iterate through each row
    for row in imu:
        # Access individual values by index
        #print(row[9], row[6])
        current_point = float(row[6])*-1
        current_time = float(row[9])
        #current_slope = (current_point-prev_point)/(current_time-prev_time)

        #if neg, wait until 0 and record until the next next 0
        #if pos, wait until 0 then record until the next next 0
        
        callibration[step%2].append(current_point)
        callibration_time[step%2].append(current_time)

        #recording swing and stance
        if ((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point))):
            if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&second_zero):
                second_zero = False
                first_zero = False
                elapsed_time = callibration_time[step%2][-1]-callibration_time[step%2][0]
                #adding new info for peaks
                #if (len(total_time)>2):
                   # pos_peak.get()
                   # neg_peak.get()
                   # total_time.get()
                if (len(callibration[step%2])>0):
                    if (((not calibrated)or((max(callibration[step%2])/(sum(pos_peak)/len(pos_peak))>0.2) & (min(callibration[step%2])/(sum(neg_peak)/len(neg_peak))>0.2) & (elapsed_time/(sum(total_time)/len(total_time))>0.1)))):
                            #good trial so put it's values
                        pos_peak.append(max(callibration[step%2]))
                        neg_peak.append(min(callibration[step%2]))
                        total_time.append(elapsed_time)
                        plt.plot(callibration[step%2], label="Step {}".format(step))
                        calibrated = True
                        step+=1 #done with recording
                callibration[step%2].clear()
                callibration_time[step%2].clear()
                print("cleared")
                continue
            if (((current_point==0.0)|((abs(prev_point)+abs(current_point))>abs(prev_point+current_point)))&first_zero):
                second_zero = True
            first_zero = True
        if (calibrated):
            #peak
            if ((current_point>sum(pos_peak)/len(pos_peak)*0.7)&(not at_max_peak)):
                at_max_peak = True
                toes_off = False
                heel_strike = False
                at_mini_peak = False
                peak.append(current_time)
            elif ((current_point<sum(neg_peak)/len(neg_peak)*0.6)&at_max_peak):
                heel_strike = True
                at_max_peak = False
                ICs.append(current_time)
                ICg.append(current_point)
            elif ((current_point>sum(neg_peak)/len(neg_peak)*0.3)&heel_strike):
                heel_strike = False
                at_mini_peak = True
                minipeak.append(current_time)
            elif ((current_point<sum(neg_peak)/len(neg_peak)*0.6)&at_mini_peak):
                toes_off = True
                at_mini_peak = False
                TOs.append(current_time)
                TOg.append(current_point)
        prev_point = current_point
        prev_time = current_time


        #making decisions


#checking plot      

#plt.savefig('Isolated Calibration step.png')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
print("final answers")

print(pos_peak)
print(sum(pos_peak)/len(pos_peak))
print()
print(neg_peak)
print(sum(neg_peak)/len(neg_peak))
print()
print(total_time)
print(sum(total_time)/len(neg_peak))
print()

print("Analysis")
print("peak")
print(peak)
print("TOs")
print(TOs)
print("ICs")
print(ICs)
print("TOg")
print(TOg)
print("ICg")
print(ICg)
print("minipeak")
print(minipeak)

####################################################################
#Plotting detection
####################################################################
# Read the CSV data into a pandas DataFrame
europa = pd.read_csv("europa_topic.csv")

plt.figure(figsize=(10, 5))

# Read the CSV data into a pandas DataFrame
imu = pd.read_csv("sensing_topic.csv")
#imu = imu[207:507]
# Plot the data
for column in imu.columns[6:7]:
    plt.plot(imu[imu.columns[9]], imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")
    #plt.plot(imu[column]*-1, label="Angular Velocity\n in Z (deg/s)")
plt.scatter(ICs, ICg, label="Detected IC")
plt.scatter(TOs, TOg, label="Detected TO")


# Add labels and legend
plt.xlabel("Time (ms)")
plt.title("Fast Walk")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

#plt.savefig('Angular Velocity in Z vs Fz of Shank 3 steps.png')

# Show the plot
plt.show()
