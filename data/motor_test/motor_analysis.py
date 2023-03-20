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

colors = ['red', 'blue', 'green']

figure = go.Figure()
figure1 = go.Figure()
figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

motor_cmd = {'m1_cmd':[], 'm2_cmd':[], 'PF_cmd':[], 'EV_cmd':[]}
motor_listen = {'curr_pos1':[], 'curr_pos2':[], 'curr_PF':[], 'curr_EV':[]}

# rosbag to csv
#rostopic echo -b motor_expt1.bag -p /motor_command > motor_cmd1.csv
#rostopic echo -b motor_expt1.bag -p /motor_listen > motor_listen1.csv

#M1,M2 = 0,0

def TADA_angle(M1,M2):
    # convert motor cmd to angle in rad
    q1 = (M1 + 141)/567*np.pi*2 - 0*np.pi # -141 was homed, 567 is counts per rev
    q5 = (M2 + 141)/567*np.pi*2 - 0*np.pi

    #q1 = (q1 + np.pi)%(2*np.pi) - np.pi
    #q5 = (q5 + np.pi)%(2*np.pi) - np.pi

    q2 = np.pi/36; q4 = q2
    R01 = np.array([[np.cos(q1), -np.sin(q1), 0], [np.sin(q1), np.cos(q1), 0], [0, 0, 1]])
    R12 = np.array([[np.cos(q2), 0 , np.sin(q2)], [0, 1, 0], [-np.sin(q2), 0, np.cos(q2)]])
    q3 = -q1 - q5;
    R23 = np.array([[np.cos(q3), -np.sin(q3), 0], [np.sin(q3), np.cos(q3), 0], [0, 0, 1]])
    R34 = np.array([[np.cos(q4), 0, np.sin(q4)], [0, 1, 0], [-np.sin(q4), 0, np.cos(q4)]])
    R45 = np.array([[np.cos(q5), -np.sin(q5), 0], [np.sin(q5), np.cos(q5), 0], [0, 0, 1]])
            
    R02 = np.matmul(R01,R12)
    R03 = np.matmul(R02,R23)
    R04 = np.matmul(R03,R34)
    R05 = np.matmul(R04,R45)
            
    PF = float(180/np.pi*R05[0,2])
    EV = float(180/np.pi*R05[1,2])
    return PF,EV
    
# Read motor cmd data from csv
data = pd.read_csv('motor_cmd.csv')
data = pd.read_csv('motor_cmd1.csv')
data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
time_offset = 0#data.shape[0]-1 # 0
time = (data.time - 1*data.time[time_offset])/1_000_000_000
#time = (data.field_t - data.field_t[0])/1_000_000_000 # using field as when the message was published
motor_cmd['m1_cmd'] = data.field_motor1_move/567
motor_cmd['m2_cmd'] = data.field_motor2_move/567
motor_cmd['PF_cmd'], motor_cmd['EV_cmd'] = data.field_PF, data.field_EV
    
# read motor listen data from csv
data1 = pd.read_csv('motor_listen.csv')
data1 = pd.read_csv('motor_listen1.csv')
data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
time_offset1 = 0#data1.shape[0]-1 # 0
time1 = (data1.time - 1*data.time[time_offset])/1_000_000_000 # there seems to be a consistent 1 or 2.4 sec delay depending on trial due when rosbag topics are started
motor_listen['curr_pos1'] = data1.field_curr_pos1/567
motor_listen['curr_pos2'] = data1.field_curr_pos2/567
#i=0
for i,x in enumerate(data1.field_curr_pos1):
    #for y in data.field_motor2_move:
    #i+=1
    a,b = TADA_angle(x,data1.field_curr_pos2[i])
    motor_listen['curr_PF'].append(a) 
    motor_listen['curr_EV'].append(b)
    #print(i)

# create a figure
figure = go.Figure()
figure1 = go.Figure()
show_legend = False
    
# specify the figure lines with time as x and motor cmd and listen as y
#figure.data = []
figure.add_trace(go.Scatter(x=time, y=motor_cmd['m1_cmd'], mode='lines', name='motor1_cmd')) # adding markers slows down the rendering
figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos1'], mode='lines', name='curr_pos of motor1'))
figure.show()

figure1.add_trace(go.Scatter(x=time, y=motor_cmd['PF_cmd'], mode='lines', name='PF_cmd')) # adding markers slows down the rendering
figure1.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
figure1.show()
# Notes: 
#        need to be careful with taking timing data; need to get timestamp when data was published not when it is rosbag-ed

#figure2.update_layout(title_text="Average Moment Peaks for a given speed")
#figure2.update_layout(xaxis1_title="TADA angle (anatomical angle)", yaxis_title="Frontal Moment (N*m)")
#figure2.update_layout(xaxis2_title="TADA angle (anatomical angle)", yaxis2_title="Sagittal Moment (N*m)")
##figure2.update_layout(xaxis3_title="TADA angle (anatomical angle)", yaxis3_title="Resultant Moment (N*m)")
#figure2.update_layout(legend_title="Speed (m/s)")

#bag_folder_path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\for_bags\data_kn"
#figure2.write_html(f'{bag_folder_path}/file_line.html')

#figure.write_html('file_motor.html')

#figure_polar.write_image(f'{bag_folder_path}/file_polar.svg')
#figure_polar.write_image(f'{bag_folder_path}/file_polar.png')

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




