# Python
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
import pickle
from plotly.colors import n_colors

step = 1
time_offset = 0

# create array of 8 different colors from red to blue
#n_colors = 8
#colors = px.colors.sample_colorscale("Rainbow", [n/(n_colors) for n in range(n_colors)])
colors = n_colors('rgb(0, 255, 255)', 'rgb(255, 0, 255)', 255, colortype = 'rgb')
other_colors = n_colors('rgb(255, 0, 255)', 'rgb(0, 255, 255)', 255, colortype = 'rgb')

# find all files with '.bag' in name
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p1"
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\motor_test\test_may_22"
files = [f for f in os.listdir(path) if f.endswith('.bag') and f.startswith('P')]
#print(files)
topics = ['motor_command','motor_listen']

figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
figure3 = go.Figure()
figure4 = go.Figure()
figure5 = go.Figure()
figure6 = go.Figure()
figure7 = go.Figure()
#figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

# rosbag to csv
#rostopic echo -b expt1_correct.bag -p /motor_command > motor_cmd1.csv
#rostopic echo -b expt1_correct.bag -p /motor_listen > motor_listen1.csv

#M1,M2 = 0,0

# convert the rosbag to csv files that are based on topics
# this section is untested with new bag files. There is a small change you may get some errors.
if step==0:
    # loop through files
    for file in files:
        # create folder using subprocess
        reduced_file_name = file[:-4]
        print(reduced_file_name)        
        subprocess.run('mkdir {}'.format(path+'\\'+reduced_file_name), capture_output=True, text=True, shell=True)

        
        for topic in topics:
            print("rostopic echo -b {} -p /{} > {}\{}.csv".format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic))
            subprocess.run('rostopic echo -b {} -p /{} > {}\{}.csv'.format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic), capture_output=True, text=True, shell=True)
            
        #break
    ## loop through each topic
    #for topic in topics:
    ##    # Execute the command and retrieve the output
    #    subprocess.run('rostopic echo -b {} -p /{} > {}.csv'.format(files[0],topic,topic), capture_output=True, text=True, shell=True)

elif step==1:
    print(path)
    # find folders in path
    #folder = path+'\\attempt4\\'#+'data_attempt2\\' P10I100S250Tor1000Vel2000
    files = [f for f in os.listdir(path) if f.endswith('0') and f.startswith('P')]
    #files = files[0]
    print(files)
    # data folder
    #folder = 'no_motive\\'
    
    
    
    for file in files:
        motor_cmd = {'m1_cmd':[], 'm2_cmd':[], 'PF_cmd':[], 'EV_cmd':[], 'CPU0':[], 'CPU1':[], 'CPU2':[], 'CPU3':[]}
        motor_cmd_new = {'PF_cmd':[], 'EV_cmd':[]}
        motor_listen = {'curr_pos1':[], 'curr_pos2':[], 'curr_PF':[], 'curr_EV':[], 'q1':[], 'q5':[], 't_off':[]}
        motor_listen_new = {'curr_PF':[], 'curr_EV':[]}
        motive = {'time':[], 'rot_X':[], 'rot_Y':[], 'rot_Z':[], 'rot_W':[]}
        # Read motor cmd data from csv
        #folder = f'{file[:-4]}\\'
        #print(folder)#; break
        #data = pd.read_csv(folder+'motor_cmd2.csv')
        data = pd.read_csv(path+'\\'+file+'\\motor_command.csv')
        data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time_offset = 0#data.shape[0]-1 # 0
        time = data.field_t - data.field_t[0]#(data.time - 1*data.time[time_offset])/1_000_000_000
        #time = (data.field_t - data.field_t[0])/1_000_000_000 # using field as when the message was published
        motor_cmd['m1_cmd'] = data.field_motor1_move/567
        motor_cmd['m2_cmd'] = data.field_motor2_move/567
        motor_cmd['PF_cmd'], motor_cmd['EV_cmd'] = data.field_PF_cmd, data.field_EV_cmd
        motor_cmd['CPU0'], motor_cmd['CPU1'], motor_cmd['CPU2'], motor_cmd['CPU3'] = data.field_CPU0, data.field_CPU1, data.field_CPU2, data.field_CPU3
        motor_cmd_new['PF_cmd'], motor_cmd_new['EV_cmd'] = data.field_PF_cmd, data.field_EV_cmd
        
        data1 = pd.read_csv(path+'\\'+file+'\\motor_listen.csv')
        data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time_offset1 = 0#data1.shape[0]-1 # 0
        time1 = data1.field_t - data.field_t[0] - time_offset#(data1.time - 1*data.time[time_offset])/1_000_000_000 # there seems to be a consistent 1 or 2.4 sec delay depending on trial due when rosbag topics are started
        motor_listen['curr_pos1'] = data1.field_curr_pos1/567 
        motor_listen['curr_pos2'] = data1.field_curr_pos2/567
        motor_listen['t_off'] = data1.field_toff/1000


        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU0'], mode='lines', name='CPU0')) # adding markers slows down the rendering
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU1'], mode='lines', name='CPU1'))
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU2'], mode='lines', name='CPU2')) # adding markers slows down the rendering
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU3'], mode='lines', name='CPU3'))
        figure3.update_layout(title_text=f'{file}')
        #figure3.show()
        figure3 = go.Figure()

        figure4.add_trace(go.Scatter(x=time, y=motor_listen['t_off'], mode='markers', name='timing_offset_markers in microsec'))
        #figure4.add_trace(go.Scatter(x=time1, y=motor_listen['t_off'], mode='lines', name='timing_offset_lines'))
        figure4.update_layout(title_text=f'{file}')
        #figure4.show()
        figure4 = go.Figure()
    #exit()

        
        color_ind_array_old = [0, 1, 0, 1, 0, 1, 0, 1]
        color_ind_array = [0, 1, 0, 1, 0, 1, 0, 1]
        # add one to each item of color_ind_array and append it to color_ind_array. Do this 8 times
        for i in range(8):
            color_ind_array_new = [x+i for x in color_ind_array_old]
            color_ind_array += color_ind_array_new
    #print(color_ind_array); exit()  
                       
        #figure2 = go.Figure()
        #figure3.show()     
        #print(steady_info_time); #break
        print(f'{file}')
        #print("Averages and sd for CPU0:", [np.mean(motor_cmd['CPU0']), np.std(motor_cmd['CPU0'])], "CPU1:", [np.mean(motor_cmd['CPU1']), np.std(motor_cmd['CPU1'])], "CPU2:", [np.mean(motor_cmd['CPU2']), np.std(motor_cmd['CPU2'])], "CPU3:", [np.mean(motor_cmd['CPU3']), np.std(motor_cmd['CPU3'])])
        print("Average CPU load:", np.mean([motor_cmd['CPU0'], motor_cmd['CPU1'], motor_cmd['CPU2'], motor_cmd['CPU3']]), "CPU_sd:", np.std([motor_cmd['CPU0'], motor_cmd['CPU1'], motor_cmd['CPU2'], motor_cmd['CPU3']]))
        #print(file.find('S'))
        sampl_freq = np.float64(file[file.find('S')+1:])
        print("Average toff:", np.mean(motor_listen['t_off'])/sampl_freq, "toff_sd:", np.std(motor_listen['t_off']))
        #exit() 
        #                    
        

        #figure.write_html(folder+'file_motor.html')
        #figure_polar.write_image(f'{bag_folder_path}/file_polar.svg')
        #figure_polar.write_image(f'{bag_folder_path}/file_polar.png')

elif step==3:
    # I in increasing order, P in increasing order, S in increasing order
    cpu_load_avg = [[42.47, 36.75, 50.11], [43.67, 36.75, 43.28], [69.74, 36.75, 29.51]]
    cpu_load_sd = []
    toff_avg = [[27.66,97.81,63.14], [43.67,97.81,43.28], [-124.26,97.81,-132.3]]
    toff_sd = [[211.71,273.22,211.05], [26.36,273.22,27.48], [1323.05,273.22,998.64]] 
    P_gains = [1, 10, 1000]
    I_gains = [100, 1000, 10000]
    Sampl_freq = [10, 100, 500]
    Section = [1,2,3]
    colors = ['red', 'blue', 'green']
    labels = ['I_gains', 'P_gains', 'Sampl_freq']
    metric_labels = [I_gains, P_gains, Sampl_freq]
    y_labels = ['cpu_load_avg', 'toff_avg', 'toff_sd']
    X = [Section, Section, Section]
    Y = [cpu_load_avg, toff_avg, toff_sd]
    fig = go.Figure()
    for x,y_metric, metric_label, y_label in zip(X,Y, metric_labels, y_labels): #labels
        #for x,y in zip(X,y_ind):
        fig = go.Figure()
        # create one ploly Go graph with two y axes of different scales: cpu_load_avg and toff_sd
        # make x axis the same for both and use the Samp_freq
        # make the y axis for cpu_load_avg on the left and toff_sd on the right
        #x = X[i]
        #y = Y[i]
        #x=[]
        #y=[]
        for color, y,  label, item in zip(colors, y_metric, labels, metric_label):
        #    x.append(x_array[j])
        #    y.append(y_array[j])
        #print(x,y)
            
        #y2 = toff_avg[i]
        ##y3 = cpu_load_sd[i]
        #y4 = toff_sd[i]
            fig.add_trace(go.Scatter(x=x, y=y, name=f'{label}',  marker_color=color)) # legendgroup=label, #  of {item}
            #fig.add_trace(go.Scatter(x=x, y=y2, name='toff_avg', legendgroup='toff_avg', marker_color='blue'))
            ##fig.add_trace(go.Scatter(x=x, y=y3, name='CPU_load_sd', legendgroup='CPU_load_sd', marker_color='green'))
            #fig.add_trace(go.Scatter(x=x, y=y4, name='toff_sd', legendgroup='toff_sd', marker_color='green'))
            fig.update_layout(title='CPU_load_avg and toff_avg', xaxis_title=label, yaxis_title=y_label)
            #fig.update_yaxes(title_text="CPU_load_avg", secondary_y=False)
            #fig.update_yaxes(title_text="toff_avg", secondary_y=True)
            #fig.show()
            #fig.write_html(folder+'file_motor.html')
            #fig.write_image(f'{bag_folder_path}/file_polar.svg')  
            #break
        fig.show()
    
else: print("Pick correct option")





