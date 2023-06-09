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

step = 2
time_offset = 0

# create array of 8 different colors from red to blue
#n_colors = 8
#colors = px.colors.sample_colorscale("Rainbow", [n/(n_colors) for n in range(n_colors)])
colors = n_colors('rgb(0, 255, 255)', 'rgb(255, 0, 255)', 255, colortype = 'rgb')
other_colors = n_colors('rgb(255, 0, 255)', 'rgb(0, 255, 255)', 255, colortype = 'rgb')

# find all files with '.bag' in name
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p1"
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\motor_test\test_may_22"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
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
figure8 = go.Figure()
figure9 = go.Figure()
#figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

# rosbag to csv
#rostopic echo -b expt1_correct.bag -p /motor_command > motor_cmd1.csv
#rostopic echo -b expt1_correct.bag -p /motor_listen > motor_listen1.csv

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
    
def TADA_angle(M1,M2,theta):
    
    # convert motor cmd to angle in rad
    q1 = (M1-374)/567*2*np.pi - 0*np.pi/2 # -141 was homed, 567 is counts per rev
    q5 = (M2-382)/567*2*np.pi - 0*np.pi/2 # 1*np.pi/2 for expt1 # 0*np.pi/2 for expt2
    
    q2 = np.pi/36; q4 = q2
    R01 = np.array([[np.cos(q1), -np.sin(q1), 0], [np.sin(q1), np.cos(q1), 0], [0, 0, 1]])
    R12 = np.array([[np.cos(q2), 0 , np.sin(q2)], [0, 1, 0], [-np.sin(q2), 0, np.cos(q2)]])
    
    q3 = -q1 - q5;
    theta = theta*math.pi/180
    beta = 5*math.pi/180
    #q3 = 2*np.real((np.arccos(np.sin(theta/2)/np.sin(beta))))
    
    R23 = np.array([[np.cos(q3), -np.sin(q3), 0], [np.sin(q3), np.cos(q3), 0], [0, 0, 1]])
    R34 = np.array([[np.cos(q4), 0, np.sin(q4)], [0, 1, 0], [-np.sin(q4), 0, np.cos(q4)]])
    R45 = np.array([[np.cos(q5), -np.sin(q5), 0], [np.sin(q5), np.cos(q5), 0], [0, 0, 1]])
            
    R02 = np.matmul(R01,R12)
    R03 = np.matmul(R02,R23)
    R04 = np.matmul(R03,R34)
    R05 = np.matmul(R04,R45)
            
    PF = float(180/np.pi*math.atan2(R05[0,2],R05[2,2]))
    EV = float(180/np.pi*math.atan2(R05[1,2],R05[2,2]))
    #PF = float(180/np.pi*R05[0,2])
    #EV = float(180/np.pi*R05[1,2])
    return PF,EV,q1,q5

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
    folder = path+'\\attempt4\\'#+'data_attempt2\\' P10I100S250Tor1000Vel2000
    files = os.listdir(folder)
    files = files[0]
    print(files)
    # data folder
    #folder = 'no_motive\\'
    
    
    
    for file in files[0]:
        motor_cmd = {'m1_cmd':[], 'm2_cmd':[], 'PF_cmd':[], 'EV_cmd':[], 'CPU0':[], 'CPU1':[], 'CPU2':[], 'CPU3':[]}
        motor_cmd_new = {'PF_cmd':[], 'EV_cmd':[]}
        motor_listen = {'curr_pos1':[], 'curr_pos2':[], 'curr_PF':[], 'curr_EV':[], 'q1':[], 'q5':[], 't_off':[]}
        motor_listen_new = {'curr_PF':[], 'curr_EV':[]}
        motive = {'time':[], 'rot_X':[], 'rot_Y':[], 'rot_Z':[], 'rot_W':[]}
        # Read motor cmd data from csv
        #folder = f'{file[:-4]}\\'
        #print(folder)#; break
        #data = pd.read_csv(folder+'motor_cmd2.csv')
        data = pd.read_csv(folder+'motor_command.csv')
        data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time_offset = 0#data.shape[0]-1 # 0
        time = data.field_t - data.field_t[0]#(data.time - 1*data.time[time_offset])/1_000_000_000
        #time = (data.field_t - data.field_t[0])/1_000_000_000 # using field as when the message was published
        motor_cmd['m1_cmd'] = data.field_motor1_move/567
        motor_cmd['m2_cmd'] = data.field_motor2_move/567
        motor_cmd['PF_cmd'], motor_cmd['EV_cmd'] = data.field_PF_cmd, data.field_EV_cmd
        # find norm of data.field_PF_cmd and data.field_EV_cmd
        angle_norm = []
        for i,x in enumerate(data.field_PF_cmd):
            if round(x) == 0: x = data.field_EV_cmd[i]
            angle_norm.append(abs(round(x,1)))
        #print(angle_norm)
        motor_cmd['CPU0'], motor_cmd['CPU1'], motor_cmd['CPU2'], motor_cmd['CPU3'] = data.field_CPU0, data.field_CPU1, data.field_CPU2, data.field_CPU3
        motor_cmd_new['PF_cmd'], motor_cmd_new['EV_cmd'] = data.field_PF_cmd, data.field_EV_cmd
    
        ## read motor listen data from csv
        #data1 = pd.read_csv(folder+'motor_listen2.csv')
        data1 = pd.read_csv(folder+'motor_listen.csv')
        data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
        time_offset1 = 0#data1.shape[0]-1 # 0
        time1 = data1.field_t - data.field_t[0] - time_offset#(data1.time - 1*data.time[time_offset])/1_000_000_000 # there seems to be a consistent 1 or 2.4 sec delay depending on trial due when rosbag topics are started
        motor_listen['curr_pos1'] = data1.field_curr_pos1/567 
        motor_listen['curr_pos2'] = data1.field_curr_pos2/567
        motor_listen['t_off'] = data1.field_toff/1000
        ###i=0
        # find the value of data1.field_t[0] in data1.field_t
        for i,x in enumerate(time1):
            if x == 0: 
                shift_ind = i
                break
        print(shift_ind,"need to investigate")
        for i,x in enumerate(data1.field_curr_pos1):
            ##for y in data.field_motor2_move:
            ##i+=1
            a,b,c,d = TADA_angle(x,data1.field_curr_pos2[i],angle_norm[i-shift_ind])
            motor_listen['curr_PF'].append(a) 
            motor_listen['curr_EV'].append(b)
            motor_listen_new['curr_PF'].append(a) 
            motor_listen_new['curr_EV'].append(b)
            motor_listen['q1'].append(c) 
            motor_listen['q5'].append(d)
        #    ##print(i)

        ##data2 = pd.read_csv(folder+'EXPT2_reduced.csv')
        data2 = pd.read_csv(folder+'attempt4_motive.csv') # motive_data.csv
        ###print(data2)

        time2 = data2.Time - 7.85#-11.3#6.6

        for i,item in enumerate(data2.Time):
        #    #x,y,z = data2.X[i], data2.Y[i], data2.Z[i]
            x,y,z = euler_from_quaternion(data2.X[i], data2.Y[i], data2.Z[i], data2.W[i])
        ##    #if i == 0:offset = -x/np.pi*180
            motive['rot_X'].append(x/np.pi*180+1.91)
            motive['rot_Y'].append(y/np.pi*180+0.32)
            motive['rot_Z'].append(z/np.pi*180-6.61+1.7)

                # specify the figure lines with time as x and motor cmd and listen as y
        figure.data = []

        figure.add_trace(go.Scatter(x=time, y=motor_cmd['m1_cmd'], mode='lines', name='motor1_cmd')) # adding markers slows down the rendering
        figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos1'], mode='lines', name='curr_pos of motor1'))
        figure.add_trace(go.Scatter(x=time, y=motor_cmd['m2_cmd'], mode='lines', name='motor2_cmd')) # adding markers slows down the rendering
        figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos2'], mode='lines', name='curr_pos of motor2'))
        #figure.show()

        figure2.add_trace(go.Scatter(x=time2, y=motive['rot_X'], mode='lines', name='rot_X of motive')) 
        figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Y'], mode='lines', name='rot_Y of motive'))
        figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Z'], mode='lines', name='rot_Z of motive'))
        figure2.add_trace(go.Scatter(x=time, y=motor_cmd['PF_cmd'], mode='lines', name='PF_cmd'))
        figure2.add_trace(go.Scatter(x=time, y=motor_cmd['EV_cmd'], mode='lines', name='EV_cmd'))
        figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
        figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_EV'], mode='lines', name='curr_EV'))
        # add title
        figure2.update_layout(title_text=f'{folder[:-1]}')
        #figure2.show()
        figure2 = go.Figure()
        
        period = slice(24550,24720)
        offset = 75
        period1 = slice(24550-offset,24720-offset)
        movement = motor_listen['curr_PF'][period1] - motor_cmd['PF_cmd'][period]
        #if abs(movement[0]-movement[offset+ind])/abs(movement[0])>=0.95: #difference < 0.25: # change in error in degrees                            
        #if np.nanmean(difference_array[i][-10:])<0.1 and len(difference_array[i][-10:])>=10 and abs(val) < 1: #difference < 0.25: # change in error in degrees

        figure1.add_trace(go.Scatter(x=time[period], y=motor_cmd['PF_cmd'][period], mode='lines', name='PF_command',marker=dict(color='red'))) # adding markers slows down the rendering
        figure1.add_trace(go.Scatter(x=time1[period1], y=motor_listen['curr_PF'][period1], mode='lines', name='PF_actual',marker=dict(color='lightcoral')))        
        figure1.add_trace(go.Scatter(x=time[period], y=motor_cmd['EV_cmd'][period], mode='lines', name='EV_command',marker=dict(color='blue'))) # adding markers slows down the rendering
        figure1.add_trace(go.Scatter(x=time1[period1], y=motor_listen['curr_EV'][period1], mode='lines', name='EV_actual',marker=dict(color='steelblue')))
        figure1.add_trace(go.Scatter(x=[time1[24598-offset],time1[24682-offset]], y=[motor_listen['curr_PF'][24598-offset],motor_listen['curr_PF'][24682-offset]], mode='markers', name='95% Rise Time', marker=dict(size=10)))
        figure1.add_trace(go.Scatter(x=[time1[24613-offset],time1[24699-offset]], y=[motor_listen['curr_PF'][24613-offset],motor_listen['curr_PF'][24699-offset]], mode='markers', name='Settling Time', marker=dict(size=10)))
        figure1.update_layout(title_text=f'Ankle Angle commands and actual positions')
        figure1.update_xaxes(title_text='Time (s)')
        figure1.update_yaxes(title_text='PF and EV Angles (deg)')
        figure1.show()

        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU0'], mode='lines', name='CPU0')) # adding markers slows down the rendering
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU1'], mode='lines', name='CPU1'))
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU2'], mode='lines', name='CPU2')) # adding markers slows down the rendering
        figure3.add_trace(go.Scatter(x=time, y=motor_cmd['CPU3'], mode='lines', name='CPU3'))
        figure3.update_layout(title_text=f'{folder[:-1]}')
        #figure3.show()
        figure3 = go.Figure()

        figure4.add_trace(go.Scatter(x=time1, y=motor_listen['t_off'], mode='markers', name='timing_offset_markers in microsec'))
        #figure4.add_trace(go.Scatter(x=time1, y=motor_listen['t_off'], mode='lines', name='timing_offset_lines'))
        figure4.update_layout(title_text=f'{folder[:-1]}')
        #figure4.show()
        #figure4 = go.Figure()
        exit()

        
        # create lists for all topics that creates regions of time based on trial selector where the cmds are not 0
        all_metrics = [motor_cmd, motor_listen, motive] #motor_listen
        all_time = [time, time1, time2]
        topic_individual_dict = []
        region = []
        regions = []

        # Find the changes in PF and EV and its respective start and end times; for PF, search motor_command['PF_cmd'] for all indices larger than 2 then save index
        trial_selector = []
        start_info={'start_time':[], 'start_index':[], 'PF':[], 'EV':[]}
        prev_val = 0
        region = [{'TADA_angle':[]}]

        for i, val in enumerate(motor_cmd['PF_cmd']):
            approx_val = round(val, 2)
            diff = abs(approx_val - prev_val)
            # find start time when approx val changes value and end time when it stops being equal to approx_val
            #if approx_val>2 or approx_val < -2:
            if  diff > 0.1:
                start_time = time[i]
                start_info['start_time'].append(start_time)
                start_info['start_index'].append(i)
                start_info['PF'].append(approx_val)
                start_info['EV'].append(round(motor_cmd['EV_cmd'][i],2))
            prev_val = approx_val
        #print(start_info)

        # loop through all start times in start_info minus 1
        for i, start_time in enumerate(start_info['start_time']):
            angle_title = 'PF = ' + str(start_info['PF'][i]) + ', EV = ' + str(start_info['EV'][i])
            #print(angle_title)
            region = []    
            # look at all metrics (two)
        
            for j, metric in enumerate(all_metrics): # angle_comparison, all_metrics
                # look at all topics of a metric (7-8 topics)
                topic_individual_dict = {}
                for k, topic in enumerate(metric.items()):            
                    end_time = start_info['start_time'][i+1]
                    start_time = start_info['start_time'][i]
                    start_index = start_info['start_index'][i]
                    end_index = start_info['start_index'][i+1]
                    list_of_values = []
                    #print(topic[0])
                    # find the region that is within the start and end time
                    for q, q_val in enumerate(topic[1]):
                        #for l, value1 in enumerate(q_val):
                        #print(q, q_val)
                        #if q >= start_index and q <= end_index:
                        #try: # decided to ignore some errors from the below line
                        topic_time = all_time[j][q]
                        if topic_time >= start_time and topic_time <= end_time:
                            list_of_values.append(q_val)
                        #except: pass
                    #list_of_time = all_time[0][start_index:end_index]# - all_time[j][start_index] # 
                    list_of_time = all_time[j][start_index:end_index] - all_time[j][start_index] # set all chunks to have an initial time of 0
                    #print(list_of_values)
                    legend_label = f'{topic[0]}' # ''
                    metric_label = f'{topic[0]}, {angle_title}'
                    # need to keep track of time and metric (different metrics have differet amount of indices)
                    topic_individual_dict[topic[0]] = ([metric_label, list_of_time, list_of_values])
            
                    figure1.add_trace(go.Scatter(x=list_of_time,y=list_of_values, mode='lines', name=metric_label,legendgroup=legend_label))
                
                # add the dictionary metrics for one topic to the region list
                region.append(topic_individual_dict)
            
            # add all topics for the region to regions
            regions.append(region) 
        
            # if i is end-1 then break loop
            break_cond = len(start_info['start_time'])-2 # 1
            if i == break_cond: break  
    
        #exit()  
        #figure1.show()
    
        ## Save region data to a pickle file
        with open(folder+'region_motor.pickle', 'wb') as handle: # region_motor_all, region_angle_accurray
            pickle.dump(regions, handle, protocol=pickle.HIGHEST_PROTOCOL)

elif step==2:  
    
    steady_info_time = []
    steady_info_val = []
    steady_info_displacement = []
    #files = files[1]
    #print(files)
    folder = path+'\\attempt4\\'#+'data_attempt2\\'    #chosen_topic_array = ['PF_cmd', 'EV_cmd', 'curr_PF', 'curr_EV']
    # Open pickle file for region data
    
    #for file in files[1]:
        #folder = f'{file[:-4]}\\'
        #print(folder)#; break
        
    #with open(path+'\\'+folder+'region_motor.pickle', 'rb') as handle: # region_motor_all, region_angle_accurray, region_motor_quat
    with open(folder+'region_motor.pickle', 'rb') as handle: # region_motor_all, region_angle_accurray, region_motor_quat
        regions = pickle.load(handle)
    color_ind_array_old = [0, 1, 0, 1, 0, 1, 0, 1]
    color_ind_array = [0, 1, 0, 1, 0, 1, 0, 1]
    # add one to each item of color_ind_array and append it to color_ind_array. Do this 8 times
    for i in range(8):
        color_ind_array_new = [x+i for x in color_ind_array_old]
        color_ind_array += color_ind_array_new
    #print(color_ind_array); exit()
        
    # Create break up regions into regions, a region is for a chunck of time
            
    steady_info_time = [[],[]]
    steady_info_val = [[],[]]
    steady_info_displacement = [[],[]]
    counter = [0, 0]
    angle_control_array = [[],[]]
    angle_actual_array = [[],[]]
    angle_motive_array = [[],[]]
    motor_angle_array = [[],[]]
    move_time_95 = [[],[]]
            
    for x, region in enumerate(regions):
            
        # region[0] refers to cmds and [1] refers to listen
        metric_cmd = region[0]['PF_cmd']
        PF_command = metric_cmd[2] # 0 is PF for metric[0]
        metric_cmd_ev = region[0]['EV_cmd']
        EV_command = metric_cmd_ev[2] # 0 is PF for metric[0]
        metric_cmd_m = region[0]
        metric_cmd_m1 = metric_cmd_m['m1_cmd'][2]
        #print(metric_cmd_m1)
        metric_cmd_m2 = metric_cmd_m['m2_cmd'][2]
        time_list = [z for z in metric_cmd[1]]# need to split up panda
        name_ind = metric_cmd[0].find('PF =')
        name = metric_cmd[0][name_ind:]  
        pf = float(name[name.find('PF =')+4:name.find(',')])
        ev = float(name[name.find('EV = ')+4:])
            
        metric_actual = region[1]['curr_PF']
        PF_actual = metric_actual[2] # 0 is PF for metric[0]
        metric_actual_ev = region[1]['curr_EV']
        EV_actual = metric_actual_ev[2] # 0 is PF for metric[0]
        metric_actual_m = region[1]
        metric_actual_m1 = [z*360 for z in metric_actual_m['curr_pos1'][2]]
        metric_actual_m2 = [z*360 for z in metric_actual_m['curr_pos2'][2]]
        #print(metric_actual_m1)
        
        metric_motive = region[2]['rot_Z']
        PF_motive = metric_motive[2] # 0 is PF for metric[0] 
        metric_motive_ev = region[2]['rot_X']
        EV_motive = metric_motive_ev[2] # 0 is PF for metric[0] 
        time_motive = [z for z in metric_motive[1]]# need to split up panda
            
        metric_CPU0 = region[0]['CPU0']
        metric_CPU1 = region[0]['CPU1']
        metric_CPU2 = region[0]['CPU2']
        metric_CPU3 = region[0]['CPU3']
        CPU0 = metric_CPU0[2] 
        CPU1 = metric_CPU1[2] 
        CPU2 = metric_CPU2[2] 
        CPU3 = metric_CPU3[2] 
            
        metric_toff = region[1]['t_off']
        toff = metric_toff[2]            
            
        # use list comprehension to find the difference of each item of two lists: values_list[1] and values_list[0] and create a new list
        #print(len(time_list), len(PF_command), len(PF_actual))
        min_list_length = min(100, len(time_list), len(PF_command), len(PF_actual), len(PF_motive)) # PF_actual ensure resulting list is as long as the min length of each list or 100 (1 sec)
        diff = [PF_command[i] - PF_actual[i] for i in range(min_list_length)] #change diff to something elsecd ca
        diff_motive = [PF_command[i] - PF_motive[i] for i in range(min_list_length)]
        angle_cmd = [[PF_command[i], EV_command[i]] for i in range(min_list_length)]
        angle_actual = [[PF_actual[i], EV_actual[i]] for i in range(min_list_length)]
        angle_motive = [[PF_motive[i], EV_motive[i]] for i in range(min_list_length)]
        motor_angle = [[metric_actual_m1[i]-metric_actual_m1[0], metric_actual_m2[i]-metric_actual_m2[0]] for i in range(min_list_length)]
        #print(motor_angle); exit()
        i = 0
        # find movement time by searching for a change of value starting at the end of the diff arrays
        offset = 10
        steady_time = [0,0]
        steady_val = [0,0]
        dist_trav = [0,0]
        first = 0  
        difference_array = [[],[]]
            
        # For hall sensors and motive
        movements = [diff, diff_motive]
        for i, movement in enumerate(movements):
            prev_val = 0
            first = 0
            #if i==1: min_list_length = 50; else: pass
            indexes = list(range(offset,min_list_length))
            last = 0
            stop = 0
            
            for ind, (j, val, t) in enumerate(zip(indexes,movement[offset:min_list_length], time_list[offset:min_list_length])):
                #approx_val = round(val, 2)
                approx_val = val
                difference = abs(approx_val - prev_val)
                difference_array[i].append(difference)
                prev_val = approx_val                
                
                # find start time when approx val changes value and end time when it stops being equal to approx_val
                # mean of last 5 items of steady_info_val should be less than 0.25

                if abs(movement[0]-movement[offset+ind])/abs(movement[0])>=0.95 and abs(val) < 1 and stop == 0: #difference < 0.25: # change in error in degrees
                    move_time_95[i].append(t)
                    stop = 1
                
                if np.nanmean(difference_array[i][-10:])<0.1 and len(difference_array[i][-10:])>=10 and abs(val) > 1 and last==0:
                    counter[i] += 1  
                    last = 1
                
                if np.nanmean(difference_array[i][-10:])<0.1 and len(difference_array[i][-10:])>=10 and abs(val) < 1: #difference < 0.25: # change in error in degrees
                    #if abs(approx_val) < 0.25:
                    steady_time[i] = [t-0.1]
                    steady_val[i] = [val]
                    dist_trav[i] = [abs(movement[0])]
                    steady_info_time[i].append(steady_time[i][0])
                    steady_info_val[i].append(abs(val)) 
                    steady_info_displacement[i].append(dist_trav[i])
                    
                    if i==0:
                        pf_control, ev_control = angle_cmd[j]
                        angle_control_array.append([pf_control, ev_control])
                        pf_actual, ev_actual = angle_actual[j]
                        angle_actual_array.append([pf_actual, ev_actual])
                        x,y = motor_angle[j]
                        motor_angle_array.append([x,y])
                    else:
                        pf_motive, ev_motive = angle_motive[j]
                        angle_motive_array.append([pf_motive, ev_motive])
                    
                    #print(steady_val[i])    
                    break
                   
                # need to complete
                    #elif abs(approx_val) > 0.25 and np.nanmean(difference_array[i][-10:])<0.1: # abs(approx_val) > 0.25:# and first==0: # abs(approx_val) > 2
                    #    steady_time[i] = [t]
                    #    steady_val[i] = [val]
                    #    dist_trav[i] = [abs(movement[0])]
                    #    #steady_t = t
                    #    #stedy_value = abs(val)
                    #    #steady_disp = dist_trav[i]
                    #    steady_info_time[i].append(t)
                    #    steady_info_val[i].append(abs(val)) 
                    #    steady_info_displacement[i].append(dist_trav[i])
                    #    #first = 1
                    #    break
                        
                # t is equal to last item of time_list
                elif t==time_list[min_list_length-1] and False:                  
                    steady_time[i] = [t]
                    steady_val[i] = [val]
                    dist_trav[i] = [abs(movement[0])]
                    counter[i] += 1     
                    #if first!=0:
                    #steady_info_time[i].append(steady_t)
                    #steady_info_val[i].append(stedy_value) 
                    #steady_info_displacement[i].append(steady_disp)
                    #counter[i] += 1
                    #else:
                    steady_info_time[i].append(t)
                    steady_info_val[i].append(abs(val)) 
                    steady_info_displacement[i].append(dist_trav[i])
                    #    #counter += 1
                    #    first = 0
                    #print(steady_val[i])
                    break
                
                else: pass              
                                
                #i+=1
        #print(steady_time, steady_val)        
        #print(x, name)  
        # go to the next item of the list, colors
        #color = colors[color_ind_array[x]]
        #other_color = other_colors[color_ind_array[x]]
        try:
            figure2.add_trace(go.Scatter(x=time_list,y=movements[0], mode='lines', name=name, legendgroup=name))#, marker_color=color)) # name, 'hall_sensors'
            figure2.add_trace(go.Scatter(x=steady_time[0],y=steady_val[0], mode='markers', name=name, legendgroup=name))#, marker_color=other_color)) # name, 'hall_sensors'
            figure5.add_trace(go.Scatter(x=time_list,y=movements[1], mode='lines', name=name, legendgroup=name))#, marker_color=color)) # name, 'hall_sensors'
            figure5.add_trace(go.Scatter(x=steady_time[1],y=steady_val[1], mode='markers', name=name, legendgroup=name))#, marker_color=other_color)) # name, 'hall_sensors'
            
            figure6.add_trace(go.Scatter(x=[ev_control], y=[pf_control], mode='markers', marker_color='Red')) 
            figure6.add_trace(go.Scatter(x=[ev_actual], y=[pf_actual], mode='markers', marker_color='Blue'))
            #figure6.add_trace(go.Scatter(x=[ev_motive], y=[pf_motive], mode='markers', marker_color='Purple'))
                    
            
        except: pass
        #figure4.add_trace(go.Scatter(x=steady_time,y=dist_trav, mode='markers', name=name, legendgroup=name, marker_color=color)) # name, 'hall_sensors'
        #figure3.add_trace(go.Scatter(x=time_list,y=diff_motive, mode='lines', name=name, legendgroup=name, marker_color=color)) # 'motive'
            #something in the below line is causing the error due to the length of the arrays or some error in the detector
        #figure3.add_trace(go.Scatter(x=steady_time[1],y=steady_val[1], mode='lines', name=name, legendgroup=name, marker_color=other_color)) # 'motive'
        #break
    #print([z for z in motor_angle_array if z!= []], '\n\n',steady_info_time[0])  ; exit()
    x0 = [abs(z[0]) for z in motor_angle_array if z!=[]]
    x1 = [abs(z[1]) for z in motor_angle_array if z!=[]]
    figure8.add_trace(go.Scatter(x=x0, y=steady_info_time[0], mode='markers', marker_color='Blue', name="Top"))
    figure8.add_trace(go.Scatter(x=x1, y=steady_info_time[0], mode='markers', marker_color='Red', name="Bottom"))
    
    figure9.add_trace(go.Scatter(x=x0, y=steady_info_val[0], mode='markers', marker_color='Blue', name="Top"))
    figure9.add_trace(go.Scatter(x=x1, y=steady_info_val[0], mode='markers', marker_color='Red', name="Bottom"))
    
    figure9.update_layout(title='PF Error of Movement', xaxis_title='Change of Motor Angle (deg)', yaxis_title='Final PF Error (deg)')
    figure8.update_layout(title='Speed of Motor Movement', xaxis_title='Change of Motor Angle (deg)', yaxis_title='Movement Time (s)')
    figure6.update_layout(title='Pose Accuracy and Repeatability', xaxis_title='EV (deg)', yaxis_title='PF (deg)')
    
    #print('counter: ', counter)   
    #figure2.show()  
    #figure5.show()
    #figure6.show()
    figure8.show()
    figure9.show()
    
    angle_dict = {}
    # create for loop for unique values of angle_control_array
    # create dict storage where key is angle_control_array and value is angle_actual_array and angle_motive_array
    #print(angle_control_array)
    missed = 0
    for x,y,z in zip(angle_control_array, angle_actual_array, angle_motive_array):
        if x != []:# and y != []:# and z != []:
            #print(x,y,z)
            x_label = f'{x}'
            
            if x_label not in angle_dict:
                angle_dict[x_label] = {}
                #angle_dict[x_label] = [x,y,z]
                angle_dict[x_label]['control'] = [x]
                angle_dict[x_label]['hall'] = [y]
                angle_dict[x_label]['motive'] = [z]
                #print(angle_dict); exit()
            else:     
                angle_dict[x_label]['control'] = angle_dict[x_label]['control']+[x]
                angle_dict[x_label]['hall'] = angle_dict[x_label]['hall']+[y]
                angle_dict[x_label]['motive'] = angle_dict[x_label]['motive']+[z]
                #print(angle_dict); exit()
        else: missed += 1
    print("missed: ", missed)
    #print(angle_dict)
    # find averages of the values of angle_dict for each key
    for key in angle_dict:
        #print(key)
        #print(angle_dict[key]); print(angle_dict[key]['control']); print(angle_dict[key]['control'][0]); 
        #print([z[0] for z in angle_dict[key]['hall']]); #exit()
        command = [np.mean([z[0] for z in angle_dict[key]['control']]), np.mean([z[1] for z in angle_dict[key]['control']])]
        actual = [np.mean([z[0] for z in angle_dict[key]['hall']]), np.mean([z[1] for z in angle_dict[key]['hall']])]
        actual_sd = [np.std([z[0] for z in angle_dict[key]['hall']]), np.std([z[1] for z in angle_dict[key]['hall']])]
        motive = [np.mean([z[0] for z in angle_dict[key]['motive']]), np.mean([z[1] for z in angle_dict[key]['motive']])]
        #print(command,actual,motive)
        name1 = "Intented Position"
        name2 = "Actual Position"
        # showlegend is False key is not the last of angle_dict
        #print(list(angle_dict.keys())[0])
        if key != list(angle_dict.keys())[-1]: showlegend = False
        else: showlegend = True
        
        figure7.add_trace(go.Scatter(x=[command[1]], y=[command[0]], mode='markers', marker_color='Red', name=name1, legendgroup=name1, showlegend=showlegend))
        figure7.add_trace(go.Scatter(x=[actual[1]], y=[actual[0]], error_x=dict(array=[actual_sd[0]]), error_y=dict(array=[actual_sd[1]]), mode='markers', marker_color='Blue', name=name2, legendgroup=name2, showlegend=showlegend))
        #figure7.add_trace(go.Scatter(x=[motive[0]], y=[motive[1]], mode='markers', marker_color='Purple'))
    
    figure7.update_layout(title='Pose Precision and Repeatability', xaxis_title='EV (deg)', yaxis_title='PF (deg)')
    
    figure7.show()
        
    
    #figure2 = go.Figure()
    #figure3.show()     
    #print(steady_info_time); #break
    print("Average, sd, max times to steady state:", np.mean(steady_info_time[0]),',', np.std(steady_info_time[0]), max(steady_info_time[0]), "seconds")
    print("Average absolute error and its sd for steady state:", np.mean(steady_info_val[0]),',', np.std(steady_info_val[0]), "degrees")
    print("Average and sd times to 95% rise time:", np.mean(move_time_95[0]),',', np.std(move_time_95[0]), "seconds\n")

    print("Average and sd times to steady state:", np.mean(steady_info_time[1]),',', np.std(steady_info_time[1]), "seconds")
    print("Average absolute error and its sd for steady state:", np.mean(steady_info_val[1]),',', np.std(steady_info_val[1]), "degrees")
    print("Average and sd times to 95% rise time:", np.mean(move_time_95[1]),',', np.std(move_time_95[1]), "seconds")

    print("Stuck movment number: ", counter,"\n")
    print("Averages and sd for CPU0:", [np.mean(CPU0), np.std(CPU0)], "CPU1:", [np.mean(CPU1), np.std(CPU1)], "CPU2:", [np.mean(CPU2), np.std(CPU2)], "CPU3:", [np.mean(CPU3), np.std(CPU3)])
    print("Average CPU load:", np.mean([CPU0, CPU1, CPU2, CPU3]), "CPU_sd:", np.std([CPU0, CPU1, CPU2, CPU3]))
    print("Average toff:", np.mean(toff), "toff_sd:", np.std(toff))
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




