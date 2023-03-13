import pandas as pd
#europa = pd.read_csv("europa_topic.csv")
imu = pd.read_csv("sensing_topic.csv")
next(imu)
    
    # Iterate through each row
for row in imu:
    # Access individual values by index
    print(row[6], row[9])