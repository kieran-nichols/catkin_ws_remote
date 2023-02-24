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
    fcallibration_step1 = []
    fcallibration_step2 = []
    fcallibration_step3 = []
    fcallibration = [fcallibration_step1, fcallibration_step2, fcallibration_step3]
    fcallibration_time1 = []
    fcallibration_time2 = []
    fcallibration_time3 = []
    fcallibration_time = [fcallibration_time1,fcallibration_time2,fcallibration_time3]
    scallibration_step1 = []
    scallibration_step2 = []
    scallibration_step3 = []
    scallibration = [scallibration_step1, scallibration_step2, scallibration_step3]
    scallibration_time1 = []
    scallibration_time2 = []
    scallibration_time3 = []
    scallibration_time = [scallibration_time1,scallibration_time2,scallibration_time3]

    #hold only 2 steps at a time
    pos_peak = []
    neg_peak = []
    total_time = []


    #
    first_zero = False
    second_zero = False
    step = 0
    calibrated = False
    
    # Iterate through each row
    for row in imu:
        # Access individual values by index
        print(row[9], row[6])
        current_point = float(row[6])*-1
        current_time = float(row[9])
        #current_slope = (current_point-prev_point)/(current_time-prev_time)

        #if neg, wait until 0 and record until the next next 0
        #if pos, wait until 0 then record until the next next 0
        if second_zero:#for the first positive part
            fcallibration[step%2].append(current_point)
            fcallibration_time[step%2].append(current_time)
        else:#for the second negative part
            scallibration[step%2].append(current_point)
            scallibration_time[step%2].append(current_time)
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
                    if (((not calibrated)or((max(callibration[step%2])/(sum(pos_peak)/len(pos_peak))>0.8) & (min(callibration[step%2])/(sum(neg_peak)/len(neg_peak))>0.8) & (elapsed_time/(sum(total_time)/len(total_time))>0.3)))):
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
print(sum(total_time)/len(total_time))
print()


