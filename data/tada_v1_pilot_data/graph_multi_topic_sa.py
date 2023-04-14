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
import pickle

# find all files with '.bag' in name
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_v1_pilot_data"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
topics = ['angular_moments','europa_topic', 'linear_moments', 'motor_command', 'sensing_topic', 'xsens_joint_angle', 'xsens_com']
colors = ['red', 'blue', 'green']

figure = go.Figure()
figure1 = go.Figure()
figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

color_dict = dict(zip(['slow', 'med', 'fast'], colors))
moments = {'mx':[], 'my':[], 'fz':[]}
imu_data = {'gyro_z':[], 'state':[]}
linear_moments = {'foot_vert_vel':[]}
motor_command = {'m1_cmd':[], 'm2_cmd':[], 'PF_cmd':[], 'EV_cmd':[], 'CPU0':[], 'CPU1':[], 'CPU2':[], 'CPU3':[]}
xsens_joint_angle = {'hip_sag':[], 'knee_sag':[], 'ankle_sag':[]}
xsens_com = {'com_pos_x':[], 'com_pos_y':[], 'com_pos_z':[]}

step = 1

# convert the rosbag to csv files that are based on topics
if step==0:
    # loop through each topic
    for topic in topics:
    #    # Execute the command and retrieve the output
        subprocess.run('rostopic echo -b {} -p /{} > {}.csv'.format(files[0],topic,topic), capture_output=True, text=True, shell=True)
   
# read all csv files, store them in dictionaries, find the regions of time where TADA angle is non-neutral, and plot the topics for each TADA angle
elif step==1: 
        ########################################
        #topics = [moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments]
        # Read europa data
        data = pd.read_csv(path + '\europa_topic.csv')
        data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        #print(data)
        time = data.field_t - data.field_t[0]
        #print(data.field_t[0])
        moments['mx'] = data.field_mx
        moments['my'] = data.field_my
        moments['fz'] = data.field_fz
    
        # read imu data
        data1 = pd.read_csv(path + '\sensing_topic.csv')
        data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time1 = data1.field_t - data.field_t[0]
        #print(data1)
        imu_data['gyro_z'] = data1.field_gyro_z
        imu_data['state'] = data1.field_state
        
        # Read motor cmd data from csv
        data2 = pd.read_csv(path + '\motor_cmd1.csv')
        data2.columns = data2.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time2 = data2.field_t - data.field_t[0]
        motor_command['m1_cmd'] = data2.field_motor1_move/567*360
        motor_command['m2_cmd'] = data2.field_motor2_move/567*360
        motor_command['PF_cmd'], motor_command['EV_cmd'] = data2.field_PF_cmd, data2.field_EV_cmd
        #print(motor_command['PF_cmd'])
        motor_command['CPU0'], motor_command['CPU1'], motor_command['CPU2'], motor_command['CPU3'] = data2.field_CPU0, data2.field_CPU1, data2.field_CPU2, data2.field_CPU3  
        
        ## Read xsens joint angle data from csv # taking the time offset from windows data since the offset is different to linux topics
        data3 = pd.read_csv(path + r'\xsens_joint_angle.csv')
        data3.columns = data3.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time3 = data3.field_data0 - data3.field_data0[0]# - data.field_t[0]
        #print(data3.field_data0[0])
        xsens_joint_angle['hip_frontal_right'] = data3.field_data3
        xsens_joint_angle['knee_frontal_right'] = data3.field_data8
        xsens_joint_angle['ankle_frontal_right'] = data3.field_data13
        xsens_joint_angle['hip_sag_right'] = data3.field_data4
        xsens_joint_angle['knee_sag_right'] = data3.field_data9
        xsens_joint_angle['ankle_sag_right'] = data3.field_data14
        
        ## Read xsens com data from csv # taking the time offset from windows data since the offset is different to linux topics
        data4 = pd.read_csv(path + r'\xsens_com.csv')
        data4.columns = data4.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time4 = data4.field_data0 - data3.field_data0[0]
        xsens_com['com_pos_x'] = data4.field_data1
        xsens_com['com_pos_y'] = data4.field_data2
        xsens_com['com_pos_z'] = data4.field_data3
        
        ## Read linear moments data from csv # taking the time offset from windows data since the offset is different to linux topics
        data5 = pd.read_csv(path + r'\linear_moments.csv')
        data5.columns = data5.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time5 = data5.field_data0 - data3.field_data0[0]
        linear_moments['foot_vert_vel'] = data5.field_data16        
        
        ########################################
        # TADA_angle finder (10 steps); in this dataset, the TADA angle changes, the persons walks about 10 steps, then the TADA angles changes back to 0,0
    
        # Find the changes in PF and EV and its respective start and end times; for PF, search motor_command['PF_cmd'] for all indices larger than 2 then save index
        trial_selector = []
        for i, val in enumerate(motor_command['PF_cmd']):
            if abs(val) > 2:
                # PF, EV, index of new TADA angle then PF, EV, index of next TADA angle that should be 0,0
                trial_selector.append([val,motor_command['EV_cmd'][i], time2[i], motor_command['PF_cmd'][i+1], motor_command['EV_cmd'][i+1], time2[i+1]])
        #print(trial_selector)
        
        # for EV, search motor_command['EV_cmd'] for all indices larger than 2 then save index
        for i, val in enumerate(motor_command['EV_cmd']):
            if abs(val) > 2:
                # PF, EV, index of new TADA angle then PF, EV, index of next TADA angle that should be 0,0
                trial_selector.append([motor_command['PF_cmd'][i], val, time2[i], motor_command['PF_cmd'][i+1], motor_command['EV_cmd'][i+1], time2[i+1]])
        #print(trial_selector)

        # create lists for all topics that creates regions of time based on trial selector where the cmds are not 0
        all_metrics = [moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments]
        all_time = [time, time1, time2, time3, time4, time5]
        topic_individual_dict = {}
        region = []
        regions = []
        
        # create topic regions that are lists of [angle_title, PF, EV, moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments]
        # where each region is a list of [time, data] and data is a dictionary of topics
        
        # search for particular region
        for i, trial_item in enumerate(trial_selector):
            #print(trial_item)
            # start the list with PF, EV
            angle_title = 'PF = ' + str(round(trial_item[0], 2)) + ', EV = ' + str(round(trial_item[1],2))
            topic_region_individual = [angle_title, trial_item[0], trial_item[1]]
            
            # search each topic/metric for that region of time
            for j, metric_val in enumerate(all_metrics):
                metric_time = all_time[j]
                
                # search for the index of the time that is closest to the time of the trial selector and add to list
                #print(metric_val)
                for key, (value1) in enumerate(metric_val.items()):
                    start_time = trial_item[2]
                    end_time = trial_item[5]
                    #print(start_time, end_time)
                
                    # find start_index of all_time[j] that is the value of start_time
                    #print(all_time[j])
                    for p, value in enumerate(metric_time):
                        if value <= start_time:
                            start_index = p
                        if value <= end_time:
                            end_index = p
                            
                    #print(start_index, end_index)
                    #print(value1[1])
                    #print(value1[0])
                    
                    # create list of value1 for the region of time between start_index and end_index
                    list_of_values = []
                    for q, q_val in enumerate(value1[1]):
                        #print(q, q_val)
                        if q >= start_index and q <= end_index:
                            list_of_values.append(q_val)
                            
                    # ensure that the list of time that starts at 0        
                    list_of_time = metric_time[start_index:end_index] - metric_time[start_index]
                    #print(list_of_values)
                    
                    # creates labels for plotting and legened grouping based on topics
                    metric_label = f'{value1[0],angle_title}'
                    legend_label = f'{value1[0]}' # '' # this variable groups the metrics of the same topic, change to '' if you don't want to group them
                    
                    # need to keep track of time and metric (different metrics have differet amount of indices)
                    topic_individual_dict[metric_label] = [list_of_time, list_of_values]
                    #print(list_of_values)
                    
                    # plot the topic for that region of time and group all metrics of the same topic
                    figure1.add_trace(go.Scatter(x=topic_individual_dict[metric_label][0],y=topic_individual_dict[metric_label][1], mode='lines', name=metric_label,legendgroup=legend_label))
                    #figure.show()
                    #break     
                    
                    # Sofya, this is one spot you can find the peaks for each metric during the stance periods of each region 
                    # But it may be difficult to create a general code to analyze all metrics so it may be better to write specific code for each metric
                    # Please see the comment with your name below step==2 for more details                    
                
                # add the dictionary metrics for one topic to the region list
                region.append(topic_individual_dict)
                #figure.show()
                #break
                #if j==0: break # look at first topic for a region
            
            # add all topics for the region to regions
            regions.append(region)     
            print(angle_title)
            #figure1.update_layout(title='TADA_angles', xaxis_title='Time (s)', yaxis_title='Metric value')
            #figure1.show()
            #print(topic_regions)
            #break
            #if i==1: break
        
        figure1.update_layout(title='TADA_angles', xaxis_title='Time (s)', yaxis_title='Metric value')
        figure1.show()
        
        # Save region data to a pickle file
        with open('region_data.pickle', 'wb') as handle:
            pickle.dump(regions, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        ########################################
elif step==2:
    # OR Sofya, you can instead process the peak finder here (focus on pylon moment, ang vel of shank, CM forward vel, foot segment pos and vel, hip/knee/ankle angles)
    # Add the peaks of the chosen to topic_individual_peaks_dict
    
    # Open pickle file for region data
    with open('region_data.pickle', 'rb') as handle:
        regions = pickle.load(handle)
        
    # Process region data
    
else: print("pick a valid option")

if step==1:
    ## Show entire time series for data of interest; Plot entire experiment
    # Future goal to plot the below graph using a for loop with the region variable allowing for much less written code
    figure.add_trace(go.Scatter(x=time, y=moments['mx'], mode='lines', name='Mx'))
    figure.add_trace(go.Scatter(x=time, y=moments['my'], mode='lines', name='My'))
    figure.add_trace(go.Scatter(x=time, y=moments['fz'], mode='lines', name='Fz'))

    figure.add_trace(go.Scatter(x=time1, y=imu_data['gyro_z'], mode='lines', name='gyro_z'))
    figure.add_trace(go.Scatter(x=time1, y=imu_data['state'], mode='lines', name='state'))

    figure.add_trace(go.Scatter(x=time2, y=motor_command['m1_cmd'], mode='lines', name='motor1_cmd (deg)')) # adding markers slows down the rendering
    figure.add_trace(go.Scatter(x=time2, y=motor_command['m2_cmd'], mode='lines', name='motor2_cmd (deg)')) 
    figure.add_trace(go.Scatter(x=time2, y=motor_command['PF_cmd'], mode='lines+markers', name='PF_cmd'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['EV_cmd'], mode='lines', name='EV_cmd'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU0'], mode='lines', name='CPU0'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU1'], mode='lines', name='CPU1'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU2'], mode='lines', name='CPU2'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU3'], mode='lines', name='CPU3'))

    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_sag_right'], mode='lines', name='hip_sag_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_sag_right'], mode='lines', name='knee_sag_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_sag_right'], mode='lines', name='ankle_sag_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_frontal_right'], mode='lines', name='hip_frontal_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_frontal_right'], mode='lines', name='knee_frontal_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_frontal_right'], mode='lines', name='ankle_frontal_right'))

    figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_x'], mode='lines', name='com_pos_x'))
    figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_y'], mode='lines', name='com_pos_y'))
    figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_z'], mode='lines', name='com_pos_z'))

    figure.add_trace(go.Scatter(x=time5, y=linear_moments['foot_vert_vel'], mode='lines', name='foot_vert_vel'))

    figure.update_layout(title='All data', xaxis_title='Time (s)', yaxis_title='Value')
    #figure.show() 


# Save the data to files
#bag_folder_path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\for_bags\data_kn"
#figure2.write_html(f'{bag_folder_path}/file_line.html')
#figure_polar.write_html(f'{bag_folder_path}/file_polar.html')
#figure_polar.write_image(f'{bag_folder_path}/file_polar.svg')
#figure_polar.write_image(f'{bag_folder_path}/file_polar.png')
   
# Show an interactive display of the data in a web browser
#fig = figure2
#figure2['layout'].update(height=1000)  
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#import dash_bootstrap_components as dbc

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.layout = html.Div([
#    dcc.Graph(figure=fig), ], 
##style = {'display': 'inline-block', 'height': '100%'}
#)

#app.run_server(debug=True, use_reloader=False, port=8050)

## Notes
# the windows and raspi systems have different timestamps
# ensure that pf/ev cmds are constant for the 10 or 5 steps
# there is a repeating weird negative 1 section that may correspond to the r in 10+r




