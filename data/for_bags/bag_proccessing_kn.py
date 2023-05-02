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
#path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\for_bags"
path = r"C:\Users\aheto\Documents\research\catkin_ws\catkin_ws_remote\data\for_bags"
files = [f for f in os.listdir(path) if f.endswith('.bag')]
#print(files, "\nlist_length= ", len(files))
all_real_time = []
all_moment = []
all_peaks = []
colors = ['red', 'blue', 'green']
TADA_angles = ['0, 180', '10, 0', '10, 180', '10, 90', '10, n90']
speed_dict = {'slow': 0, 'med': 1, 'fast': 2}

figure = go.Figure()
figure1 = go.Figure()
figure2 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)   
figure_peaks = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], subplot_titles=("Plantarflexor Peaks", "Eversion Peaks"))   
figure3 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009) 
figure_state = go.Figure()     
figure_polar = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2],  subplot_titles=("Plantarflexor Moment", "Eversion Moment")) 

color_dict = dict(zip(['slow', 'med', 'fast'], colors))
moments = {'mx':[], 'my':[]}
#print(moments)
condition_dict = dict(zip(['slow', 'med', 'fast'], colors))
TADA_angle_dict = dict(zip(TADA_angles, ['Neutral', 'PF', 'DF', 'EV', 'IV']))
peak_avg_array_sag = []
peak_avg_array_front = []
condition_sag = []
condition_frontal = []
peak_avg_sag = []
peak_avg_front = []
speed_sag = []
speed_front = []
peak_avg_result_array = []
speed_array = []
error_on_raise_delay = []
error_on_fall_delay = []
#print(color_dict)
#print(TADA_angle_dict)

# loop through each file
#for file in files:
    # Execute the command and retrieve the output
    #subprocess.run('rostopic echo -b {} -p /europa_topic > data_kn/europa_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
    #subprocess.run('rostopic echo -b {} -p /sensing_topic > data_kn/sensing_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)  
    #subprocess.run('rostopic echo -b {} -p /angular_moments > data_kn/angular_moments_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
#raise SystemExit
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
    #real_time = pd.DataFrame({'time':[]}, dtype: float64)
    #print(condition, speed)
    
    # Execute the command and retrieve the output
    #subprocess.run('rostopic echo -b {} -p /europa_topic > data_kn/europa_topic_{}.csv'.format(file,file), capture_output=True, text=True, shell=True)
    # read the data from the file
    data = pd.read_csv('data_kn/europa_topic_{}.csv'.format(file)) 
    data.columns = data.columns.map(lambda x : x.replace(".", "_").replace("%", ""))

    data_sensing = pd.read_csv('data_kn/sensing_topic_{}.csv'.format(file)) 
    data_sensing.columns = data_sensing.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    data_sensing_state = data_sensing.field_state
    print(data_sensing_state)
    data_angular = pd.read_csv('data_kn/angular_moments_{}.csv'.format(file)) 
    data_angular.columns = data_angular.columns.map(lambda x : x.replace(".", "_").replace("%", ""))
    data_angular_r = [data_angular.field_data16, data_angular.field_data17, data_angular.field_data18 ] #foot
    data_angular_l = [data_angular.field_data37, data_angular.field_data38, data_angular.field_data39 ] #foot


    ######calculating error: to compare state###########
    for i in range(1, len(data_sensing_state)):
        if data_sensing_state[i-1]==0 and data_sensing_state[i]==1:
            b = data_angular_r[1].index(min(data_angular_r[1][i-20:i+20]))
            error_on_raise_delay.append(data_sensing.time[i] - data_angular.field_data0[b])
        if data_sensing_state[i-1]==1 and data_sensing_state[i]==0:
            b = data_angular_r[1].index(min(data_angular_r[1][i-20:i+20]))
            error_on_fall_delay.append(data_sensing.time[i] - data_angular.field_data0[b])

    
    #print(data.field_moment)
    #time = data.time
    #real_time = (data.time - data.time[0])/1_000_000_000
    # create list of indices that has length of data.time
    #for i in range(len(data.time)):
        #real_time.append({'time':i}, ignore_index=True)
    real_time = data.index
    moments['mx'] = data.field_mx
    moments['my'] = data.field_my
    #all_real_time.append(real_time)
    peak_avg_array = []
    peak_avg_result = []
    figure = go.Figure()
    show_legend = False

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
        height = 600 if j==1 else 200
        all_peaks, _ = find_peaks(moment, height=height, distance=50)
        # pick the middle three peaks
        peaks = all_peaks[len(all_peaks) // 2 - 1: len(all_peaks) // 2 + 2]
        condition_array = []
        #all_peaks.append((peaks))
        #print(len(peaks))
    
        #figure.data = []
        figure.add_trace(go.Scatter(x=real_time, y=moment, mode='lines'))
        figure.add_trace(go.Scatter(x=real_time[peaks], y=moment[peaks], mode='markers'))
        #figure_peaks.add_trace(go.Scatter(x=real_time[peaks], y=moment[peaks], mode='markers'))
    
        #print(color_dict[speed])
        condition_list = [condition]*len(peaks)
        speed_list = [speed]*len(peaks)
        #print(condition_list, speed_list)
        figure1.add_trace(go.Scatter(x=condition_list, y=moment[peaks], mode='markers', name=speed, marker_color=color_dict[speed]))
        legendgroup = f'group{speed_dict[speed]}'
        figure2.add_trace(go.Scatter(x=condition_list, y=moment[peaks], mode='markers', name=speed, marker_color=color_dict[speed],legendgroup=legendgroup, showlegend=show_legend),j+1,1)
        
        peak_avg = np.mean(moment[peaks])
        # sagittal
        if j==1:
            peak_avg_array_sag.append(peak_avg)
            condition_sag.append(condition)
            speed_sag.append(speed)
            peak_avg_result.append(peak_avg)
            speed_array.append(speed)
        # frontal
        else: 
            peak_avg_array_front.append(peak_avg)
            condition_frontal.append(condition)
            speed_front.append(speed)
            peak_avg_result.append(peak_avg)
        condition_array.append(condition)
        
        # place means as diamonds on the plot
        #trace = go.Scatter(x=[condition], y=[peak_avg], mode='markers', name=speed, legendgroup=legendgroup, showlegend=show_legend, marker=dict(color=color_dict[speed], size=10, symbol = 'diamond'))
        #figure2.add_trace(trace,j+1,1)
        
        #break
    #figure.show()
    #break
    #time.sleep(2)
    peak_avg_result_array.append(np.linalg.norm(peak_avg_result))
    #peak_avg_front[i] = np.mean(peak_avg_array_front)
    #figure2.add_trace(go.Scatter(x=condition_array, y=peak_avg_result_array, mode='markers', name=speed, marker_color=color_dict[speed],legendgroup=legendgroup, showlegend=show_legend),2,1)
    
figure_state.add_trace(go.Scatter(y=error_on_raise_delay, mode='lines', name="Raise Delay"))
figure_state.add_trace(go.Scatter(y=error_on_fall_delay, mode='lines', name = "Fall Delay"))
# sort through the data to display a line graph for the average peaks for each condition and give a color for each speed
peak_sum_sag = [0,0,0,0,0] #[0,0,0]
peak_sum_front = [0,0,0,0,0] 
# sort by speed
for i in range(1,3):
    # by speed
    x_values = [0,0,0,0,0]
    y_values = [0,0,0,0,0] #[0,0,0]
    z_values = [0,0,0,0,0] 
    result_values = [0,0,0,0,0] 
    speed = speed_array[2-i]
    # sort by condition
    for j in range(1,5):
        # by condition
        #print(i,j)
        x_values[j] = condition_sag[j*3 + i]
        y_values[j] = peak_avg_array_sag[j*3 + i]
        z_values[j] = peak_avg_array_front[j*3 + i]
        result_values[j] = peak_avg_result_array[j*3 + i]
        peak_sum_sag[j]+=y_values[j]/3
        peak_sum_front[j]+=z_values[j]/3
    
    new_color = colors[2-i] # fast is the first trial, then med, then slow
    legendgroup=f'group1{2-i}'


    figure2.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='peak_sag_avg_array',marker=dict(color=new_color), showlegend=show_legend, legendgroup=legendgroup),2,1)
    figure2.add_trace(go.Scatter(x=x_values, y=z_values, mode='lines', name=speed, marker=dict(color=new_color), legendgroup=legendgroup),1,1) # 'peak_front_avg_array', showlegend=show_legend,
    #figure2.add_trace(go.Scatter(x=x_values, y=result_values, mode='lines+markers', name=speed, marker=dict(color=new_color), legendgroup=legendgroup,),3,1) # name='peak_front_avg_array'
    #figure3.show()
    #time.sleep(3)
    #figure3.add_trace(go.Scatter(x=condition_frontal[i], y=peak_avg_array_front[i], mode='markers+lines', name='peak_front_avg_array'),1,1)
    #figure3.add_trace(go.Scatter(x=speed_sag, y=peak_avg_array_sag, mode='lines', name='peak_sag_avg_array', marker=dict(color=color_dict[speed], size=10, symbol = 'diamond')),2,1)
    
    # sort by condition to make polar plot where center is netural
    # right is EV, up is PF, left is IV, and down is DF
    # all non-neutral moments are subtracted from the neutral moment for that speed
    # all neutral moments are normalized to the max value of all sag and front moments
    moment_offset = [y_values[0], z_values[0], result_values[0]]
    max_moment = [np.max(peak_avg_array_front), np.max(peak_avg_array_sag), np.max(peak_avg_result_array)]
    polar_moments_sag = []
    polar_moments_front = []
    polar_moments_result = []
    #direction = [0, 90, 180 ,270,0] # relates to PF, DF, EV, IV
    direction = ['Plantarflexion', 'Eversion', 'Dorsiflexion', 'Inversion', 'Plantarflexion']
    order = [1,3,2,4,1]
    for k in range(5):
        # convert polar values to be between 0 and 1
        #print(i,k)
        k = order[k] # overide k to create line graphs
        polar_moments_sag.append((y_values[k]))# - moment_offset[0] #/max_moment[0])
        polar_moments_front.append((z_values[k]))# - moment_offset[1])) #/max_moment[1])
        polar_moments_result.append((result_values[k]))# - moment_offset[2])) #/max_moment[2]))
    figure_polar.add_trace(go.Scatterpolar(r=polar_moments_sag, theta= direction, mode='markers+lines', name='sag moment',marker=dict(color=new_color),showlegend=show_legend, legendgroup=legendgroup, line_width=6, marker_line_width=6),1,1)
    figure_polar.add_trace(go.Scatterpolar(r=polar_moments_front, theta= direction, mode='markers+lines', name=speed, marker=dict(color=new_color), legendgroup=legendgroup,  line_width=6, marker_line_width=6),1,2) # 'frontal moment', showlegend=show_legend
    #figure_polar.add_trace(go.Scatterpolar(r=polar_moments_result, theta= direction, mode='markers+lines', name=speed, marker=dict(color=new_color),legendgroup=legendgroup),1,3) # name='resultant moment'
print(peak_sum_sag)
print(peak_sum_front)
print(direction)
figure_peaks.add_trace(go.Scatterpolar(r=peak_sum_sag, theta= direction, mode='markers+lines', name="sag peaks", marker=dict(color=new_color), showlegend=show_legend, legendgroup=legendgroup,  line_width=6, marker_line_width=6),1,1) # 'frontal moment', showlegend=show_legend
figure_peaks.add_trace(go.Scatterpolar(r=peak_sum_front, theta= direction, mode='markers+lines', name="frontal peaks", marker=dict(color=new_color), legendgroup=legendgroup,  line_width=6, marker_line_width=6),1,2) # 'frontal moment', showlegend=show_legend
    

figure2.update_layout(title_text="Average Moment Peaks for a given speed and TADA angle", template='plotly')
figure2.update_layout(xaxis1_title="TADA angle (anatomical angle)", yaxis_title="Frontal Moment (N*m)")
figure2.update_layout(xaxis2_title="TADA angle (anatomical angle)", yaxis2_title="Sagittal Moment (N*m)")
#figure2.update_layout(xaxis3_title="TADA angle (anatomical angle)", yaxis3_title="Resultant Moment (N*m)")
figure2.update_layout(legend_title="Speed (m/s)")

figure_polar.update_layout(title_text="Polar plots of Average Peak Pylon Moments for various TADA angles and walking speeds", template='plotly')
figure_polar.update_layout(polar=dict(angularaxis=dict(rotation=-45, gridwidth = 10), radialaxis=dict(tickvals=[500, 1000, 1500, 2000], gridwidth = 10)), 
                           polar2=dict(angularaxis=dict(rotation=-45, gridwidth = 10), radialaxis=dict(tickvals=[250, 500, 750], gridwidth = 10)))
figure_polar.update_layout(legend=dict(title="Speed (m/s)", orientation="h",))
#figure_polar.update_layout(legend=dict(title="Speed (m/s)", orientation="h",  font=dict(size=40)))#, yanchor="bottom", y=0, xanchor="left", x=0.99))
#figure_polar.add_annotation(xref="paper", yref="paper", x=0.155, y=0.51, text="<b>Sagittal<br>Moments</b>", showarrow=False,  font=dict(size=32))
#figure_polar.add_annotation(xref="paper", yref="paper", x=0.82, y=0.51, text="<b>Frontal<br>Moments</b>", showarrow=False,  font=dict(size=32))
#figure.update_layout(legend=dict(x='slow', y='medium',z='fast'))
figure.show()
figure2.show()
#figure3.show()
figure_state.show()
figure_peaks.show()
figure_polar.show()

#bag_folder_path = r"C:\Users\the1k\source\repos\PythonApplication1\catkin_ws_remote\data\for_bags\data_kn"
bag_folder_path =r"C:\Users\aheto\Documents\research\catkin_ws\catkin_ws_remote\data\for_bags\data_kn" 
figure2.write_html(f'{bag_folder_path}/file_line.html')
figure_polar.write_html(f'{bag_folder_path}/file_polar.html')

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



