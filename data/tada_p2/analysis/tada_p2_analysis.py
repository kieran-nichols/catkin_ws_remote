import subprocess
import os
import pandas as pd
import os
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from plotly.colors import sequential, n_colors
from scipy.signal import find_peaks
from scipy import integrate
import time
from plotly.subplots import make_subplots
import types
import pickle
import warnings
import math
#import matplotlib.pyplot as plt
#from scipy.signal import butter, lfilter, freqz
#from scipy.signal import find_peaks
from scipy import signal
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from scipy import integrate
from scipy import stats

colors = n_colors('rgb(0, 255, 255)', 'rgb(0, 0, 255)', 255, colortype = 'rgb')
color_rgb = ['Red', 'Green', 'Blue']

def TADA_angle(M1,M2):
    
    # convert motor cmd to angle in rad
    q1 = (M1-160)/567*2*np.pi - 0*np.pi/2 # -141 was homed, 567 is counts per rev
    q5 = (M2-0)/567*2*np.pi - 0*np.pi/2 # 1*np.pi/2 for expt1 # 0*np.pi/2 for expt2
    
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

# find all files with '.bag' in name
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p2\subj1"
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p2\subj2_new"
path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\tada_p2\subj3"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
topics = ['angular_moments','europa_topic', 'linear_moments', 'motor_command', 'sensing_topic', 'xsens_joint_angle', 'xsens_com']
#colors = ['red', 'blue', 'green']

figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
figure3 = go.Figure()
figure4 = make_subplots(rows=1, cols=2, shared_xaxes=True, vertical_spacing=0.15, horizontal_spacing=.1, subplot_titles=("Peak Pylon Moments", "Pylon Impulses"))
figure5 = go.Figure()
figure6 = go.Figure()
figure7 = go.Figure()
figure8 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.15, horizontal_spacing=0.009)
figure10 = go.Figure()
figure11 = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.15, horizontal_spacing=0.009)
figure12 = go.Figure()
#figure11 = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.15, horizontal_spacing=0.009)
#figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 
figure_polar1 = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)

color_dict = dict(zip(['slow', 'med', 'fast'], colors))
moments = {'mx':[], 'my':[], 'fz':[]}
imu_data = {'gyro_z':[], 'state':[]}
linear_moments = {'foot_vert_vel':[]}
motor_command = {'PF_cmd':[], 'EV_cmd':[], 'valid':[]}#, 'm1_cmd':[], 'm2_cmd':[], 'CPU0':[], 'CPU1':[], 'CPU2':[], 'CPU3':[]}
xsens_joint_angle = {'hip_sag':[], 'knee_sag':[], 'ankle_sag':[]}
xsens_com = {'com_pos_x':[], 'com_pos_y':[], 'com_pos_z':[]}
files = [f for f in os.listdir(path) if f.endswith('.bag')]

#step = 5
# ask user for input
step = int(input("Enter step number: "))

# convert the rosbag to csv files that are based on topics
if step==0:
    #    ## loop through files
    for file in files:
        # create folder using subprocess
        reduced_file_name = file[:-4]
        print(reduced_file_name)        
        subprocess.run('mkdir {}'.format(path+'\\'+reduced_file_name), capture_output=True, text=True, shell=True)
        # loop through each topic
        for topic in topics:
            print("rostopic echo -b {} -p /{} > {}\{}.csv".format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic))
            subprocess.run('rostopic echo -b {} -p /{} > {}\{}.csv'.format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic), capture_output=True, text=True, shell=True)

    # for files that need combining
    #all_filenames = ['\\subj1_med','\\subj1_med_after','\\subj1_med_3.5_n135']
    #comb_name = 'subj1_med_comb'
    #subprocess.run('mkdir {}'.format(path+'\\'+comb_name), capture_output=True, text=True, shell=True)
    #for topic in topics:
    #    #combine all files for a topic
    #    #print(path+'\\subj1_med'+'\\'+topic+'.csv')
    #    combined_csv = pd.concat([pd.read_csv(path+f+'\\'+topic+'.csv') for f in all_filenames])
    #    #export to csv
    #    combined_csv.to_csv( path+f'\{comb_name}\{topic}.csv', index=False, encoding='utf-8-sig')
   
# read all csv files, store them in dictionaries, find the regions of time where TADA angle is non-neutral, and plot the topics for each TADA angle
elif step==1: 
    ########################################
    #topics = [moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments]
    #folder_name = path+'\\'+'subj1_fast\\' #subj1_med_comb
    #folder_name = path+'\\'+'subj2_new_fast\\' #subj1_med_comb
    folder_name = path+'\\'+'subj3_fast\\' #subj1_med_comb

    # Read motor cmd data from csv
    data2 = pd.read_csv(folder_name+'motor_command.csv')
    data2.columns = data2.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time2 = data2.field_t - data2.field_t[0]
    #motor_command['m1_cmd'] = data2.field_motor1_move/567*360
    #motor_command['m2_cmd'] = data2.field_motor2_move/567*360
    motor_command['PF_cmd'], motor_command['EV_cmd'] = data2.field_PF_cmd, data2.field_EV_cmd
    motor_command['valid'] = data2.field_valid
    #print(motor_command['PF_cmd'])
    #motor_command['CPU0'], motor_command['CPU1'], motor_command['CPU2'], motor_command['CPU3'] = data2.field_CPU0, data2.field_CPU1, data2.field_CPU2, data2.field_CPU3  
    
    # Read europa data
    data = pd.read_csv(folder_name+'europa_topic.csv')
    data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    #print(data)
    time = data.field_t - data2.field_t[0] - 2
    #print(data.field_t[0])
    # correct the values and normalize to body mass = 64.8 kg
    moments['mx'] = [z/19.38/64.8 for z in data.field_mx]
    moments['my'] = [z/20.24/64.8 for z in data.field_my]
    moments['fz'] = data.field_fz # need to finalize this correction factor
    
    # read imu data
    data1 = pd.read_csv(folder_name+'sensing_topic.csv')
    data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time1 = data1.field_t - data2.field_t[0]
    #print(data1)
    imu_data['gyro_z'] = data1.field_gyro_z
    imu_data['state'] = data1.field_state       
 
        
    ## Read xsens joint angle data from csv # taking the time offset from windows data since the offset is different to linux topics
    data3 = pd.read_csv(folder_name+'xsens_joint_angle.csv')
    data3.columns = data3.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time3 = data3.field_data0 - data2.field_t[0] #data3.field_data0[0]# + 28302.41254 # - data.field_t[0]
    #print(data3.field_data0[0])
    xsens_joint_angle['hip_frontal_right'] = data3.field_data3
    xsens_joint_angle['knee_frontal_right'] = data3.field_data8
    xsens_joint_angle['ankle_frontal_right'] = data3.field_data13
    xsens_joint_angle['hip_sag_right'] = data3.field_data5
    xsens_joint_angle['knee_sag_right'] = data3.field_data10
    xsens_joint_angle['ankle_sag_right'] = data3.field_data15
        
    ## Read xsens com data from csv # taking the time offset from windows data since the offset is different to linux topics
    data4 = pd.read_csv(folder_name+'xsens_com.csv')
    data4.columns = data4.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time4 = data4.field_data0 - data2.field_t[0] #data4.field_data0[0]#+ 28302.41254
    xsens_com['com_pos_x'] = data4.field_data1
    xsens_com['com_pos_y'] = data4.field_data2
    xsens_com['com_pos_z'] = data4.field_data3
    xsens_com['com_vel_x'] = data4.field_data4
    xsens_com['com_vel_y'] = data4.field_data5
    xsens_com['com_vel_z'] = data4.field_data6
        
    ## Read linear moments data from csv # taking the time offset from windows data since the offset is different to linux topics
    data5 = pd.read_csv(folder_name+'linear_moments.csv')
    data5.columns = data5.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time5 = data5.field_data0 - data2.field_t[0] #data5.field_data0[0] + 28302.41254
    linear_moments['foot_vert_vel'] = data5.field_data16   
    
            ## Show entire time series for data of interest; Plot entire experiment
    # Future goal to plot the below graph using a for loop with the region variable allowing for much less written code
    figure.add_trace(go.Scatter(x=time, y=moments['mx'], mode='lines', name='Mx'))
    figure.add_trace(go.Scatter(x=time, y=moments['my'], mode='lines', name='My'))
    #figure.add_trace(go.Scatter(x=time, y=moments['fz'], mode='lines', name='Fz'))

    figure.add_trace(go.Scatter(x=time1, y=imu_data['gyro_z'], mode='lines', name='gyro_z'))
    figure.add_trace(go.Scatter(x=time1, y=imu_data['state']*10, mode='lines', name='state'))

    #figure.add_trace(go.Scatter(x=time2, y=motor_command['m1_cmd'], mode='lines', name='motor1_cmd (deg)')) # adding markers slows down the rendering
    #figure.add_trace(go.Scatter(x=time2, y=motor_command['m2_cmd'], mode='lines', name='motor2_cmd (deg)')) 
    figure.add_trace(go.Scatter(x=time2, y=motor_command['PF_cmd'], mode='lines', name='PF_cmd'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['EV_cmd'], mode='lines', name='EV_cmd'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU0'], mode='lines', name='CPU0'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU1'], mode='lines', name='CPU1'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU2'], mode='lines', name='CPU2'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU3'], mode='lines', name='CPU3'))

    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_sag_right'], mode='lines', name='hip_sag_right'))
    figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_sag_right'], mode='lines', name='knee_sag_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_sag_right'], mode='lines', name='ankle_sag_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_frontal_right'], mode='lines', name='hip_frontal_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_frontal_right'], mode='lines', name='knee_frontal_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_frontal_right'], mode='lines', name='ankle_frontal_right'))

    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_x'], mode='lines', name='com_pos_x'))
    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_y'], mode='lines', name='com_pos_y'))
    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_z'], mode='lines', name='com_pos_z'))

    #figure.add_trace(go.Scatter(x=time5, y=linear_moments['foot_vert_vel'], mode='lines', name='foot_vert_vel'))

    figure.update_layout(title='All data', xaxis_title='Time (s)', yaxis_title='Value')
    figure.show(); exit()
        
    ########################################
    # TADA_angle finder (10 steps); in this dataset, the TADA angle changes, the persons walks about 10 steps, then the TADA angles changes back to 0,0

    # create lists for all topics that creates regions of time based on trial selector where the cmds are not 0
    all_metrics = [moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments] # there seems to be some issues with time of linear_moments
    all_time = [time, time1, time2, time3, time4, time5]
    topic_individual_dict = {}
    region = []
    regions = []
        
    # create topic regions that are lists of [angle_title, PF, EV, moments, imu_data, motor_command, xsens_joint_angle, xsens_com, linear_moments]
    # where each region is a list of [time, data] and data is a dictionary of topics
        
    # # Find the changes in PF and EV and its respective start and end times; for PF, search motor_command['PF_cmd'] for all indices larger than 2 then save index
    trial_selector = []
    start_info={'start_time':[], 'start_index':[], 'PF':[], 'EV':[]}
    prev_val = [0,0]
    region = [{'TADA_angle':[]}]

    for i, val in enumerate(zip(motor_command['PF_cmd'],motor_command['EV_cmd'])): # add EV processing
        #print(val)
        approx_val = [round(val[0], 2), round(val[1], 2)]
        diff_pf = abs(approx_val[0] - prev_val[0])
        diff_ev = abs(approx_val[1] - prev_val[1])
        # find start time when approx val changes value and end time when it stops being equal to approx_val
        #if approx_val>0.1 or approx_val < -0.1 
        if  diff_pf > 0.1 or diff_ev > 0.1: 
            start_time = time2[i]
            start_info['start_time'].append(start_time)
            start_info['start_index'].append(i)
            start_info['PF'].append(approx_val[0])
            start_info['EV'].append(approx_val[1])
        prev_val = approx_val
    print(start_info)
    #exit()

    # loop through all start times in start_info minus 1
    for i, start_time in enumerate(start_info['start_time']):
        angle_title = 'PF = ' + str(start_info['PF'][i]) + ', EV = ' + str(start_info['EV'][i])
        print(angle_title)
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
                list_of_time = []
                last_time = [0,0]
                #print(topic[0])
                # find the region that is within the start and end time
                for q, q_val in enumerate(topic[1]):
                    #for l, value1 in enumerate(q_val):
                    #print(q, q_val)
                    #if q >= start_index and q <= end_index:
                    #try: # decided to ignore some errors from the below line
                    topic_time = all_time[j][q]
                    if topic_time >= start_time and topic_time <= end_time:# and motor_command['valid'][q]:
                        list_of_values.append(q_val)
                        list_of_time.append(topic_time-start_time)
                #        last_time = [q, topic_time]
                        
                #    # conditional statement if the end time is not valid then create an end time that is valid; valid means the experiment is not paused
                #    if last_time[1] < end_time: 
                #        end_index = last_time[0]
                #        start_index = start_info['start_index'][i]
                #    #except: pass
                ##list_of_time = all_time[j][start_index:end_index] #- all_time[j][start_index]
                #print(start_index,end_index,len(all_time[j]))
                #try: # some errors seem to pop up with this time calculation
                #    list_of_time = all_time[j][start_index:end_index] - all_time[j][start_index] # set all chunks to have an initial time of 0
                #except:
                #    list_of_time = []
                #    list_of_values = []
                #    print("issue")
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
    figure1.update_layout(title='Multiple Metrics vs Time', xaxis_title='Time (s)', yaxis_title='Metric', legend_title="Grouped by Metric")
    figure1.show()
    #exit()
    
    ## Save region data to a pickle file
    with open(folder_name+'region_all.pickle', 'wb') as handle: # region_motor_all, region_angle_accurray
        pickle.dump(regions, handle, protocol=pickle.HIGHEST_PROTOCOL)       
            
        ########################################
elif step==2:
    # OR Sofya, you can instead process the peak finder here (focus on pylon moment, ang vel of shank, CM forward vel, foot segment pos and vel, hip/knee/ankle angles)
    # Add the peaks of the chosen to topic_individual_peaks_dict
    folder_name = path+'\\'+'subj1_med_comb\\'
    
    
    # Open pickle file for region data
    with open(folder_name+'region_all.pickle', 'rb') as handle: #region_all_mini
        regions = pickle.load(handle)
        
    pf_array = []
    ev_array = []
    avg_peak_array = []
    name_array = []
    avg_peak_neutral = []
    direction_array = []
    index = 0
    index_array = []
    pf_ev_array = []
    pf_array_med = []
    ev_array_med = []
    angle_color = []
    chosen_moment_stance = []
    impulse_array = []
    impulse_neutral = []
    chosen_moment_stance_integral = []
    
    # Create break up regions into regions, a region is for a chunck of time
    for x, region in enumerate(regions):
        #print(region[2])
        brain_cmd = region[2]['PF_cmd']
        PF_command = brain_cmd[2] # 0 is PF for metric[0]
        time_cmd = [z for z in brain_cmd[1]]
        valid_cmd = region[2]['valid'][2]
            
        imu = region[1]['gyro_z'] # 1 is IMU
        imu_gyro = imu[2]
        time_imu = [z for z in imu[1]]# need to split up panda
            
        moments = region[0]
        my = moments['my'][2]
        mx = moments['mx'][2]
        fz = moments['fz'][2]
        
        chosen_moment = my
        
        if chosen_moment == mx: 
            chosen_moment_label = 'Frontal Moment'
            time_m = [z for z in moments['mx'][1]]
            sizing =  300 # 10, 30
            height = 0.14
        elif chosen_moment == my: 
            chosen_moment_label = 'Sagittal Moment'
            time_m = [z for z in moments['my'][1]]
            sizing = 125 # 10, 30
            height = 0.5
        elif chosen_moment == fz: chosen_moment_label = 'Axial Force'

        # low pass filter for chosen moment
        sos = signal.butter(2, 6, 'lp', fs=100, output='sos')
        filtered = signal.sosfilt(sos, chosen_moment)
        
        chosen_moment = []
        chosen_moment = [z for z in filtered]
        
        name_ind = brain_cmd[0].find('PF =')
        name = brain_cmd[0][name_ind:]   
        print(name)
        
        #if name in ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']:
        #print(my); print(time_my); break
        
        all_peaks, _ = find_peaks(chosen_moment, height=height, distance=50)
        print(all_peaks)
        #print(len(all_peaks))
        # pick the middle three peaks peaks if there are more than 2 peaks
        if len(all_peaks) > 2:
            peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
        #elif all_peaks == None or math.isnan(all_peaks): peaks = [0]
        else: peaks = all_peaks
        #peaks = all_peaks[0:1+min(2,len(all_peaks))]
        #peaks = all_peaks
        print(peaks)
        print(len(time_m))
        peaks_time = [time_m[z] for z in peaks]
        peaks_array = [chosen_moment[z] for z in peaks]

        if len(peaks) > 2:
                first_ind = peaks[0] - 50
                if first_ind < 0: first_ind=0
                second_ind = peaks[1] + 50
                last_ind = peaks[len(peaks)-1] + 50
                print(first_ind, second_ind, last_ind)
                print(len(chosen_moment), len(time_m))
                #print(chosen_moment,time_m[first_ind:last_ind]); exit()
                #try:
                chosen_moment_stance_integral = integrate.cumtrapz(chosen_moment[first_ind:last_ind], time_m[first_ind:last_ind], initial=0)
                #print(chosen_moment_stance_integral); exit()
                #except: chosen_moment_stance_integral = [0]
                chosen_moment_stance_integral_val = chosen_moment_stance_integral[len(chosen_moment_stance_integral)-1]/len(peaks)
        else: chosen_moment_stance_int = 0
        
        # ignore warnings for nanmean
        #with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        try:
            avg_peak = np.nanmean(peaks_array)
        except: 
            avg_peak = 0
        #print(avg_peak)
        if math.isnan(avg_peak): avg_peak = 0
        elif avg_peak == float('nan'): avg_peak = 0
        #print(avg_peak)
            
        
        name_array.append(name)
        pf = float(name[name.find('PF =')+4:name.find(',')])
        ev = float(name[name.find('EV = ')+4:])
        #print(pf, ev)
            
        #print(time_cmd)
        #print(PF_command)
        #print(time_imu)
        #print(imu_gyro)
        chosen_angles = ['PF = 5.0, EV = 0.0', 'PF = -0.0, EV = 5.0', 'PF = -5.0, EV = 0.0', 'PF = 0.0, EV = -5.0','PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']
        chosen_angles_10 = ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']
            
        # sample graph to check variables
        #figure3.add_trace(go.Scatter(x=time_imu,y=imu_gyro, mode='lines', name=name))
        if name != 'PF = 0.0, EV = 0.0': # name in chosen_angles:
            #figure3.add_trace(go.Scatter(x=time_my, y=my, mode='lines', name=name))
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            #print([mx[z] for z in peaks])
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name)) 
            index+=1
            index_array.append(index)            
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            #avg_peak = 0.1
            #figure4.add_trace(go.Scatter(x=[ev], y=[pf], mode='markers', marker=dict(size=abs(0.1*int(avg_peak)), color=abs(0.1*int(avg_peak)), colorscale='Viridis', showscale=True), name=name))
            if (ev,pf) not in zip(ev_array,pf_array):
                pf_array.append(pf)
                ev_array.append(ev)
                pf_ev_array.append([ev,pf])
                avg_peak_array.append((avg_peak))
                impulse_array.append((chosen_moment_stance_integral_val)) 
                
                # cartesian to polar
                #r = math.sqrt(pf**2 + ev**2)
                theta = math.atan2(pf,ev)
                direction = 180/np.pi*theta
                direction_array.append(direction)
                if name in chosen_angles_10: angle_color.append('red')
                else: angle_color.append('blue')
            else:
                ind = pf_ev_array.index([ev,pf]) 
                #print(ind,[ev,pf],pf_ev_array)
                avg_peak_array[ind] = (avg_peak_array[ind] + (avg_peak))/2
                impulse_array[ind] = (impulse_array[ind] + (chosen_moment_stance_integral_val))/2
        
        elif name == 'PF = 0.0, EV = 0.0' and len(all_peaks)<6:# and valid_cmd: # neutral walking trials with around 10 steps
            #print(valid_cmd)
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            avg_peak_neutral.append((avg_peak))  
            impulse_neutral.append((chosen_moment_stance_integral_val))
                #first = peaks[0]; second = peaks[1]
                #if name == 'PF = 0.0, EV = -5.0':
                #    print("worked")
                #    figure7.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first_ind:last_ind]], y=chosen_moment[first_ind:last_ind], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                #    figure7.add_trace(go.Scatter(x=[z-peaks_time[0] for z in peaks_time], y=peaks_array, mode='markers', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                #    figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first:second]], y=xsens_sag_hip_angle[first:second], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1],marker_color=color_rgb[speed],showlegend=False),1,1) 
                #    figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first:second]], y=xsens_sag_knee_angle[first:second], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1],marker_color=color_rgb[speed],showlegend=True),2,1) 
                #    #figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first_ind:second_ind]], y=xsens_sag_ankle_angle[first_ind:second_ind], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1]),3,1) 

                #print("found")
 
    pf_array.append(0.0); ev_array.append(0.0); avg_peak_array.append(np.nanmean(avg_peak_neutral)) # to add all neutral to the mix
    impulse_array.append(np.nanmean(impulse_neutral))
   
        #
    #print(avg_peak_neutral)
    
    # remapping theta to ankle angle names
    polar_moments_red = []; polar_impulses = []; direction_names_blue = [];  polar_moments_blue = []; direction_names_red = []; 
    polar_moments_red_sorted = []; polar_moments_blue_sorted = []; direction_names_red_sorted = []; direction_names_blue_sorted = [];
    polar_impulses_red = []; polar_impulses_blue = []; polar_impulses_red_sorted = []; polar_impulses_blue_sorted = [];
    dummy = 0
    direction_name = ['Inversion', 'Plantarflexion', 'Eversion' , 'Dorsiflexion','Inversion']
    order = [0,90,180,-90, 0]
    #print(direction_array, avg_peak_array); #exit()
    
    #for i,z in enumerate(angle_color):
    #    if z=='red':
    #        polar_moments_red.append(avg_peak_array[i])
    #        polar_impulses_red.append(impulse_array[i])
    #        direction_names_red.append(direction_array[i])
    #    else:
    #        polar_moments_blue.append(avg_peak_array[i])
    #        polar_impulses_blue.append(impulse_array[i])
    #        direction_names_blue.append(direction_array[i])
    
    #for i,z in enumerate(order):
    #    sort_ind = direction_names_red.index(z)
    #    polar_moments_red_sorted.append(polar_moments_red[sort_ind])
    #    polar_impulses_red_sorted.append(polar_impulses_red[sort_ind])
    #    direction_names_red_sorted.append(direction_names_red[sort_ind])
        
    #for i,z in enumerate(order):
    #    sort_ind = direction_names_blue.index(z)
    #    polar_moments_blue_sorted.append(polar_moments_blue[sort_ind])
    #    polar_impulses_blue_sorted.append(polar_impulses_blue[sort_ind])
    #    direction_names_blue_sorted.append(direction_names_blue[sort_ind])
            

       
    #print(avg_peak_neutral_array,direction_array_neutral)
    avg_peak_array_neutral = np.nanmean(avg_peak_neutral) # to add all neutral to the mix
    avg_impulses_array_neutral = np.nanmean(impulse_neutral) # to add all neutral to the mix    

        # create color array that is a function of avg_peak_array and does not have 0 as a min
    color = []
    second_min = sorted(set(avg_peak_array))
    for x in (avg_peak_array):#+avg_peak_array_neutral):
        # if x is 0, make x the 2nd smallest value of avg_peak_array
        #if x == 0: x = second_min
        color.append(x)
        
    color1 = []
    second_min = sorted(set(impulse_array))
    for x in (impulse_array):#+avg_impulses_array_neutral):
        # if x is 0, make x the 2nd smallest value of avg_peak_array
        #if x == 0: x = second_min
        color1.append(x)
        
    #print(avg_peak_array_neutral)
    avg_peak_neutral_array = [avg_peak_array_neutral for z in direction_name] #range(360)
    polar_impulses_neutral_array = [avg_impulses_array_neutral for z in direction_name] #range(360)
    #direction_array_neutral = np.linspace(0,360,361)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_blue_sorted, theta=direction_name, mode='markers+lines',marker_color='blue', name="5 deg"),1,1)
    #print("5 deg inf:",avg_peak_array,direction_array)
    figure_polar1.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_name, mode='lines', line_width = 3, name='Neutral'),1,1)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_red_sorted, theta= direction_name, marker_color='red', mode='markers+lines', name="10 deg"),1,1)
    
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_blue_sorted, theta=direction_name, mode='markers+lines',marker_color='blue', name="5 deg"),1,2)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_neutral_array, theta= direction_name, mode='lines', line_width = 3, name='Neutral'),1,2)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_red_sorted, theta= direction_name, marker_color='red', mode='markers+lines', name="10 deg"),1,2)
    #print(polar_moments,direction_array)
    #figure4.add_trace(go.Scatter(x=ev_array_med+ev_array, y=pf_array_med+pf_array, mode='markers', text=avg_peak_array_med+avg_peak_array, marker=dict(size=[z/sizing for z in avg_peak_array_med+avg_peak_array], color=color1, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'

            #figure3.show()
            #figure4.show()
            
    figure4.add_trace(go.Scatter(x=[-z for z in ev_array], y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[(z-min(avg_peak_array))*sizing+10 for z in (avg_peak_array)], color=color, colorscale=colors, colorbar=dict(title='Peaks:<br>marker size <br>and color', x=-0.15), showscale=True )),1,1) #'Viridis'
    figure4.add_trace(go.Scatter(x=[-z for z in ev_array], y=pf_array, mode='markers', text=impulse_array, marker=dict(size=[(z-min(impulse_array))*sizing+10 for z in (impulse_array)], color=color1, colorscale=colors, colorbar=dict(title='Impulses:<br>marker size <br>and color'), showscale=True)),1,2) #'Viridis'
    
    figure12.add_trace(go.Scatter(x=[-z for z in ev_array], y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[(z-min(avg_peak_array))*sizing+10 for z in (avg_peak_array)], color=color, colorscale=colors, colorbar=dict(title='Peaks:<br>marker size <br>and color'), showscale=True ))) #'Viridis'

    figure_polar.add_trace(go.Scatterpolar(r=polar_moments_red_sorted, theta= direction_array, mode='markers', name=chosen_moment_label+chosen_moment_label[1]))
    figure_polar.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_name, mode='lines', line_width = 5, name='Neutral'))
    
    figure4.update_layout(title=f'PF vs IV with {chosen_moment_label} Moments', xaxis_title='IV', yaxis_title='PF', showlegend=False, font_size=15)
    figure4.update_xaxes(title='IV', row=1, col=2)
    figure4.update_yaxes(title='PF', row=1, col=2)
    figure4.update_yaxes(scaleanchor="x", scaleratio=1)

    figure12.update_layout(title=f'PF vs IV with {chosen_moment_label} Peak Moments', xaxis_title='IV', yaxis_title='PF', showlegend=False, font_size=15)
    figure12.update_yaxes(scaleanchor="x", scaleratio=1)
    
    figure3.update_layout(title=f'{chosen_moment_label} vs Time, with the chosen peaks', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm)', legend_title='Grouped by Angle')
    figure_polar.update_layout(title=f'Polar Plot of the Peaks(left) and Impulses (right) for {chosen_moment_label} vs Ankle Angle', legend_title='Grouped by Angle')
    figure_polar1.update_layout(title=f'Polar Plot of the Peaks(left) and Impulses (right) for {chosen_moment_label} vs Ankle Angle', legend_title='Grouped by Angle')


    figure3.show()
    figure4.show()
    #figure_polar.show()
    #figure_polar1.show()
    figure12.show()

elif step==3:
    # OR Sofya, you can instead process the peak finder here (focus on pylon moment, ang vel of shank, CM forward vel, foot segment pos and vel, hip/knee/ankle angles)
    # Add the peaks of the chosen to topic_individual_peaks_dict
    folder_name = path+'\\'+'subj1_med_comb\\'
    
    
    # Open pickle file for region data
    with open(folder_name+'region_all.pickle', 'rb') as handle: #region_all_mini
        regions = pickle.load(handle)
        
    pf_array = []
    ev_array = []
    avg_peak_array = []
    name_array = []
    avg_peak_neutral = []
    direction_array = []
    index = 0
    index_array = []
    pf_ev_array = []
    pf_array_med = []
    ev_array_med = []
    angle_color = []
    chosen_moment_stance = []
    impulse_array = []
    impulse_neutral = []
    chosen_moment_stance_integral = []
    
    
    # Create break up regions into regions, a region is for a chunck of time
    for x, region in enumerate(regions):
        #print(region[2])
        brain_cmd = region[2]['PF_cmd']
        PF_command = brain_cmd[2] # 0 is PF for metric[0]
        time_cmd = [z for z in brain_cmd[1]]
        valid_cmd = region[2]['valid'][2]
            
        imu = region[1]['gyro_z'] # 1 is IMU
        imu_gyro = imu[2]
        time_imu = [z for z in imu[1]]# need to split up panda
            
        moments = region[0]
        my = moments['my'][2]
        mx = moments['mx'][2]
        fz = moments['fz'][2]
        
        chosen_moment = mx
        
        if chosen_moment == mx: 
            chosen_moment_label = 'Frontal Moment'
            time_m = [z for z in moments['mx'][1]]
            sizing =  300 # 10, 30
            height = 0.14
        elif chosen_moment == my: 
            chosen_moment_label = 'Sagittal Moment'
            time_m = [z for z in moments['my'][1]]
            sizing = 125 # 10, 30
            height = 0.5
        elif chosen_moment == fz: chosen_moment_label = 'Axial Force'

        # low pass filter for chosen moment
        sos = signal.butter(2, 6, 'lp', fs=100, output='sos')
        filtered = signal.sosfilt(sos, chosen_moment)
        
        chosen_moment = []
        chosen_moment = [z for z in filtered]
        
        name_ind = brain_cmd[0].find('PF =')
        name = brain_cmd[0][name_ind:]   
        print(name)
        
        #if name in ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']:
        #print(my); print(time_my); break
        
        all_peaks, _ = find_peaks(chosen_moment, height=height, distance=50)
        print(all_peaks)
        #print(len(all_peaks))
        # pick the middle three peaks peaks if there are more than 2 peaks
        if len(all_peaks) > 2:
            peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
        #elif all_peaks == None or math.isnan(all_peaks): peaks = [0]
        else: peaks = all_peaks
        #peaks = all_peaks[0:1+min(2,len(all_peaks))]
        #peaks = all_peaks
        print(peaks)
        print(len(time_m))
        peaks_time = [time_m[z] for z in peaks]
        peaks_array = [chosen_moment[z] for z in peaks]

        if len(peaks) > 2:
                first_ind = peaks[0] - 50
                if first_ind < 0: first_ind=0
                second_ind = peaks[1] + 50
                last_ind = peaks[len(peaks)-1] + 50
                print(first_ind, second_ind, last_ind)
                print(len(chosen_moment), len(time_m))
                #print(chosen_moment,time_m[first_ind:last_ind]); exit()
                #try:
                chosen_moment_stance_integral = integrate.cumtrapz(chosen_moment[first_ind:last_ind], time_m[first_ind:last_ind], initial=0)
                #print(chosen_moment_stance_integral); exit()
                #except: chosen_moment_stance_integral = [0]
                chosen_moment_stance_integral_val = chosen_moment_stance_integral[len(chosen_moment_stance_integral)-1]/len(peaks)
        else: chosen_moment_stance_int = 0
        
        # ignore warnings for nanmean
        #with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        try:
            avg_peak = np.nanmean(peaks_array)
        except: 
            avg_peak = 0
        #print(avg_peak)
        if math.isnan(avg_peak): avg_peak = 0
        elif avg_peak == float('nan'): avg_peak = 0
        #print(avg_peak)
            
        
        name_array.append(name)
        pf = float(name[name.find('PF =')+4:name.find(',')])
        ev = float(name[name.find('EV = ')+4:])
        #print(pf, ev)
            
        #print(time_cmd)
        #print(PF_command)
        #print(time_imu)
        #print(imu_gyro)
        chosen_angles = ['PF = 5.0, EV = 0.0', 'PF = -0.0, EV = 5.0', 'PF = -5.0, EV = 0.0', 'PF = 0.0, EV = -5.0','PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']
        chosen_angles_10 = ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']
            
        # sample graph to check variables
        #figure3.add_trace(go.Scatter(x=time_imu,y=imu_gyro, mode='lines', name=name))
        if name in chosen_angles:
            #figure3.add_trace(go.Scatter(x=time_my, y=my, mode='lines', name=name))
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            #print([mx[z] for z in peaks])
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name)) 
            index+=1
            index_array.append(index)            
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            #avg_peak = 0.1
            #figure4.add_trace(go.Scatter(x=[ev], y=[pf], mode='markers', marker=dict(size=abs(0.1*int(avg_peak)), color=abs(0.1*int(avg_peak)), colorscale='Viridis', showscale=True), name=name))
            if (ev,pf) not in zip(ev_array,pf_array):
                pf_array.append(pf)
                ev_array.append(ev)
                pf_ev_array.append([ev,pf])
                avg_peak_array.append((avg_peak))
                impulse_array.append((chosen_moment_stance_integral_val)) 
                
                # cartesian to polar
                #r = math.sqrt(pf**2 + ev**2)
                theta = math.atan2(pf,ev)
                direction = 180/np.pi*theta
                direction_array.append(direction)
                if name in chosen_angles_10: angle_color.append('red')
                else: angle_color.append('blue')
            else:
                ind = pf_ev_array.index([ev,pf]) 
                #print(ind,[ev,pf],pf_ev_array)
                avg_peak_array[ind] = (avg_peak_array[ind] + (avg_peak))/2
                impulse_array[ind] = (impulse_array[ind] + (chosen_moment_stance_integral_val))/2
        
        elif name == 'PF = 0.0, EV = 0.0' and len(all_peaks)<6:#6<len(all_peaks)<12: #and valid_cmd: # neutral walking trials with around 10 steps
            #print(valid_cmd)
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            avg_peak_neutral.append((avg_peak))  
            impulse_neutral.append((chosen_moment_stance_integral_val))
                #first = peaks[0]; second = peaks[1]
                #if name == 'PF = 0.0, EV = -5.0':
                #    print("worked")
                #    figure7.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first_ind:last_ind]], y=chosen_moment[first_ind:last_ind], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                #    figure7.add_trace(go.Scatter(x=[z-peaks_time[0] for z in peaks_time], y=peaks_array, mode='markers', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                #    figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first:second]], y=xsens_sag_hip_angle[first:second], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1],marker_color=color_rgb[speed],showlegend=False),1,1) 
                #    figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first:second]], y=xsens_sag_knee_angle[first:second], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1],marker_color=color_rgb[speed],showlegend=True),2,1) 
                #    #figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first_ind:second_ind]], y=xsens_sag_ankle_angle[first_ind:second_ind], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1]),3,1) 

                #print("found")
 
    pf_array.append(0.0); ev_array.append(0.0); avg_peak_array.append(np.nanmean(avg_peak_neutral)) # to add all neutral to the mix
    impulse_array.append(np.nanmean(impulse_neutral))
   
        #
    #print(avg_peak_neutral)
    
    # remapping theta to ankle angle names
    polar_moments_red = []; polar_impulses = []; direction_names_blue = [];  polar_moments_blue = []; direction_names_red = []; 
    polar_moments_red_sorted = []; polar_moments_blue_sorted = []; direction_names_red_sorted = []; direction_names_blue_sorted = [];
    polar_impulses_red = []; polar_impulses_blue = []; polar_impulses_red_sorted = []; polar_impulses_blue_sorted = [];
    dummy = 0
    direction_name = ['Inversion', 'Plantarflexion', 'Eversion' , 'Dorsiflexion','Inversion']
    order = [180,90, 0,-90, 180]
    print(direction_array, avg_peak_array); #exit()
    
    for i,z in enumerate(angle_color):
        if z=='red':
            polar_moments_red.append(avg_peak_array[i])
            polar_impulses_red.append(impulse_array[i])
            direction_names_red.append(direction_array[i])
        else:
            polar_moments_blue.append(avg_peak_array[i])
            polar_impulses_blue.append(impulse_array[i])
            direction_names_blue.append(direction_array[i])
    
    for i,z in enumerate(order):
        sort_ind = direction_names_red.index(z)
        polar_moments_red_sorted.append(polar_moments_red[sort_ind])
        polar_impulses_red_sorted.append(polar_impulses_red[sort_ind])
        direction_names_red_sorted.append(direction_names_red[sort_ind])
        
    for i,z in enumerate(order):
        sort_ind = direction_names_blue.index(z)
        polar_moments_blue_sorted.append(polar_moments_blue[sort_ind])
        polar_impulses_blue_sorted.append(polar_impulses_blue[sort_ind])
        direction_names_blue_sorted.append(direction_names_blue[sort_ind])
            

       
    #print(avg_peak_neutral_array,direction_array_neutral)
    avg_peak_array_neutral = np.nanmean(avg_peak_neutral) # to add all neutral to the mix
    avg_impulses_array_neutral = np.nanmean(impulse_neutral) # to add all neutral to the mix    

        # create color array that is a function of avg_peak_array and does not have 0 as a min
    color = []
    second_min = sorted(set(avg_peak_array))
    for x in (avg_peak_array):#+avg_peak_array_neutral):
        # if x is 0, make x the 2nd smallest value of avg_peak_array
        #if x == 0: x = second_min
        color.append(x)
        
    color1 = []
    second_min = sorted(set(impulse_array))
    for x in (impulse_array):#+avg_impulses_array_neutral):
        # if x is 0, make x the 2nd smallest value of avg_peak_array
        #if x == 0: x = second_min
        color1.append(x)
        
    #print(avg_peak_array_neutral)
    marker_size = 10
    avg_peak_neutral_array = [avg_peak_array_neutral for z in direction_name] #range(360)
    polar_impulses_neutral_array = [avg_impulses_array_neutral for z in direction_name] #range(360)
    #direction_array_neutral = np.linspace(0,360,361)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_blue_sorted, theta=direction_name, mode='markers',marker_color='blue',  marker=dict(size=marker_size), name="5 deg"),1,1)
    #print("5 deg inf:",avg_peak_array,direction_array)
    figure_polar1.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_name, mode='lines', name='Neutral',marker_color='green'),1,1)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_red_sorted, theta= direction_name, marker_color='red', mode='markers',  marker=dict(size=marker_size), name="10 deg"),1,1)
    
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_blue_sorted, theta=direction_name, mode='markers',  marker=dict(size=marker_size), marker_color='blue', name="5 deg",showlegend=False),1,2)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_neutral_array, theta= direction_name, mode='lines', name='Neutral',marker_color='green',showlegend=False),1,2)
    figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_red_sorted, theta= direction_name, marker_color='red',  marker=dict(size=marker_size), mode='markers', name="10 deg",showlegend=False),1,2)
    #print(polar_moments,direction_array)
    #figure4.add_trace(go.Scatter(x=ev_array_med+ev_array, y=pf_array_med+pf_array, mode='markers', text=avg_peak_array_med+avg_peak_array, marker=dict(size=[z/sizing for z in avg_peak_array_med+avg_peak_array], color=color1, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'

            #figure3.show()
            #figure4.show()
            
    figure4.add_trace(go.Scatter(x=[-z for z in ev_array], y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[(z-min(avg_peak_array)+100)/sizing for z in (avg_peak_array)], color=color, colorscale=colors, colorbar=dict(title='Peaks', x=-0.15), showscale=True )),1,1) #'Viridis'
    figure4.add_trace(go.Scatter(x=[-z for z in ev_array], y=pf_array, mode='markers', text=impulse_array, marker=dict(size=[(z-min(impulse_array)+100)/sizing for z in (impulse_array)], color=color1, colorscale=colors, colorbar=dict(title='Impulses  '), showscale=True)),1,2) #'Viridis'
    
    figure_polar.add_trace(go.Scatterpolar(r=polar_moments_red_sorted, theta= direction_array, mode='markers', name=chosen_moment_label+chosen_moment_label[1]))
    figure_polar.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_name, mode='lines', line_width = 5, name='Neutral'))
    
    figure4.update_layout(title=f'PF vs EV, with {chosen_moment_label} Peaks(left) and Impulses (right) as marker color and size', xaxis_title='IV', yaxis_title='PF', xaxis1_title='IV', yaxis1_title='PF', showlegend=False)
    figure4.update_yaxes(scaleanchor="x", scaleratio=1)

    figure3.update_layout(title=f'{chosen_moment_label} vs Time, with the chosen peaks', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm)', legend_title='Grouped by Angle')
    figure_polar.update_layout(title=f'Polar Plot of the Peaks(left) and Impulses (right) for {chosen_moment_label} vs Ankle Angle', legend_title='Grouped by ankle angle')
    figure_polar1.update_layout(title=f'Polar Plot of the Peaks(left) and Impulses (right) for {chosen_moment_label} vs Ankle Angle', legend_title='Grouped by ankle angle')


    #figure3.show()
    figure4.show()
    #figure_polar.show()
    figure_polar1.show()
    
    data = [[-z for z in ev_array],pf_array,avg_peak_array,impulse_array]
    print(data)
    
    with open(path+'\\results_step2_frontal.pickle', 'wb') as handle: 
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
elif step==6:
    
    with open(path+'\\results_step2_sagittal.pickle', 'rb') as handle: #results_step2_sagittal.pickle'
        data = pickle.load(handle)
    print(data)
    ev_array = data[0]
    pf_array = data[1]
    avg_peak_array = data[2]
    impulse_array = data[3]

    peaks_ev = []
    peaks_pf = []
    impulses_ev = []
    impulses_pf = []
    pf_arr = []
    ev_arr = []
        
    for x,y,a,b in zip(ev_array,pf_array,avg_peak_array,impulse_array):
        if x==0: # plot PF
            #print(x,y)
            peaks_pf.append(a)
            impulses_pf.append(b)
            pf_arr.append(y)
            #figure10.add_trace(go.Scatter(x=[y], y=[a], mode='markers', marker=dict(size=10, color='red'), showlegend=True))
            #figure10.add_trace(go.Scatter(x=[y], y=[b], mode='markers', marker=dict(size=10, color='blue'), showlegend=True))
        elif y==0: # plot EV
            #print(x,y)
            peaks_ev.append(a)
            impulses_ev.append(b)
            ev_arr.append(x)
            #figure10.add_trace(go.Scatter(x=[x], y=[a], mode='markers+lines', marker=dict(size=10, color='darkred'), showlegend=True))
            #figure10.add_trace(go.Scatter(x=[x], y=[b], mode='markers+lines', marker=dict(size=10, color='darkblue'), showlegend=True))
        else:
            pass
        if (x == 0 and y==0):
            peaks_pf.append(a)
            impulses_pf.append(b)
            pf_arr.append(y)
            peaks_ev.append(a)
            impulses_ev.append(b)
            ev_arr.append(x)
    print(peaks_ev,impulses_ev,ev_arr)
    
    # sort ev_arr in increasing value
    ev_arr, peaks_ev, impulses_ev = zip(*sorted(zip(ev_arr, peaks_ev, impulses_ev)))
    pf_arr, peaks_pf, impulses_pf = zip(*sorted(zip(pf_arr, peaks_pf, impulses_pf)))
    
    # find slope of the line for ev_arr and peaks_ev
    slope_peaks_ev, intercept_peaks_ev, r_value_peaks_ev, p_value_peaks_ev, std_err_peaks_ev = stats.linregress(ev_arr,peaks_ev)
    slope_impulses_ev, intercept_impulses_ev, r_value_impulses_ev, p_value_impulses_ev, std_err_impulses_ev = stats.linregress(ev_arr,impulses_ev)
    slope_peaks_pf, intercept_peaks_pf, r_value_peaks_pf, p_value_peaks_pf, std_err_peaks_pf = stats.linregress(pf_arr,peaks_pf)
    slope_impulses_pf, intercept_impulses_pf, r_value_impulses_pf, p_value_impulses_pf, std_err_impulses_pf = stats.linregress(pf_arr,impulses_pf)
    print("slope, intecept, r^2, p_value")
    print(slope_peaks_ev, intercept_peaks_ev, r_value_peaks_ev**2, p_value_peaks_ev, std_err_peaks_ev)
    print(slope_impulses_ev, intercept_impulses_ev, r_value_impulses_ev**2, p_value_impulses_ev, std_err_impulses_ev)
    print(slope_peaks_pf, intercept_peaks_pf, r_value_peaks_pf**2, p_value_peaks_pf, std_err_peaks_pf)
    print(slope_impulses_pf, intercept_impulses_pf, r_value_impulses_pf**2, p_value_impulses_pf, std_err_impulses_pf)

    showlegend = False
    
    figure10.add_trace(go.Scatter(x=pf_arr, y=peaks_pf, mode='markers+lines', marker=dict(size=20, color='purple'), showlegend=showlegend, name='Peaks for PF'))
    figure10.add_trace(go.Scatter(x=pf_arr, y=impulses_pf, mode='markers+lines', marker=dict(size=20, color='purple',symbol='triangle-up-dot'), showlegend=showlegend, name='Impulses for PF'))
    figure10.add_trace(go.Scatter(x=ev_arr, y=peaks_ev, mode='markers+lines', marker=dict(size=20, color='orange'), showlegend=showlegend, name='Peaks for IV'))
    figure10.add_trace(go.Scatter(x=ev_arr, y=impulses_ev, mode='markers+lines', marker=dict(size=20, color='orange',symbol='triangle-up-dot'), showlegend=showlegend, name='Impulse for IV'))

    figure10.update_layout(title=f'Peaks and Impulses for Sagittal Moments for various Ankle Angles', xaxis_title='PF/IV angles', yaxis_title='Magnitude', showlegend=showlegend, font_size=20)
    figure10.show()
    
elif step==7:
    
    with open(path+'\\results_speeds_sagittal.pickle', 'rb') as handle: #results_speeds.pickle'
        data_all = pickle.load(handle)
    
    print(data_all)
    
    peaks_ev = []
    peaks_pf = []
    impulses_ev = []
    impulses_pf = []
    pf_arr = []
    ev_arr = []
    peaks_other = []
    impulses_other = []
    other_arr = []
    
    for data in data_all:
        ev_array = data[0]
        pf_array = data[1]
        avg_peak_array = data[2]
        impulse_array = data[3]
        speed = data[4]

        for x,y,a,b in zip(ev_array,pf_array,avg_peak_array,impulse_array):
            angle,angle1 = y,x
            if speed==0 and angle==0: # plot PF
                #print(x,y)
                peaks_pf.append(a)
                impulses_pf.append(b)
                pf_arr.append(angle1)
                #figure10.add_trace(go.Scatter(x=[y], y=[a], mode='markers', marker=dict(size=10, color='red'), showlegend=True))
                #figure10.add_trace(go.Scatter(x=[y], y=[b], mode='markers', marker=dict(size=10, color='blue'), showlegend=True))
            elif speed==1 and angle==0: 
                #print(x,y)
                peaks_ev.append(a)
                impulses_ev.append(b)
                ev_arr.append(angle1)
                #figure10.add_trace(go.Scatter(x=[x], y=[a], mode='markers+lines', marker=dict(size=10, color='darkred'), showlegend=True))
                #figure10.add_trace(go.Scatter(x=[x], y=[b], mode='markers+lines', marker=dict(size=10, color='darkblue'), showlegend=True))
            elif speed==2 and angle==0: # plot EV
                #print(x,y)
                peaks_other.append(a)
                impulses_other.append(b)
                other_arr.append(angle1)
            else:
                pass   
    print(peaks_ev,impulses_ev)
    # sort ev_arr in increasing value
    ev_arr, peaks_ev, impulses_ev = zip(*sorted(zip(ev_arr, peaks_ev, impulses_ev)))
    pf_arr, peaks_pf, impulses_pf = zip(*sorted(zip(pf_arr, peaks_pf, impulses_pf)))
    other_arr, peaks_other, impulses_other = zip(*sorted(zip(other_arr, peaks_other, impulses_other)))
    
    # find slope of the line for ev_arr and peaks_ev
    slope_peaks_ev, intercept_peaks_ev, r_value_peaks_ev, p_value_peaks_ev, std_err_peaks_ev = stats.linregress(ev_arr,peaks_ev)
    slope_impulses_ev, intercept_impulses_ev, r_value_impulses_ev, p_value_impulses_ev, std_err_impulses_ev = stats.linregress(ev_arr,impulses_ev)
    slope_peaks_pf, intercept_peaks_pf, r_value_peaks_pf, p_value_peaks_pf, std_err_peaks_pf = stats.linregress(pf_arr,peaks_pf)
    slope_impulses_pf, intercept_impulses_pf, r_value_impulses_pf, p_value_impulses_pf, std_err_impulses_pf = stats.linregress(pf_arr,impulses_pf) 
    slope_peaks_other, intercept_peaks_other, r_value_peaks_other, p_value_peaks_other, std_err_peaks_other = stats.linregress(other_arr,peaks_other)
    slope_impulses_other, intercept_impulses_other, r_value_impulses_other, p_value_impulses_other, std_err_impulses_other = stats.linregress(other_arr,impulses_other)
        
    print("slope, intecept, r_value, p_value")
    print(slope_peaks_ev, intercept_peaks_ev, r_value_peaks_ev**2, p_value_peaks_ev, std_err_peaks_ev)
    print(slope_impulses_ev, intercept_impulses_ev, r_value_impulses_ev**2, p_value_impulses_ev, std_err_impulses_ev)
    print(slope_peaks_pf, intercept_peaks_pf, r_value_peaks_pf**2, p_value_peaks_pf, std_err_peaks_pf)
    print(slope_impulses_pf, intercept_impulses_pf, r_value_impulses_pf**2, p_value_impulses_pf, std_err_impulses_pf)
    print(slope_peaks_other, intercept_peaks_other, r_value_peaks_other**2, p_value_peaks_other, std_err_peaks_other)      
    print(slope_impulses_other, intercept_impulses_other, r_value_impulses_other**2, p_value_impulses_other, std_err_impulses_other)
    
    
    figure10.add_trace(go.Scatter(x=pf_arr, y=peaks_pf, mode='markers+lines', marker=dict(size=20, color='blue'), showlegend=True, name='Peaks for Fast'))
    figure10.add_trace(go.Scatter(x=pf_arr, y=impulses_pf, mode='markers+lines', marker=dict(size=20, color='blue ',symbol='triangle-up-dot'), showlegend=True, name='Impulses for Fast'))
    figure10.add_trace(go.Scatter(x=ev_arr, y=peaks_ev, mode='markers+lines', marker=dict(size=20, color='green'), showlegend=True, name='Peaks for Med'))
    figure10.add_trace(go.Scatter(x=ev_arr, y=impulses_ev, mode='markers+lines', marker=dict(size=20, color='green',symbol='triangle-up-dot'), showlegend=True, name='Impulses for Med'))
    figure10.add_trace(go.Scatter(x=other_arr, y=peaks_other, mode='markers+lines', marker=dict(size=20, color='red'), showlegend=True, name='Peaks for Slow'))
    figure10.add_trace(go.Scatter(x=other_arr, y=impulses_other, mode='markers+lines', marker=dict(size=20, color='red',symbol='triangle-up-dot'), showlegend=True, name='Impulses for Slow'))

    figure10.update_layout(title=f'Effect of Walking Speed on Peaks and Impulses of Sagittal Moments for only changes in PF', xaxis_title='PF angles', yaxis_title='Magnitude', showlegend=True, font_size=20)
    figure10.show()
    
elif step==4:
    data = []
    chosen_files = ['subj1_fast\\', 'subj1_med_comb\\', 'subj1_slow\\']
    color_speed = ['red', 'blue','green']
    time_select = [[2.91,4.05],[4.22,5.65],[4.11,5.57]]
    time_select_x = [[7.78,8.89,8.49],[11.97,13.36,12.95],[8.52,9.98, 9.55]]
    
    for speed, chosen_file in enumerate(chosen_files):
        folder_name = path+'\\'+chosen_file
    
    
        # Open pickle file for region data
        with open(folder_name+'region_all.pickle', 'rb') as handle: #region_all_mini
            regions = pickle.load(handle)
        
        pf_array = []
        ev_array = []
        avg_peak_array = []
        name_array = []
        avg_peak_neutral = []
        direction_array = []
        impulse_array = []
        impulse_neutral = []
        pf_ev_array = []
        chosen_angles_10 = []
        angle_color = []

        
        # Create break up regions into regions, a region is for a chunck of time
        for x, region in enumerate(regions):
            #print(region[2])
            brain_cmd = region[2]['PF_cmd']
            PF_command = brain_cmd[2] # 0 is PF for metric[0]
            time_cmd = [z for z in brain_cmd[1]]
            valid_cmd = region[2]['valid'][2]

            motor = region[0]
            
            imu = region[1] # 1 is IMU
            imu_gyro = imu['gyro_z'][2]
            imu_state = imu['state'][2]
            time_imu = [z for z in imu['gyro_z'][1]]# need to split up panda
            
            xsens_com = region[4]
            xsens_walking_speed = xsens_com['com_vel_x'][2]
            time_com = [z for z in xsens_com['com_vel_x'][1]]

            xsens_ja = region[3]
            xsens_sag_hip_angle = xsens_ja['hip_sag_right'][2]
            xsens_frontal_hip_angle = xsens_ja['hip_frontal_right'][2]
            xsens_sag_knee_angle = xsens_ja['knee_sag_right'][2]
            xsens_frontal_knee_angle = xsens_ja['knee_frontal_right'][2]
            xsens_sag_ankle_angle = xsens_ja['ankle_sag_right'][2]
            time_ja = [z for z in xsens_ja['hip_sag_right'][1]]
            
            #xsens_linear = region[4]
            #xsens_foot = xsens_linear['foot_vert_vel'][2]
            #time_linear = [z for z in xsens_linear['foot_vert_vel'][1]]
            
            moments = region[0]
            my = moments['my'][2]
            mx = moments['mx'][2]
            fz = moments['fz'][2]
        
            chosen_moment = my
        
            if chosen_moment == mx: 
                chosen_moment_label = 'Frontal Moment'
                time_m = [z for z in moments['mx'][1]]
                sizing =  300 # 10, 30
                height = 0.14
            elif chosen_moment == my: 
                chosen_moment_label = 'Sagittal Moment'
                time_m = [z for z in moments['my'][1]]
                sizing = 125 # 10, 30
                height = 0.5
            elif chosen_moment == fz: chosen_moment_label = 'Axial Force'

            # low pass filter for chosen moment
            sos = signal.butter(2, 6, 'lp', fs=100, output='sos')
            filtered = signal.sosfilt(sos, chosen_moment)
        
            chosen_moment = []
            chosen_moment = [z for z in filtered]
        
            name_ind = brain_cmd[0].find('PF =')
            name = brain_cmd[0][name_ind:]   
            print(name)
        
            #if name in ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']:
            #print(my); print(time_my); break
        
            all_peaks, _ = find_peaks(chosen_moment, height=height, distance=50)
            print(all_peaks)
            #print(len(all_peaks))
            # pick the middle three peaks peaks if there are more than 2 peaks
            if len(all_peaks) > 2:
                peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
            #elif all_peaks == None or math.isnan(all_peaks): peaks = [0]
            else: peaks = all_peaks
            #peaks = all_peaks[0:1+min(2,len(all_peaks))]
            #peaks = all_peaks
            print(peaks)
            print(len(time_m))
            peaks_time = [time_m[z] for z in peaks]
            peaks_array = [chosen_moment[z] for z in peaks]

            if len(peaks) > 2:
                    first_ind = peaks[0] - 50
                    if first_ind < 0: first_ind=0
                    second_ind = peaks[1] - 50
                    last_ind = peaks[len(peaks)-1] + 50
                    print(first_ind, second_ind, last_ind)
                    print(len(chosen_moment), len(time_m))
                    #print(chosen_moment,time_m[first_ind:last_ind]); exit()
                    #try:
                    chosen_moment_stance_integral = integrate.cumtrapz(chosen_moment[first_ind:last_ind], time_m[first_ind:last_ind], initial=0)
                    #print(chosen_moment_stance_integral); exit()
                    #except: chosen_moment_stance_integral = [0]
                    chosen_moment_stance_integral_val = chosen_moment_stance_integral[len(chosen_moment_stance_integral)-1]/len(peaks)
            else: chosen_moment_stance_int = 0
        
            # ignore warnings for nanmean
            #with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            try:
                avg_peak = np.nanmean(peaks_array)
            except: 
                avg_peak = 0
            #print(avg_peak)
            if math.isnan(avg_peak): avg_peak = 0
            elif avg_peak == float('nan'): avg_peak = 0
            #print(avg_peak)
            avg_speed = np.nanmean(xsens_walking_speed)
            
            
            name_ind = brain_cmd[0].find('PF =')
            name = brain_cmd[0][name_ind:]   
            print(name)
            name_array.append(name)
            pf = float(name[name.find('PF =')+4:name.find(',')])
            ev = float(name[name.find('EV = ')+4:])
            #print(pf, ev)
            
            #print(time_cmd)
            #print(PF_command)
            #print(time_imu)
            #print(imu_gyro)
            
            # sample graph to check variables
            #figure3.add_trace(go.Scatter(x=time_imu,y=imu_gyro, mode='lines', name=name))
            chosen_angles = ['PF = 10.0, EV = 0.0', 'PF = 0.0, EV = 10.0', 'PF = -10.0, EV = 0.0', 'PF = 0.0, EV = -10.0']
            
            chosen_other = xsens_sag_hip_angle #xsens_walking_speed
            chosen_other_time = time_ja #time_com
            # if name is one of chosen angles
            if name in chosen_angles:
            
                #figure3.add_trace(go.Scatter(x=time_my, y=my, mode='lines', name=name))
                figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))                

                #figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment_stance_int, mode='lines', name=name, legendgroup=name))
                #print([mx[z] for z in peaks])
                figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))  
                #figure3.add_trace(go.Scatter(x=time_m[first_ind:last_ind], y=chosen_moment_stance_integral, mode='lines', name=name, legendgroup=name))  
                figure5.add_trace(go.Scatter(x=chosen_other_time, y=chosen_other, mode='markers', name=name, legendgroup=name))

                first = peaks[0]; second = peaks[1]
                if name == 'PF = 10.0, EV = 0.0':
                    name = chosen_file[1+chosen_file.find('_'):-1]
                    if name == 'med_comb': name = 'med'
                    #print("worked"); exit()
                    first_ind = [round(z,2) for z in time_m].index(time_select[speed][0])
                    second_ind = [round(z,2) for z in time_m].index(time_select[speed][1])
                    first_ind_x = [round(z,2) for z in time_ja].index(time_select_x[speed][0])
                    second_ind_x = [round(z,2) for z in time_ja].index(time_select_x[speed][1])
                    third_ind_x = [round(z,2) for z in time_ja].index(time_select_x[speed][2])
                    figure7.add_trace(go.Scatter(x=[z - time_m[first_ind] for z in time_m[first_ind:second_ind]], y=chosen_moment[first_ind:second_ind], mode='lines', line_color=color_rgb[2-speed], name=name,legendgroup=name)) 
                    # used shaded region under curve
                    #figure7.add_trace(go.Scatter(x=[z - time_m[first_ind] for z in time_m[first_ind:second_ind]], y=chosen_moment[first_ind:second_ind], mode='lines', line_color=color_rgb[2-speed], name=name, legendgroup=name, fill='toself', opacity=0.35,showlegend=False))
                    # plot peak value of chosen_moment[first_ind:second_ind]; doesn't work
                    #figure7.add_trace(go.Scatter(x=[z - time_m[first_ind] for z in time_m[first_ind:second_ind]], y=[chosen_moment[first_ind:second_ind][z] for z in peaks[first:second]], mode='markers', marker_color=color_rgb[2-speed], name=name, legendgroup=name))
                    #figure7.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                    #figure7.add_trace(go.Scatter(x=[z - time_imu[0] for z in time_imu], y=[z*1000 for z in imu_state], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1])) 
                    #=[z - time_m[first_ind_x] for z in time_m[first_ind_x:second_ind_x]]
                    #figure8.add_trace(go.Scatter(x=[z - time_m[first_ind] for z in time_m[first_ind:second_ind]], y=xsens_sag_hip_angle[first_ind_x:second_ind_x], mode='lines', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=False),1,1) 
                    time = [z - time_m[first_ind_x] for z in time_m[first_ind_x:second_ind_x]]
                    hip = xsens_sag_hip_angle[first_ind_x:second_ind_x]
                    hip_max = [max(hip) for z in hip]  
                    hip_min = [min(hip) for z in hip]
                    knee = xsens_sag_knee_angle[first_ind_x:second_ind_x]
                    knee_max = [max(knee) for z in knee]
                    knee_min = [min(knee) for z in knee]
                    
                    # resample time, hip, knee to be 100 points long and interpolate time
                    time1 = np.linspace(0, 100, 98)
                    time = [z*100/time[len(time)-1] for z in time]
                    #time = np.interp(time1, time, time)
                    print(len(time), len(hip), len(knee))
                    swing_ind = third_ind_x - first_ind_x
                    #print(swing_ind, third_ind_x, len(time)); exit()
                    
                    for i,(x,y) in enumerate(zip(hip_max, knee_max)):
                        replace = 0 #np.NaN #0
                        if i == swing_ind: 
                            hip_max[i] = replace; knee_max[i] = replace
                            hip_min[i] = replace; knee_min[i] = replace
                            
                        if i == len(hip_max)-1:
                            hip_max[i] = replace; knee_max[i] = replace
                            hip_min[i] = replace; knee_min[i] = replace

                    #hip = np.interp(time1, time, hip)
                    #knee = np.interp(time1,time, knee)  
                    #exit()                    
                    figure8.add_trace(go.Scatter(x=time, y=hip, mode='lines', name=name,legendgroup=name,marker_color=color_rgb[2-speed],showlegend=False),1,1) 
                    figure8.add_trace(go.Scatter(x=time, y=knee, mode='lines', name=name,legendgroup=name,marker_color=color_rgb[2-speed],showlegend=True),2,1)#,3-speed,1)
                    figure8.add_trace(go.Scatter(x=time[swing_ind:], y=hip_max[swing_ind:], fill='toself', mode='lines+markers', fillcolor='lightgrey', opacity=0.35, name=name,legendgroup=name,line_color='lightgrey',showlegend=False),1,1)#,3-speed,1)
                    figure8.add_trace(go.Scatter(x=time[swing_ind:], y=knee_max[swing_ind:], fill='toself', mode='lines+markers', fillcolor='lightgrey', opacity=0.35, name=name,legendgroup=name,line_color='lightgrey',showlegend=False),2,1)#,3-speed,1)
                    figure8.add_trace(go.Scatter(x=time[swing_ind:], y=hip_min[swing_ind:], fill='toself', mode='lines', fillcolor='lightgrey', opacity=0.35, name=name,legendgroup=name,line_color='lightgrey',showlegend=False),1,1)#,3-speed,1)   
                    showl = True if speed == 2 else False
                    figure8.add_trace(go.Scatter(x=time[swing_ind:], y=knee_min[swing_ind:], fill='toself', mode='lines', fillcolor='lightgrey', opacity=0.35, name='IMU-defined swing period',legendgroup=name,line_color='lightgrey',showlegend=showl),2,1)#,3-speed,1)
                    
                    figure11.add_trace(go.Scatter(x=[z - time_m[first_ind_x] for z in time_m[first_ind_x:second_ind_x]], y=10*imu_gyro[first_ind_x:second_ind_x], mode='lines', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=True),3-speed,1) 
                    figure11.add_trace(go.Scatter(x=time_ja, y=xsens_sag_knee_angle, mode='lines', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=True),3-speed,1)
                    figure11.add_trace(go.Scatter(x=time_imu, y=10*imu_state, mode='lines', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=True),3-speed,1) 
                    
                    #figure8.add_trace(go.Scatter(x=[z-peaks_time[0] for z in time_m[first_ind:second_ind]], y=xsens_sag_ankle_angle[first_ind:second_ind], mode='lines', name=chosen_file[1+chosen_file.find('_'):-1],legendgroup=chosen_file[1+chosen_file.find('_'):-1]),3,1) 

                # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
                #avg_peak = 0.1
                #figure4.add_trace(go.Scatter(x=[ev], y=[pf], mode='markers', marker=dict(size=abs(0.1*int(avg_peak)), color=abs(0.1*int(avg_peak)), colorscale='Viridis', showscale=True), name=name))
                #print(avg_speed, pf, ev, chosen_moment_stance_int)
                if (ev,pf) not in zip(ev_array,pf_array):
                    pf_array.append(pf)
                    ev_array.append(ev)
                    pf_ev_array.append([ev,pf])
                    avg_peak_array.append((avg_peak))
                    impulse_array.append((chosen_moment_stance_integral_val)) 
                
                    # cartesian to polar
                    #r = math.sqrt(pf**2 + ev**2)
                    theta = math.atan2(pf,ev)
                    direction = 180/np.pi*theta
                    direction_array.append(direction)
                    #if name in chosen_angles_10: 
                    angle_color.append('red')
                    #else: angle_color.append('blue')
                else:
                    ind = pf_ev_array.index([ev,pf]) 
                    #print(ind,[ev,pf],pf_ev_array)
                    avg_peak_array[ind] = (avg_peak_array[ind] + (avg_peak))/2
                    impulse_array[ind] = (impulse_array[ind] + (chosen_moment_stance_integral_val))/2
            
            elif name == 'PF = 0.0, EV = 0.0' and len(all_peaks)<7: # neutral walking trials with around 10 steps
            #    #print(valid_cmd)
            #    figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            #    figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))
                
            #    # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
                avg_peak_neutral.append((avg_peak))  
                impulse_neutral.append((chosen_moment_stance_integral_val))
            #    #theta = math.atan2(ev, pf)
            #    #direction = 180/np.pi*theta
            #    #direction_array.append(direction)
            #    #print('#################################')
            #    #pf_array.append(pf)
            #    #ev_array.append(ev)
            #    #avg_peak_array.append(int(avg_peak))
    
        pf_array.append(0.0); ev_array.append(0.0); avg_peak_array.append(np.nanmean(avg_peak_neutral)) # to add all neutral to the mix
        impulse_array.append(np.nanmean(impulse_neutral)) 
        #
            # remapping theta to ankle angle names
        polar_moments_red = []; polar_impulses = []; direction_names_blue = [];  polar_moments_blue = []; direction_names_red = []; 
        polar_moments_red_sorted = []; polar_moments_blue_sorted = []; direction_names_red_sorted = []; direction_names_blue_sorted = [];
        polar_impulses_red = []; polar_impulses_blue = []; polar_impulses_red_sorted = []; polar_impulses_blue_sorted = [];
        dummy = 0
        direction_name = ['Inversion', 'Plantarflexion', 'Eversion' , 'Dorsiflexion','Inversion']
        order = [180,90, 0,-90, 180]
        print(direction_array, avg_peak_array); #exit()
    
        for i,z in enumerate(angle_color):
            if z=='red':
                polar_moments_red.append(avg_peak_array[i])
                polar_impulses_red.append(impulse_array[i])
                direction_names_red.append(direction_array[i])
            #else:
            #    polar_moments_blue.append(avg_peak_array[i])
            #    polar_impulses_blue.append(impulse_array[i])
            #    direction_names_blue.append(direction_array[i])
    
        for i,z in enumerate(order):
            sort_ind = direction_names_red.index(z)
            polar_moments_red_sorted.append(polar_moments_red[sort_ind])
            polar_impulses_red_sorted.append(polar_impulses_red[sort_ind])
            direction_names_red_sorted.append(direction_names_red[sort_ind])
        
        #for i,z in enumerate(order):
        #    sort_ind = direction_names_blue.index(z)
        #    polar_moments_blue_sorted.append(polar_moments_blue[sort_ind])
        #    polar_impulses_blue_sorted.append(polar_impulses_blue[sort_ind])
        #    direction_names_blue_sorted.append(direction_names_blue[sort_ind])
            

       
        #print(avg_peak_neutral_array,direction_array_neutral)
        avg_peak_array_neutral = np.nanmean(avg_peak_neutral) # to add all neutral to the mix
        avg_impulses_array_neutral = np.nanmean(impulse_neutral) # to add all neutral to the mix    

            # create color array that is a function of avg_peak_array and does not have 0 as a min
        color = []
        second_min = sorted(set(avg_peak_array))
        for x in (avg_peak_array):#+avg_peak_array_neutral):
            # if x is 0, make x the 2nd smallest value of avg_peak_array
            #if x == 0: x = second_min
            color.append(x)
        
        color1 = []
        second_min = sorted(set(impulse_array))
        for x in (impulse_array):#+avg_impulses_array_neutral):
            # if x is 0, make x the 2nd smallest value of avg_peak_array
            #if x == 0: x = second_min
            color1.append(x)
        
        #print(avg_peak_array_neutral)
        name = chosen_file[1+chosen_file.find('_'):-1]
        if name == 'med_comb': name = 'med'
        marker_size = 10
        avg_peak_neutral_array = [avg_peak_array_neutral for z in direction_name] #range(360)
        polar_impulses_neutral_array = [avg_impulses_array_neutral for z in direction_name] #range(360)
        #direction_array_neutral = np.linspace(0,360,361)
        #figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_blue_sorted, theta=direction_name, mode='markers',marker_color='blue',  marker=dict(size=marker_size), name="5 deg"),1,1)
        #print("5 deg inf:",avg_peak_array,direction_array)
        #figure_polar1.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_name, mode='lines', name='Neutral',marker_color='green'),1,1)
        figure_polar1.add_trace(go.Scatterpolar(r=polar_moments_red_sorted, theta= direction_name, marker_color=color_speed[speed], mode='lines+markers',  marker=dict(size=marker_size), name=name),1,1)
    
        #figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_blue_sorted, theta=direction_name, mode='markers',  marker=dict(size=marker_size), marker_color='blue', name="5 deg",showlegend=False),1,2)
        #figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_neutral_array, theta= direction_name, mode='lines', name='Neutral',marker_color='green',showlegend=False),1,2)
        figure_polar1.add_trace(go.Scatterpolar(r=polar_impulses_red_sorted, theta= direction_name, marker_color=color_speed[speed],  marker=dict(size=marker_size), mode='lines+markers', name="10 deg",showlegend=False),1,2)
        
        #print(avg_peak_neutral_array,direction_array_neutral)
        #figure4.add_trace(go.Scatter(x=ev_array, y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[z/sizing for z in avg_peak_array], color=color, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'

        #figure6.add_trace(go.Scatter(x=ev_array, y=pf_array, mode='markers', text=impulse_array, marker=dict(size=[z/sizing for z in avg_peak_array], color=color, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'
        #figure6.show()
        #figure6 = go.Figure()
        
        
        #figure_polar.add_trace(go.Scatterpolar(r=avg_peak_array, theta= direction_array, mode='lines+markers', name=chosen_file[1+chosen_file.find('_'):-1]))
        #figure_polar.add_trace(go.Scatterpolar(r=polar_moments, theta= direction_name, mode='lines+markers', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=False),1,1)
        
        #figure_polar.add_trace(go.Scatterpolar(r=polar_impulses, theta= direction_name, mode='lines+markers', name=name,legendgroup=name,marker_color=color_rgb[speed],showlegend=True),1,2)
        
        figure4.update_layout(title=f'PF vs IV, with Peak {chosen_moment_label} as marker color and size', xaxis_title='IV', yaxis_title='PF')
        figure3.update_layout(title=f'{chosen_moment_label} vs Time, with the chosen peaks', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm)', legend_title='Grouped by Angle')
        figure_polar.update_layout(title=f'Polar Plot of {chosen_moment_label} Peaks (left) and Impulse (Right) vs Angle', legend_title='Grouped by condition')
        figure_polar1.update_layout(title=f'Polar Plot of the Peaks(left) and Impulses (right) for {chosen_moment_label} vs Ankle Angle', legend_title='Grouped by speed')
        figure7.update_layout(title=f'{chosen_moment_label} vs Time for PF = 10.0, IV = 0.0', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm/kg)', legend_title='Grouped by Speed', font_size = 20)
        figure8.update_layout(title=f'Hip and Knee sagittal angles for one stride of PF= 10.0, IV = 0.0', xaxis2_title='Percentage of stride (0 to 100%, heel strike to heel strike)', yaxis1_title=f'Hip Flexion Angle (deg)', yaxis2_title=f'Knee Flexion Angle (deg)', legend_title='Grouped by Speed', font_size=15)

        data.append([[-z for z in ev_array], pf_array, avg_peak_array,impulse_array,speed])
        #print(data)
        
    #figure3.show()
    #figure4.show()
    #figure_polar.show()
    figure7.show()
    #figure_polar1.show()
    #figure5.show()
    figure8.show()
    #figure11.show()
    
    
    # save to pickle file
    #print(path+'\results.pickle')
    #with open(path+'\\results_speeds_sagittal.pickle', 'wb') as handle: 
    #    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
elif step==5:
    
    #open pickle file
    with open(path+'\\results.pickle', 'rb') as handle: 
        data = pickle.load(handle) 
        
    
    
else: print("pick a valid option")



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




