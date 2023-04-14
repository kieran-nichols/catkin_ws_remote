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
import math

colors = ['red', 'blue', 'green']
figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
#figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

motor_cmd = {'m1_cmd':[], 'm2_cmd':[], 'PF_cmd':[], 'EV_cmd':[]}
motor_listen = {'curr_pos1':[], 'curr_pos2':[], 'curr_PF':[], 'curr_EV':[], 'q1':[], 'q5':[]}
motive = {'time':[], 'rot_X':[], 'rot_Y':[], 'rot_Z':[], 'rot_W':[]}

# rosbag to csv
#rostopic echo -b motive_expt1.bag -p /motor_command > motor_cmd1.csv
#rostopic echo -b motive_expt1.bag -p /motor_listen > motor_listen1.csv

#M1,M2 = 0,0

# https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians
    
def TADA_angle(M1,M2):
    
    # convert motor cmd to angle in rad
    q1 = (M1+0*141)/567*2*np.pi - 0*np.pi/2 # -141 was homed, 567 is counts per rev
    q5 = (M2+0*141)/567*2*np.pi - 0*np.pi/2 # 1*np.pi/2 for expt1 # 0*np.pi/2 for expt2
    
    q2 = np.pi/36; q4 = q2
    R01 = np.array([[np.cos(q1), -np.sin(q1), 0], [np.sin(q1), np.cos(q1), 0], [0, 0, 1]])
    R12 = np.array([[np.cos(q2), 0 , np.sin(q2)], [0, 1, 0], [-np.sin(q2), 0, np.cos(q2)]])
    
    q3 = -q1 - q5;
    #theta = theta_deg*math.pi/180
    #beta = 5*math.pi/180
    #q3 = 2*np.real((np.arccos(np.sin(theta/2)/np.sin(beta))))
    
    R23 = np.array([[np.cos(q3), -np.sin(q3), 0], [np.sin(q3), np.cos(q3), 0], [0, 0, 1]])
    R34 = np.array([[np.cos(q4), 0, np.sin(q4)], [0, 1, 0], [-np.sin(q4), 0, np.cos(q4)]])
    R45 = np.array([[np.cos(q5), -np.sin(q5), 0], [np.sin(q5), np.cos(q5), 0], [0, 0, 1]])
            
    R02 = np.matmul(R01,R12)
    R03 = np.matmul(R02,R23)
    R04 = np.matmul(R03,R34)
    R05 = np.matmul(R04,R45)
            
    PF = float(180/np.pi*R05[0,2])
    EV = float(180/np.pi*R05[1,2])
    return PF,EV,q1,q5
    
# data folder
#folder = 'no_motive\\'
folder = 'motive\\'

# Read motor cmd data from csv
data = pd.read_csv(folder+'motor_cmd2.csv')
data = pd.read_csv(folder+'motor_cmd1.csv')
data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
time_offset = 0#data.shape[0]-1 # 0
time = (data.time - 1*data.time[time_offset])/1_000_000_000
#time = (data.field_t - data.field_t[0])/1_000_000_000 # using field as when the message was published
motor_cmd['m1_cmd'] = data.field_motor1_move/567
motor_cmd['m2_cmd'] = data.field_motor2_move/567
motor_cmd['PF_cmd'], motor_cmd['EV_cmd'] = data.field_PF, data.field_EV
    
# read motor listen data from csv
data1 = pd.read_csv(folder+'motor_listen2.csv')
data1 = pd.read_csv(folder+'motor_listen1.csv')
data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
time_offset1 = 0#data1.shape[0]-1 # 0
time1 = (data1.time - 1*data.time[time_offset])/1_000_000_000 # there seems to be a consistent 1 or 2.4 sec delay depending on trial due when rosbag topics are started
motor_listen['curr_pos1'] = data1.field_curr_pos1/567
motor_listen['curr_pos2'] = data1.field_curr_pos2/567
#i=0
for i,x in enumerate(data1.field_curr_pos1):
    #for y in data.field_motor2_move:
    #i+=1
    a,b,c,d = TADA_angle(x,data1.field_curr_pos2[i])
    motor_listen['curr_PF'].append(a) 
    motor_listen['curr_EV'].append(b)
    motor_listen['q1'].append(c) 
    motor_listen['q5'].append(d)
    #print(i)

data2 = pd.read_csv(folder+'EXPT2_reduced.csv')
data2 = pd.read_csv(folder+'EXPT1_reduced.csv')
#data2.columns = data2.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
#print(data2)
time2 = data2.Time - (-11.3)#-11.3#6.6
#motive['rot_X'] = data2.X
#motive['rot_Y'] = data2.Y
#motive['rot_Z'] = data2.Z
#motive['rot_W'] = data2.W
offset = 0
for i,item in enumerate(data2.Time):
    x,y,z = euler_from_quaternion(data2.X[i], data2.Y[i], data2.Z[i], data2.W[i])
    if i == 0:offset = -x/np.pi*180
    motive['rot_X'].append(-x/np.pi*180-offset-4)#12.6)
    motive['rot_Y'].append(y/np.pi*180)
    motive['rot_Z'].append(-z/np.pi*180-2)

    
# specify the figure lines with time as x and motor cmd and listen as y
#figure.data = []
figure.add_trace(go.Scatter(x=time, y=motor_cmd['m1_cmd'], mode='lines', name='motor1_cmd')) # adding markers slows down the rendering
figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos1'], mode='lines', name='curr_pos of motor1'))
figure.add_trace(go.Scatter(x=time, y=motor_cmd['m2_cmd'], mode='lines', name='motor2_cmd')) # adding markers slows down the rendering
figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos2'], mode='lines', name='curr_pos of motor2'))
figure.show()

figure2.add_trace(go.Scatter(x=time2, y=motive['rot_X'], mode='lines', name='rot_X of motive')) 
figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Y'], mode='lines', name='rot_Y of motive'))
figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Z'], mode='lines', name='rot_Z of motive'))
#figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos1'], mode='lines', name='curr_pos of motor1'))
figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_EV'], mode='lines', name='curr_EV'))
figure2.show()

figure1.add_trace(go.Scatter(x=time, y=motor_cmd['PF_cmd'], mode='lines', name='PF_cmd')) # adding markers slows down the rendering
figure1.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
figure1.add_trace(go.Scatter(x=time, y=motor_listen['q1'], mode='lines', name='q1')) # adding markers slows down the rendering
figure1.add_trace(go.Scatter(x=time1, y=motor_listen['q5'], mode='lines', name='q5'))
figure1.add_trace(go.Scatter(x=time, y=motor_cmd['EV_cmd'], mode='lines', name='EV_cmd')) # adding markers slows down the rendering
figure1.add_trace(go.Scatter(x=time1, y=motor_listen['curr_EV'], mode='lines', name='curr_EV'))
figure1.show()
# Notes: 
#        need to be careful with taking timing data; need to get timestamp when data was published not when it is rosbag-ed

#figure2.update_layout(title_text="Average Moment Peaks for a given speed")
#figure2.update_layout(xaxis1_title="TADA angle (anatomical angle)", yaxis_title="Frontal Moment (N*m)")
#figure2.update_layout(xaxis2_title="TADA angle (anatomical angle)", yaxis2_title="Sagittal Moment (N*m)")
##figure2.update_layout(xaxis3_title="TADA angle (anatomical angle)", yaxis3_title="Resultant Moment (N*m)")
#figure2.update_layout(legend_title="Speed (m/s)")

#figure.write_html(folder+'file_motor.html')
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




