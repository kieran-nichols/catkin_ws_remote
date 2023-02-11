import subprocess
import os
import pandas as pd
import os
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from plotly.colors import sequential
from scipy.signal import find_peaks
import time

# find all files with '.bag' in name
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\for_bags"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
#print(files, "\nlist_length= ", len(files))
all_real_time = []
all_moment = []
all_peaks = []
colors = ['red', 'blue', 'green']
TADA_angles = ['0, 180', '10, 0', '10, 180', '10, 90', '10, n90']
figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
color_dict = dict(zip(['slow', 'med', 'fast'], colors))

condition_dict = dict(zip(['slow', 'med', 'fast'], colors))
TADA_angle_dict = dict(zip(TADA_angles, ['Neutral', 'PF', 'DF', 'EV', 'IV']))
#print(color_dict)
#print(TADA_angle_dict)

# loop through each file
#for file in files:
#    # Execute the command and retrieve the output
#    subprocess.run('rostopic echo -b {} -p /europa_topic > data_kn/europa_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
    
for i, file in enumerate(files): 
    if i>= 15: break
    #print(file)
    description = file.split('_')
    #print(description)
    condition_from_file = f'{description[1]}, {description[2]}'
    # check if the condition is in the dictionary then pick the match
    condition = TADA_angle_dict[condition_from_file]
    last_item = description[3].split('.')
    speed = last_item[0]
    #print(condition, speed)
    
    #figure.data = []
    
    # Execute the command and retrieve the output
    #subprocess.run('rostopic echo -b {} -p /europa_topic > data_kn/europa_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
    # read the data from the file
    data = pd.read_csv('data_kn/europa_topic_{}.csv'.format(file))
    data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    #print(data.field_moment)
    #time = data.time
    real_time = (data.time - data.time[0])/1_000_000_000
    #print(time)
    moment = data.field_my
    all_real_time.append(real_time)
    all_moment.append(moment)

    ### plot the data
    ##fig = px.line(x=time, y=moment)
    ##fig.update_layout(title_text=file)
    ##fig.show()

    ## find the peak
    all_peaks, _ = find_peaks(moment, height=300, distance=50)
    # pick the middle three peaks
    peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
    #all_peaks.append((peaks))
    #print(len(peaks))
    
    #print(f"Peak for {file}: {peak_time}s, {peak_moment}")

    figure.add_trace(go.Scatter(x=real_time, y=moment, mode='lines'))
    figure.add_trace(go.Scatter(x=real_time[peaks], y=moment[peaks], mode='markers'))
    
    #print(color_dict[speed])
    condition_list = [condition]*len(peaks)
    speed_list = [speed]*len(peaks)
    #print(condition_list, speed_list)
    figure1.add_trace(go.Scatter(x=condition_list, y=moment[peaks], mode='markers', name=speed, marker_color=color_dict[speed]))
    
    peak_avg = np.mean(moment[peaks])
    figure1.add_trace(go.Scatter(x=[condition], y=[peak_avg], mode='markers', name=speed, marker=dict(color=color_dict[speed], size=20, symbol = 'square')))
    #break
    #figure.show()
    #figure1.show()
    #time.sleep(2)
    
    
### add markers for each peak
#for (peak_time, peak_value) in all_peaks:
#    figure.add_trace(
#        go.Scatter(mode='markers', x=[peak_time], y=[peak_value], line=dict(color='red', width=100))
#    )
#print(all_peaks)

#fig.update_layout(title_text="All Files with Peaks")
#figure.show()
figure1.show()

## find the middle three peaks
## (assuming there are more than three files)
#middle_peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
#print(f"Middle three peaks: {middle_peaks}")


