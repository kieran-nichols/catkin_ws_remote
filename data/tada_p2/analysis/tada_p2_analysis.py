import subprocess
import os
import pandas as pd
import os
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from plotly.colors import sequential, n_colors
from scipy.signal import find_peaks
import time
from plotly.subplots import make_subplots
import types
import pickle
import warnings
import math
colors = n_colors('rgb(0, 255, 255)', 'rgb(0, 0, 255)', 255, colortype = 'rgb')


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
path = r"C:\Users\roemb\source\repos\catkin_ws_remote\data\tada_p2\subj1"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
topics = ['angular_moments','europa_topic', 'linear_moments', 'motor_command', 'sensing_topic', 'xsens_joint_angle', 'xsens_com']
#colors = ['red', 'blue', 'green']

figure = go.Figure()
figure1 = go.Figure()
figure2 = go.Figure()
figure3 = go.Figure()
figure4 = go.Figure()
#figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
#figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], horizontal_spacing=0.075,)# subplot_titles=("Plantarflexor Moment", "Eversion Moment", "Resultant Moment")) 

color_dict = dict(zip(['slow', 'med', 'fast'], colors))
moments = {'mx':[], 'my':[], 'fz':[]}
imu_data = {'gyro_z':[], 'state':[]}
linear_moments = {'foot_vert_vel':[]}
motor_command = {'PF_cmd':[], 'EV_cmd':[], 'valid':[]}#, 'm1_cmd':[], 'm2_cmd':[], 'CPU0':[], 'CPU1':[], 'CPU2':[], 'CPU3':[]}
xsens_joint_angle = {'hip_sag':[], 'knee_sag':[], 'ankle_sag':[]}
xsens_com = {'com_pos_x':[], 'com_pos_y':[], 'com_pos_z':[]}
files = [f for f in os.listdir(path) if f.endswith('.bag')]

step = 1

# convert the rosbag to csv files that are based on topics
if step==0:
        ## loop through files
    for file in files:
        # create folder using subprocess
        reduced_file_name = file[:-4]
        print(reduced_file_name)        
        subprocess.run('mkdir {}'.format(path+'\\'+reduced_file_name), capture_output=True, text=True, shell=True)
        # loop through each topic
        for topic in topics:
            print("rostopic echo -b {} -p /{} > {}\{}.csv".format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic))
            subprocess.run('rostopic echo -b {} -p /{} > {}\{}.csv'.format(path+'\\'+file,topic,path+'\\'+reduced_file_name,topic), capture_output=True, text=True, shell=True)

    #all_filenames = ['\\subj1_med','\\subj1_med_3.5_n135','\\subj1_med_after']
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
    folder_name = path+'\\'+'subj1_slow\\'
    # Read europa data
    data = pd.read_csv(folder_name+'europa_topic.csv')
    data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    #print(data)
    time = data.field_t - data.field_t[0] 
    #print(data.field_t[0])
    moments['mx'] = data.field_mx
    moments['my'] = data.field_my
    moments['fz'] = data.field_fz
    
    # read imu data
    data1 = pd.read_csv(folder_name+'sensing_topic.csv')
    data1.columns = data1.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time1 = data1.field_t - data.field_t[0]
    #print(data1)
    imu_data['gyro_z'] = data1.field_gyro_z
    imu_data['state'] = data1.field_state
        
    # Read motor cmd data from csv
    data2 = pd.read_csv(folder_name+'motor_command.csv')
    data2.columns = data2.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time2 = data2.field_t - data.field_t[0]
    #motor_command['m1_cmd'] = data2.field_motor1_move/567*360
    #motor_command['m2_cmd'] = data2.field_motor2_move/567*360
    motor_command['PF_cmd'], motor_command['EV_cmd'] = data2.field_PF_cmd, data2.field_EV_cmd
    motor_command['valid'] = data2.field_valid
    #print(motor_command['PF_cmd'])
    #motor_command['CPU0'], motor_command['CPU1'], motor_command['CPU2'], motor_command['CPU3'] = data2.field_CPU0, data2.field_CPU1, data2.field_CPU2, data2.field_CPU3  
        
    ## Read xsens joint angle data from csv # taking the time offset from windows data since the offset is different to linux topics
    data3 = pd.read_csv(folder_name+'xsens_joint_angle.csv')
    data3.columns = data3.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time3 = data3.field_data0 - data.field_t[0] #data3.field_data0[0]# + 28302.41254 # - data.field_t[0]
    #print(data3.field_data0[0])
    xsens_joint_angle['hip_frontal_right'] = data3.field_data3
    xsens_joint_angle['knee_frontal_right'] = data3.field_data8
    xsens_joint_angle['ankle_frontal_right'] = data3.field_data13
    xsens_joint_angle['hip_sag_right'] = data3.field_data4
    xsens_joint_angle['knee_sag_right'] = data3.field_data9
    xsens_joint_angle['ankle_sag_right'] = data3.field_data14
        
    ## Read xsens com data from csv # taking the time offset from windows data since the offset is different to linux topics
    data4 = pd.read_csv(folder_name+'xsens_com.csv')
    data4.columns = data4.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time4 = data4.field_data0 - data.field_t[0] #data4.field_data0[0]#+ 28302.41254
    xsens_com['com_pos_x'] = data4.field_data1
    xsens_com['com_pos_y'] = data4.field_data2
    xsens_com['com_pos_z'] = data4.field_data3
        
    ## Read linear moments data from csv # taking the time offset from windows data since the offset is different to linux topics
    data5 = pd.read_csv(folder_name+'linear_moments.csv')
    data5.columns = data5.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    time5 = data5.field_data0 - data.field_t[0] #data5.field_data0[0] + 28302.41254
    linear_moments['foot_vert_vel'] = data5.field_data16   
    
            ## Show entire time series for data of interest; Plot entire experiment
    # Future goal to plot the below graph using a for loop with the region variable allowing for much less written code
    figure.add_trace(go.Scatter(x=time, y=moments['mx'], mode='lines', name='Mx'))
    figure.add_trace(go.Scatter(x=time, y=moments['my'], mode='lines', name='My'))
    figure.add_trace(go.Scatter(x=time, y=moments['fz'], mode='lines', name='Fz'))

    figure.add_trace(go.Scatter(x=time1, y=imu_data['gyro_z'], mode='lines', name='gyro_z'))
    figure.add_trace(go.Scatter(x=time1, y=imu_data['state'], mode='lines', name='state'))

    #figure.add_trace(go.Scatter(x=time2, y=motor_command['m1_cmd'], mode='lines', name='motor1_cmd (deg)')) # adding markers slows down the rendering
    #figure.add_trace(go.Scatter(x=time2, y=motor_command['m2_cmd'], mode='lines', name='motor2_cmd (deg)')) 
    figure.add_trace(go.Scatter(x=time2, y=motor_command['PF_cmd'], mode='lines', name='PF_cmd'))
    figure.add_trace(go.Scatter(x=time2, y=motor_command['EV_cmd'], mode='lines', name='EV_cmd'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU0'], mode='lines', name='CPU0'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU1'], mode='lines', name='CPU1'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU2'], mode='lines', name='CPU2'))
    ##figure.add_trace(go.Scatter(x=time2, y=motor_command['CPU3'], mode='lines', name='CPU3'))

    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_sag_right'], mode='lines', name='hip_sag_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_sag_right'], mode='lines', name='knee_sag_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_sag_right'], mode='lines', name='ankle_sag_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['hip_frontal_right'], mode='lines', name='hip_frontal_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['knee_frontal_right'], mode='lines', name='knee_frontal_right'))
    #figure.add_trace(go.Scatter(x=time3, y=xsens_joint_angle['ankle_frontal_right'], mode='lines', name='ankle_frontal_right'))

    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_x'], mode='lines', name='com_pos_x'))
    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_y'], mode='lines', name='com_pos_y'))
    #figure.add_trace(go.Scatter(x=time4, y=xsens_com['com_pos_z'], mode='lines', name='com_pos_z'))

    #figure.add_trace(go.Scatter(x=time5, y=linear_moments['foot_vert_vel'], mode='lines', name='foot_vert_vel'))

    figure.update_layout(title='All data', xaxis_title='Time (s)', yaxis_title='Value')
    figure.show(); #exit()
        
    ########################################
    # TADA_angle finder (10 steps); in this dataset, the TADA angle changes, the persons walks about 10 steps, then the TADA angles changes back to 0,0

    # create lists for all topics that creates regions of time based on trial selector where the cmds are not 0
    all_metrics = [moments, imu_data, motor_command]#, xsens_joint_angle, xsens_com, linear_moments] # there seems to be some issues with time of linear_moments
    all_time = [time, time1, time2]#, time3, time4, time5]
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
            start_time = time[i]
            start_info['start_time'].append(start_time)
            start_info['start_index'].append(i)
            start_info['PF'].append(approx_val[0])
            start_info['EV'].append(approx_val[1])
        prev_val = approx_val
    #print(start_info)

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
                last_time = [0,0]
                #print(topic[0])
                # find the region that is within the start and end time
                for q, q_val in enumerate(topic[1]):
                    #for l, value1 in enumerate(q_val):
                    #print(q, q_val)
                    #if q >= start_index and q <= end_index:
                    #try: # decided to ignore some errors from the below line
                    topic_time = all_time[j][q]
                    if topic_time >= start_time and topic_time <= end_time and motor_command['valid'][q]:
                        list_of_values.append(q_val)
                        last_time = [q, topic_time]
                        
                    # conditional statement if the end time is not valid then create an end time that is valid; valid means the experiment is not paused
                    if last_time[1] < end_time: end_index = last_time[0]
                    #except: pass
                #list_of_time = all_time[j][start_index:end_index] #- all_time[j][start_index]
                try: # some errors seem to pop up with this time calculation
                    list_of_time = all_time[j][start_index:end_index] - all_time[j][start_index] # set all chunks to have an initial time of 0
                except:
                    list_of_time = []
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
    folder_name = path+'\\'+'subj1_fast\\'
    
    
    # Open pickle file for region data
    with open(folder_name+'region_all.pickle', 'rb') as handle: #region_all_mini
        regions = pickle.load(handle)
        
    pf_array = []
    ev_array = []
    avg_peak_array = []
    name_array = []
    avg_peak_neutral = []
    direction_array = []
    
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
            sizing =  10 # 10, 30
        elif chosen_moment == my: 
            chosen_moment_label = 'Sagittal Moment'
            sizing =  30 # 10, 30
        elif chosen_moment == fz: chosen_moment_label = 'Axial Force'
        
        time_m = [z for z in moments['mx'][1]]
        #print(my); print(time_my); break
        height = 200
        all_peaks, _ = find_peaks(chosen_moment, height=height, distance=50)
        #print(all_peaks)
        #print(len(all_peaks))
        # pick the middle three peaks peaks if there are more than 2 peaks
        if len(all_peaks) > 2:
            peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
        #elif all_peaks == None or math.isnan(all_peaks): peaks = [0]
        else: peaks = all_peaks
        #peaks = all_peaks[0:1+min(2,len(all_peaks))]
        #peaks = all_peaks
        print(peaks)
        peaks_time = [time_m[z] for z in peaks]
        peaks_array = [chosen_moment[z] for z in peaks]
        
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
        if name != 'PF = 0.0, EV = 0.0':
            #figure3.add_trace(go.Scatter(x=time_my, y=my, mode='lines', name=name))
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            #print([mx[z] for z in peaks])
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))           
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            #avg_peak = 0.1
            #figure4.add_trace(go.Scatter(x=[ev], y=[pf], mode='markers', marker=dict(size=abs(0.1*int(avg_peak)), color=abs(0.1*int(avg_peak)), colorscale='Viridis', showscale=True), name=name))
            pf_array.append(pf)
            ev_array.append(ev)
            avg_peak_array.append(int(avg_peak))
            
            # cartesian to polar
            #r = math.sqrt(pf**2 + ev**2)
            theta = math.atan2(ev, pf)
            direction = 180/np.pi*theta
            direction_array.append(direction)
        
        elif name == 'PF = 0.0, EV = 0.0' and 5<len(all_peaks)<11 and valid_cmd: # neutral walking trials with around 10 steps
            #print(valid_cmd)
            figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))
                
            # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            avg_peak_neutral.append(int(avg_peak))  
            #theta = math.atan2(ev, pf)
            #direction = 180/np.pi*theta
            #direction_array.append(direction)
            #print('#################################')
            #pf_array.append(pf)
            #ev_array.append(ev)
            #avg_peak_array.append(int(avg_peak))
    
    pf_array.append(0.0); ev_array.append(0.0); avg_peak_array.append(np.nanmean(avg_peak_neutral)) # to add all neutral to the mix
    #
    #print(avg_peak_neutral)
    
    # create scatter plot that has x be ev, y be pf, and marker color and size be avg_peak, I used a 1/10 or 1/30 for frontal or sagittal for marker sizing  and offset the minimum peak, 
    print(avg_peak_array,'\n', pf_array ,'\n', ev_array )
    
    # create color array that is a function of avg_peak_array and does not have 0 as a min
    color = []
    second_min = sorted(set(avg_peak_array))
    for x in avg_peak_array:
        # if x is 0, make x the 2nd smallest value of avg_peak_array
        if x == 0: x = second_min
        color.append(x)
        
    #print(avg_peak_neutral)
    avg_peak_neutral_array = [avg_peak_neutral[0] for z in range(360)]
    direction_array_neutral = np.linspace(0,360,361)
    #print(avg_peak_neutral_array,direction_array_neutral)
    figure4.add_trace(go.Scatter(x=ev_array, y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[z/sizing for z in avg_peak_array], color=color, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'
    figure_polar.add_trace(go.Scatterpolar(r=avg_peak_array, theta= direction_array, mode='markers', name=chosen_moment_label+chosen_moment_label[1]))
    figure_polar.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_array_neutral, mode='lines', line_width = 5, name='Neutral'))
    
    figure4.update_layout(title=f'PF vs EV, with Peak {chosen_moment_label} as marker color and size', xaxis_title='EV', yaxis_title='PF')
    figure3.update_layout(title=f'{chosen_moment_label} vs Time, with the chosen peaks', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm)', legend_title='Grouped by Angle')
    figure_polar.update_layout(title=f'Polar Plot of {chosen_moment_label} vs Angle', legend_title='Grouped by condition')

    figure3.show()
    figure4.show()
    figure_polar.show()
    
elif step==3:

    chosen_files = ['subj1_fast\\', 'subj1_med\\', 'subj1_slow\\']
    
    for chosen_file in chosen_files:
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
                sizing =  10 # 10, 30
            elif chosen_moment == my: 
                chosen_moment_label = 'Sagittal Moment'
                sizing =  30 # 10, 30
            elif chosen_moment == fz: chosen_moment_label = 'Axial Force'
        
            time_m = [z for z in moments['mx'][1]]
            #print(my); print(time_my); break
            height = 200
            all_peaks, _ = find_peaks(chosen_moment, height=height, distance=50)
            #print(all_peaks)
            #print(len(all_peaks))
            # pick the middle three peaks peaks if there are more than 2 peaks
            if len(all_peaks) > 2:
                peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
            #elif all_peaks == None or math.isnan(all_peaks): peaks = [0]
            else: peaks = all_peaks
            #peaks = all_peaks[0:1+min(2,len(all_peaks))]
            #peaks = all_peaks
            print(peaks)
            peaks_time = [time_m[z] for z in peaks]
            peaks_array = [chosen_moment[z] for z in peaks]
        
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
            if name != 'PF = 0.0, EV = 0.0':
                #figure3.add_trace(go.Scatter(x=time_my, y=my, mode='lines', name=name))
                figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
                #print([mx[z] for z in peaks])
                figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))           
                
                # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
                #avg_peak = 0.1
                #figure4.add_trace(go.Scatter(x=[ev], y=[pf], mode='markers', marker=dict(size=abs(0.1*int(avg_peak)), color=abs(0.1*int(avg_peak)), colorscale='Viridis', showscale=True), name=name))
                pf_array.append(pf)
                ev_array.append(ev)
                avg_peak_array.append(int(avg_peak))
            
                # cartesian to polar
                #r = math.sqrt(pf**2 + ev**2)
                theta = math.atan2(ev, pf)
                direction = 180/np.pi*theta
                direction_array.append(direction)
        
            #elif name == 'PF = 0.0, EV = 0.0' and 5<len(all_peaks)<11 and valid_cmd: # neutral walking trials with around 10 steps
            #    #print(valid_cmd)
            #    figure3.add_trace(go.Scatter(x=time_m, y=chosen_moment, mode='lines', name=name, legendgroup=name))
            #    figure3.add_trace(go.Scatter(x=peaks_time, y=peaks_array, mode='markers', name=name, legendgroup=name))
                
            #    # create scatter plot that has x be ev, y be pf, and marker color be avg_peak
            #    avg_peak_neutral.append(int(avg_peak))  
            #    #theta = math.atan2(ev, pf)
            #    #direction = 180/np.pi*theta
            #    #direction_array.append(direction)
            #    #print('#################################')
            #    #pf_array.append(pf)
            #    #ev_array.append(ev)
            #    #avg_peak_array.append(int(avg_peak))
    
        #pf_array.append(0.0); ev_array.append(0.0); avg_peak_array.append(np.nanmean(avg_peak_neutral)) # to add all neutral to the mix
        #
        #print(avg_peak_neutral)
    
        # create scatter plot that has x be ev, y be pf, and marker color and size be avg_peak, I used a 1/10 or 1/30 for frontal or sagittal for marker sizing  and offset the minimum peak, 
        print(avg_peak_array,'\n', pf_array ,'\n', ev_array )
    
        # create color array that is a function of avg_peak_array and does not have 0 as a min
        color = []
        second_min = sorted(set(avg_peak_array))
        for x in avg_peak_array:
            # if x is 0, make x the 2nd smallest value of avg_peak_array
            if x == 0: x = second_min
            color.append(x)
        
        #print(avg_peak_neutral)
        #avg_peak_neutral_array = [avg_peak_neutral[0] for z in range(360)]
        #direction_array_neutral = np.linspace(0,360,361)
        #print(avg_peak_neutral_array,direction_array_neutral)
        figure4.add_trace(go.Scatter(x=ev_array, y=pf_array, mode='markers', text=avg_peak_array, marker=dict(size=[z/sizing for z in avg_peak_array], color=color, colorscale=colors, colorbar=dict(title=chosen_moment_label), showscale=True))) #'Viridis'
        figure_polar.add_trace(go.Scatterpolar(r=avg_peak_array, theta= direction_array, mode='lines+markers', name=chosen_moment_label+chosen_moment_label[1]))
        #figure_polar.add_trace(go.Scatterpolar(r=avg_peak_neutral_array, theta= direction_array_neutral, mode='lines', line_width = 5, name='Neutral'))
    
        figure4.update_layout(title=f'PF vs EV, with Peak {chosen_moment_label} as marker color and size', xaxis_title='EV', yaxis_title='PF')
        figure3.update_layout(title=f'{chosen_moment_label} vs Time, with the chosen peaks', xaxis_title='Time (s)', yaxis_title=f'{chosen_moment_label} (Nm)', legend_title='Grouped by Angle')
        figure_polar.update_layout(title=f'Polar Plot of {chosen_moment_label} vs Angle', legend_title='Grouped by condition')

    #figure3.show()
    #figure4.show()
    figure_polar.show()
    
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




