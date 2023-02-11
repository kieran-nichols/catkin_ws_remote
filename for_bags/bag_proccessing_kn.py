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
from plotly.subplots import make_subplots
import types

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
figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)        
color_dict = dict(zip(['slow', 'med', 'fast'], colors))
moments = {'mx':[], 'my':[]}
#print(moments)
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
    
    # Execute the command and retrieve the output
    #subprocess.run('rostopic echo -b {} -p /europa_topic > data_kn/europa_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
    # read the data from the file
    data = pd.read_csv('data_kn/europa_topic_{}.csv'.format(file))
    data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    #print(data.field_moment)
    #time = data.time
    real_time = (data.time - data.time[0])/1_000_000_000
    #print(time)
    moments['mx'] = data.field_mx
    moments['my'] = data.field_my
    all_real_time.append(real_time)
    peak_avg_array = []
    condition_array = []
    #all_moment.append(moment)

    ### plot the data
    ##fig = px.line(x=time, y=moment)
    ##fig.update_layout(title_text=file)
    ##fig.show()
    #print(moments.values())
    for j,moment in enumerate(moments.values()):
        #print(i,j)
        ## find the peak
        #print(moment)
        all_peaks, _ = find_peaks(moment, height=300, distance=50)
        # pick the middle three peaks
        peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
        #all_peaks.append((peaks))
        #print(len(peaks))
    
        #figure.data = []
        figure.add_trace(go.Scatter(x=real_time, y=moment, mode='lines'))
        figure.add_trace(go.Scatter(x=real_time[peaks], y=moment[peaks], mode='markers'))
    
        #print(color_dict[speed])
        condition_list = [condition]*len(peaks)
        speed_list = [speed]*len(peaks)
        #print(condition_list, speed_list)
        #figure1.add_trace(go.Scatter(x=condition_list, y=moment[peaks], mode='markers', name=speed, marker_color=color_dict[speed]))
        figure2.add_trace(go.Scatter(x=condition_list, y=moment[peaks], mode='markers', name=speed, marker_color=color_dict[speed]),j+1,1)
    
        peak_avg = np.mean(moment[peaks])
        #peak_avg_array.append(peak_avg)
        #condition_array.append(condition)
        
        trace = go.Scatter(x=[condition], y=[peak_avg], mode='markers', name=speed, marker=dict(color=color_dict[speed], size=10, symbol = 'diamond'))
        #figure1.add_trace(trace)
        figure2.add_trace(trace,j+1,1)
        #break
        #figure.show()
        #figure1.show()
        #time.sleep(2)

#fig.update_layout(title_text="All Files with Peaks")
#figure.show()
#figure.add_trace(go.Scatter(x=condition_array, y=peak_avg_array, mode='lines', name='peak_avg_array'))
#figure.add_trace(go.Scatter(x=condition_array, y=peak_avg_array, mode='markers', name='peak_avg_array'))
figure2.update_layout(title_text="Average Moment Peaks for a given speed")
figure2.update_layout(xaxis1_title="TADA angle (anatomical angle)", yaxis_title="Frontal Moment (N*m)")
figure2.update_layout(xaxis2_title="TADA angle (anatomical angle)", yaxis2_title="Sagittal Moment (N*m)")
figure2.update_layout(legend_title="Speed (m/s)")
#figure.update_layout(legend=dict(x='slow', y='medium',z='fast'))
#figure1.show()
figure2.show()




