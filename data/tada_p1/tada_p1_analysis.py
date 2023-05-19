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
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p1"
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\May-19-v1"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
print(files)
topics = ['motor_command','motor_listen']

figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
figure3 = go.Figure()
figure4 = go.Figure()
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
    
def TADA_angle(M1,M2):
    
    # convert motor cmd to angle in rad
    q1 = (M1-0)/567*2*np.pi - 0*np.pi/2 # -141 was homed, 567 is counts per rev
    q5 = (M2-2*567)/567*2*np.pi - 0*np.pi/2 # 1*np.pi/2 for expt1 # 0*np.pi/2 for expt2
    
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
            
    PF = float(180/np.pi*math.atan2(R05[0,2],R05[2,2]))
    EV = float(180/np.pi*math.atan2(R05[1,2],R05[2,2]))
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
    folder = path+'\\'+'short_test\\'#+'data_attempt2\\'
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
        for i,x in enumerate(data1.field_curr_pos1):
            ##for y in data.field_motor2_move:
            ##i+=1
            a,b,c,d = TADA_angle(x,data1.field_curr_pos2[i])
            motor_listen['curr_PF'].append(a) 
            motor_listen['curr_EV'].append(b)
            motor_listen_new['curr_PF'].append(a) 
            motor_listen_new['curr_EV'].append(b)
            motor_listen['q1'].append(c) 
            motor_listen['q5'].append(d)
        #    ##print(i)

        ##data2 = pd.read_csv(folder+'EXPT2_reduced.csv')
        #data2 = pd.read_csv(folder+'motive_data_quat.csv') # motive_data.csv
        ###print(data2)

        #time2 = data2.Time - 3.2#-11.3#6.6

        #for i,item in enumerate(data2.Time):
        #    #x,y,z = data2.X[i], data2.Y[i], data2.Z[i]
        #    x,y,z = euler_from_quaternion(data2.X[i], data2.Y[i], data2.Z[i], data2.W[i])
        ##    #if i == 0:offset = -x/np.pi*180
        #    motive['rot_X'].append(x/np.pi*180-5.7)#12.6)
        #    motive['rot_Y'].append(y/np.pi*180+5.9)
        #    motive['rot_Z'].append(z/np.pi*180-5.15)
        #    #motive['rot_X'].append(x-5.7)#12.6)
        #    #motive['rot_Y'].append(y)
        #    #motive['rot_Z'].append(z-5.15)

                # specify the figure lines with time as x and motor cmd and listen as y
        figure.data = []

        figure.add_trace(go.Scatter(x=time, y=motor_cmd['m1_cmd'], mode='lines', name='motor1_cmd')) # adding markers slows down the rendering
        figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos1'], mode='lines', name='curr_pos of motor1'))
        figure.add_trace(go.Scatter(x=time, y=motor_cmd['m2_cmd'], mode='lines', name='motor2_cmd')) # adding markers slows down the rendering
        figure.add_trace(go.Scatter(x=time1, y=motor_listen['curr_pos2'], mode='lines', name='curr_pos of motor2'))
        figure.show()

        #figure2.add_trace(go.Scatter(x=time2, y=motive['rot_X'], mode='lines', name='rot_X of motive')) 
        #figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Y'], mode='lines', name='rot_Y of motive'))
        #figure2.add_trace(go.Scatter(x=time2, y=motive['rot_Z'], mode='lines', name='rot_Z of motive'))
        figure2.add_trace(go.Scatter(x=time, y=motor_cmd['PF_cmd'], mode='lines', name='PF_cmd'))
        figure2.add_trace(go.Scatter(x=time, y=motor_cmd['EV_cmd'], mode='lines', name='EV_cmd'))
        #figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
        #figure2.add_trace(go.Scatter(x=time1, y=motor_listen['curr_EV'], mode='lines', name='curr_EV'))
        # add title
        figure2.update_layout(title_text=f'{folder[:-1]}')
        #figure2.show()
        figure2 = go.Figure()

        figure1.add_trace(go.Scatter(x=time, y=motor_cmd['PF_cmd'], mode='lines', name='PF_cmd')) # adding markers slows down the rendering
        figure1.add_trace(go.Scatter(x=time1, y=motor_listen['curr_PF'], mode='lines', name='curr_PF'))
        #figure1.add_trace(go.Scatter(x=time, y=motor_listen['q1'], mode='lines', name='q1')) # adding markers slows down the rendering
        #figure1.add_trace(go.Scatter(x=time1, y=motor_listen['q5'], mode='lines', name='q5'))
        figure1.add_trace(go.Scatter(x=time, y=motor_cmd['EV_cmd'], mode='lines', name='EV_cmd')) # adding markers slows down the rendering
        figure1.add_trace(go.Scatter(x=time1, y=motor_listen['curr_EV'], mode='lines', name='curr_EV'))
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
        figure4.show()
        #figure4 = go.Figure()
        #exit()

        
        # create lists for all topics that creates regions of time based on trial selector where the cmds are not 0
        all_metrics = [motor_cmd, motor_listen]#, motive], motor_listen
        all_time = [time, time1]#, time2]
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
    #folder = 'P10_I1000_S50\\'
    #chosen_topic_array = ['PF_cmd', 'EV_cmd', 'curr_PF', 'curr_EV']
    # Open pickle file for region data
    
    for file in files:
        folder = f'{file[:-4]}\\'
        print(folder)#; break
        
        with open(path+'\\'+folder+'region_motor.pickle', 'rb') as handle: # region_motor_all, region_angle_accurray, region_motor_quat
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
            
            for x, region in enumerate(regions):
            
                # region[0] refers to cmds and [1] refers to listen
                metric_cmd = region[0]['PF_cmd']
                PF_command = metric_cmd[2] # 0 is PF for metric[0]
                time_list = [z for z in metric_cmd[1]]# need to split up panda
                name_ind = metric_cmd[0].find('PF =')
                name = metric_cmd[0][name_ind:]   
            
                metric_actual = region[1]['curr_PF']
                PF_actual = metric_actual[2] # 0 is PF for metric[0]             
                #metric_motive = region[1]['rot_Z']
                #PF_motive = metric_motive[2] # 0 is PF for metric[0]  
            
                metric_CPU0 = region[0]['CPU0']
                metric_CPU1 = region[0]['CPU1']
                metric_CPU2 = region[0]['CPU2']
                metric_CPU3 = region[0]['CPU3']
                CPU0 = metric_CPU0[2] 
                CPU1 = metric_CPU1[2] 
                CPU2 = metric_CPU2[2] 
                CPU3 = metric_CPU3[2] 
            
                #metric_toff = region[1]['t_off']
                #toff = metric_toff[2]            
            
                # use list comprehension to find the difference of each item of two lists: values_list[1] and values_list[0] and create a new list
                #print(len(time_list), len(PF_command), len(PF_actual))
                min_list_length = min(100, len(time_list), len(PF_command), len(PF_actual)) # PF_actual ensure resulting list is as long as the min length of each list or 100 (1 sec)
                diff = [PF_command[i] - PF_actual[i] for i in range(min_list_length)]
                #diff_motive = [PF_command[i] - PF_motive[i] for i in range(min_list_length)]

                i = 0
                # find movement time by searching for a change of value starting at the end of the diff arrays
                offset = 10
                steady_time = [0,0]
                steady_val = [0,0]
                dist_trav = [0,0]
                first = 0
            
                # For hall sensors and motive
                movements = [diff]#,diff]#, diff_motive]
                for i, movement in enumerate(movements):
                    prev_val = 0
                    #first = 0
                    for val, t in zip(movement[offset:], time_list[offset:min_list_length]):
                        #approx_val = round(val, 2)
                        approx_val = val
                        difference = abs(approx_val - prev_val)
                        # find start time when approx val changes value and end time when it stops being equal to approx_val
                        if abs(approx_val) < 0.25 and difference < 0.25: # change in error in degrees
                            steady_time[i] = [t]
                            steady_val[i] = [val]
                            dist_trav[i] = [abs(movement[0])]
                            steady_info_time[i].append(t)
                            steady_info_val[i].append(abs(val)) 
                            steady_info_displacement[i].append(dist_trav[i])
                            #print(steady_val[i])
                            break
                        
                        # need to complete
                        elif abs(approx_val) > 0.25 and difference < 0.01 and first==0:
                            steady_time[i] = [t]
                            steady_val[i] = [val]
                            dist_trav[i] = [abs(movement[0])]
                            steady_t = t
                            stedy_value = abs(val)
                            steady_disp = dist_trav[i]
                            first = 1
                        
                        # t is equal to last item of time_list
                        elif t==time_list[min_list_length-1]:
                            steady_time[i] = [t]
                            steady_val[i] = [val]
                            dist_trav[i] = [abs(movement[0])]
                            
                            if first!=0:
                                steady_info_time[i].append(steady_t)
                                steady_info_val[i].append(stedy_value) 
                                steady_info_displacement[i].append(steady_disp)
                            else:
                                steady_info_time[i].append(t)
                                steady_info_val[i].append(abs(val)) 
                                steady_info_displacement[i].append(dist_trav[i])
                                first = 0
                            #print(steady_val[i])
                            break
                        else: pass
                        prev_val = approx_val
                        #i+=1
                #print(steady_time, steady_val)
                #print(diff)
                #print(x, name)  
                # go to the next item of the list, colors
                #color = colors[color_ind_array[x]]
                #other_color = other_colors[color_ind_array[x]]
                try:
                    figure2.add_trace(go.Scatter(x=time_list,y=movements[0], mode='lines', name=name, legendgroup=name))#, marker_color=color)) # name, 'hall_sensors'
                    figure2.add_trace(go.Scatter(x=steady_time[0],y=steady_val[0], mode='markers', name=name, legendgroup=name))#, marker_color=other_color)) # name, 'hall_sensors'
                    
                except: pass
                #figure4.add_trace(go.Scatter(x=steady_time,y=dist_trav, mode='markers', name=name, legendgroup=name, marker_color=color)) # name, 'hall_sensors'
                #figure3.add_trace(go.Scatter(x=time_list,y=diff_motive, mode='lines', name=name, legendgroup=name, marker_color=color)) # 'motive'
                 #something in the below line is causing the error due to the length of the arrays or some error in the detector
                #figure3.add_trace(go.Scatter(x=steady_time[1],y=steady_val[1], mode='lines', name=name, legendgroup=name, marker_color=other_color)) # 'motive'
                #break
        figure2.show()  
        figure2 = go.Figure()
        #figure3.show() 
        #figure4.show()
        #print(steady_info_time); #break
        print("Average and sd times to steady state:", np.mean(steady_info_time[0]),',', np.std(steady_info_time[0]), "seconds")
        print("Average absolute error and its sd for steady state:", np.mean(steady_info_val[0]),',', np.std(steady_info_val[0]), "degrees")
        print("Averages and sd for CPU0:", [np.mean(CPU0), np.std(CPU0)], "CPU1:", [np.mean(CPU1), np.std(CPU1)], "CPU2:", [np.mean(CPU2), np.std(CPU2)], "CPU3:", [np.mean(CPU3), np.std(CPU3)])
        print("Average CPU load:", np.mean([CPU0, CPU1, CPU2, CPU3]), "CPU_sd:", np.std([CPU0, CPU1, CPU2, CPU3]))
        #print("Average toff:", np.mean(toff), "toff_sd:", np.std(toff))
        #exit() 
        #
        # Average and sd times to steady state: 0.32458639705882353 , 0.28493547307365363 seconds
        # Average absolute error and its sd for steady state: 0.9858418024542115 , 2.421143594760132 degrees
        # Averages and sd for CPU0: [2.3366337011356166, 4.712690390412716] CPU1: [14.383168551001217, 26.100617135281787] CPU2: [7.464356620713036, 8.084266641278454] CPU3: [0.9009901367791812, 2.717945430250144]
        # Average CPU load: 6.271287252407263 CPU_sd: 14.89749880387883                      


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




