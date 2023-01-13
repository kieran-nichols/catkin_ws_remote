# !/usr/bin/env python3
import rospy
from std_msgs.msg import String, Bool
from std_msgs.msg import Float32MultiArray
from rospy.numpy_msg import numpy_msg
import pandas as pd
import json
import numpy
from rospy_tutorials.msg import Floats
from collections import deque
## Plotly setup
# from https://www.geeksforgeeks.org/plot-live-graphs-using-python-dash-and-plotly/
# from https://stackoverflow.com/questions/72496810/live-update-multiple-y-axis-in-plotly-dash
# from https://stackoverflow.com/questions/63589249/plotly-dash-display-real-time-data-in-smooth-animation
# from https://gitlab.com/chambana/ros-dashboard/-/blob/master/ros_dashboard.py
# from https://www.geeksforgeeks.org/multiprocessing-python-set-2/
# form https://stackoverflow.com/questions/65321096/plotly-dash-and-callbacks-that-invoke-multiprocessing-code
import dash 
import time
import multiprocessing
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from multiprocessing import Process, Manager, freeze_support, Pool, Pipe, Queue
import functools
import dash_daq as daq
from dash_extensions import Download
#from dash_extensions.snippets import send_file

time = deque(maxlen = 50)
X = deque(maxlen = 50)
#X.append(0)
Y = deque(maxlen = 50)
#Y.append(0)

app = dash.Dash()#(__name__)

# Main Dash app that processes and sorts the incoming ROS data and returns the appropiate scatter data that is added to the graphs
# This callback is quicker with direct javascript code that is embedded in the triple quotations marks

@app.callback(
    [Output('live-graph', 'extendData'),],
    [Input('graph-update', 'n_intervals'), Input("dropdown0", "value"),   Input("dropdown1", "value"),  Input("dropdown2", "value"), State('store', 'children'),]
    )

def update_graph_scatter(n_intervals, val0, val1, val2, data):    
    resolution = 1000    
    #print(data )
    #x0 = [x/100 for x in data["x"]] # issue with itr type error # data["x"]
    x0 = data["time"]
    
    if val0==1:
        y0 = data["x"]
    else:    
        y0 = data["y"]

    return [[dict(x=[x0], y=[y0]), [0], resolution]]

# Seondary callback function for ROS which Dash calls and it includes the fast_ros_dict_to_json, callback and init_variables functions
@app.callback([ Output('store', 'children')],
              [Input('graph-update', 'n_intervals')])

def fast_ros_dict_to_json(n_intervals):#, on, value): # try using Store to store the extra shared_dicts and n to eventually plot
    #print(shared_dict)
    return [dict(shared_dict)]#, f'Data is being recorded: {on}.', f'Notes taken: {value}' # need to return as list (rolleyes)

def callback(data, args): #shared_dict, X, Y): # needed to convert to python float # this function is called at the publisher's freq (100 Hz)
    args[1].append(data.data[0])
    args[2].append(data.data[1])
    args[3].append(rospy.Time.now().secs%60)
    args[0]["x"] = list(args[1])
    args[0]["y"] = list(args[2])
    args[0]["time"] = list(args[3])
    #print(args[0]["x"])
    
def init_variables(shared_dict): # set up ROS subscibers
    rospy.init_node('listener', anonymous=True)
    # ROS subscriber to collect compiled data array from data processing node  
    #rospy.Subscriber('chatter', numpy_msg(Floats), callback, (shared_dict, X, Y)) # added on shared_dict as an optional callback_arg parameter 
    rospy.Subscriber('processed_data', numpy_msg(Floats), callback, (shared_dict, X, Y, time)) 
    rospy.spin()

# Seondary callback function for ROS 
#@app.callback([ Output('power-button-result-1', 'children'), Output("notes-result", "children"), Output('storage', 'data')], # somehow string takes a lot of bandwidth
@app.callback([ Output('storage', 'data')],
              [ Input('our-power-button-1', 'on'), Input('notes-input','value')], prevent_initial_call=True) 

def print_recording_info(on, value):
    #return (f'Data is being recorded: {on}.', f'Notes taken: {value}', record.put(int(on))) # somehow string takes a lot of bandwidth
    #return (notes.put(value), record.put(int(on)))
    return (record.put(int(on)))

# high-level callback for input widgets
@app.callback(
    [Output('theta-gauge', 'value'), Output('Theta', 'value'), Output('Theta_num', 'value'), Output('alpha-gauge', 'value'), Output('Theta-result', 'children'), Output('dropdown_kill-result', 'children'),],
    [Input('Theta', 'value'), Input('Theta_num', 'value'), Input('Alpha', 'value'), Input('motor_torque', 'on'), Input('dropdown_kill', 'value')], 
     prevent_initial_call=True
    )
def update_output(value4, value3, value1, on, value2): #, value3): 
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    value = value4 if trigger_id == "Theta" else value3
    return (value, value, value, value1, f'Theta: {value},  Alpha: {value1}.', f'Killed {value2} node.')

## need a separate callback for downloading
#@app.callback( # not working
#    Output("download", "data"),
#    Input("btn", "n_clicks"),
#     prevent_initial_call=True
#    )
#def update_output(n_clicks, on): #, value3): 
#    return (dict(content="Hello world!", filename="hello.txt")) #send_file("C:/Users/the1k/Documents/TADA_data/Untitled.png"))

def init_publisher(record): # ,notes):
    rospy.init_node('talker_record', anonymous=True)
#    # ROS publisher that sends a true or false value to the talker node to start or stop the talker node
    pub = rospy.Publisher('chatter_control', numpy_msg(Floats), queue_size=10)
    #pub1 = rospy.Publisher('chatter_control1', String, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rec = record.get()
        if rec==1: 
            pub_data = 1
            #pub_data1 = notes
        else: 
            pub_data = 0
            #pub_data1 = ''
        #print(rec)
        pub_array = numpy.array([pub_data], dtype=numpy.float32)
        pub.publish(pub_array)
        #pub1.publish(pub_data1)
        rate.sleep()  

# Function for setting up the Dash graphical layout
def setup_dash_app(shared_dict):
    trace1 = go.Scatter(x=[], y=[], mode= 'lines')
    trace2 = go.Scatter(x=[], y=[], mode= 'markers')
    trace3 = go.Scatter(x=[], y=[], mode= 'markers')
    figure = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.15, horizontal_spacing=0.009)
    figure['layout'].update(height=600)                    
    figure.add_trace(trace1, 1, 1)
    figure.add_trace(trace1, 1, 1)
    figure.add_trace(trace1, 1, 1) # three of the same traces to allow for up to 3 plots on the real time graph
    figure.add_trace(trace2, 2, 1)
    figure.add_trace(trace2, 2, 1)
    figure.add_trace(trace2, 2, 1)
    figure.add_trace(trace3, 3, 1)
    figure.add_trace(trace3, 3, 1)
    figure.add_trace(trace3, 3, 1)

    figure['layout']['xaxis']['title']='Real-time'
    figure['layout']['yaxis']['title']='TADA Metric'
    figure['layout']['xaxis2']['title']='Stride frame number'
    figure['layout']['yaxis2']['title']='TADA Metric'
    figure['layout']['xaxis3']['title']='TADA Ankle Angle'
    figure['layout']['yaxis3']['title']='TADA Metric'
    figure = figure

    app.layout = html.Div(
               # Graphing
                html.Div(
                    [
                    html.Div(children=[ html.Div([html.Label('TADA Graphical Display')],style={'paddingTop': '1rem','paddingBottom': '1rem', 'textAlign': 'center'})]),
                     # Input widgets
                    html.Div(children=[ html.Div([daq.BooleanSwitch(id='motor_torque', on=False, label='Motor Torque', labelPosition="top")],style={"width": "33%"}),
                                        html.Div([daq.BooleanSwitch(id='kill_system', on=False, label='Kill System', labelPosition="top")],style={"width": "33%"}),
                                        html.Div([daq.BooleanSwitch(id='calibrate', on=False, label='Calibrate', labelPosition="top")],style={"width": "33%"})], 
                             style=dict(display='flex',paddingBottom='1rem'), ), 

                    html.Div(children=[ html.Div([dcc.Dropdown(['None', 'Motor', 'IMU', 'Europa', 'Xsens', 'Data processing', 'All'], 'None', id='dropdown_kill'), html.Div(id='dropdown_kill-result') ], style={"width": "100%", 'textAlign': 'center'}),],style=dict(display='flex',paddingBottom='1rem')), 
                    
                    html.Div(children=[ html.Div([html.Button('Home', id='home')],style={"width": "50%"}),  html.Div([html.Button('Rehome', id='rehome')],style={"width": "50%"}),],
                             style=dict(display='flex',paddingBottom='1rem'), ),
                    
                    html.Div([ html.Div(id='Theta-result'),],style={'textAlign': 'center','paddingBottom':'0rem'}),
                    html.Div(children=[
                        # slider or numeric input
                        html.Div([ dcc.Slider(id='Theta', value=0, min=0, max=10), dcc.Input(id='Theta_num', type='number',value=0, min=0, max=10, debounce=False), # wait until input in parallel, mostly on alpha
                                  daq.Gauge(id='theta-gauge', label='Theta', min=0, max=10)],style={"width": "50%", 'textAlign': 'center'}),
                        html.Div([ dcc.Slider(id='Alpha', value=0, min=-180, max=180, step=45), #daq.NumericInput(id='Alpha', value=0, min=0, max=180), #marks={180,-135,-90,-45,0,45,90,135,180}
                                  daq.Gauge(id='alpha-gauge', label='Alpha', min=-180, max=180) ],style={"width": "50%", 'textAlign': 'center'}),
                        ],style=dict(display='flex')), 
                    
                    html.Div(children=[ html.Div([dcc.Dropdown(['None', 'Static', 'Adaptive (Moment)'], 'None', id='TADA_mode'), html.Div(id='tada_mode-result') ], style={"width": "100%", 'textAlign': 'center'}),],style=dict(display='flex',paddingBottom='1rem')),                     
                    
                    #html.Div([html.Button("Download", id="btn"), Download(id="download")]),
                    html.Div( children= [
                              html.Div(children=[html.Div(id='power-button-result-1'), daq.PowerButton(id='our-power-button-1', on=False, label='Record' )],  style={"width": "50%", 'paddingBottom':'1rem'}),
                              html.Div(children=[html.I("Notes"), dcc.Textarea(rows=3, id="notes-input", placeholder=""), html.Div(id='notes-result')], style={"width": "50%",'paddingBottom':'1rem'}),
                                 ], style=dict(display='flex')), 

                    html.Div(children=[
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown0")],style={"width": "33%"}),
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0},{"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}], value=0,id="dropdown1")],style={"width": "33%"}),
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown2")],style={"width": "33%"} )
                        ]
                        , style=dict(display='flex')), 
                    
                    dcc.Graph(id = 'live-graph', figure=figure),
		            dcc.Interval(id = 'graph-update', interval = 500, n_intervals = 0), # 200ms seems to be the fastest with ROS; interval does not work reliably under 50 ms giving 20 Hz samp_freq, the fastest samp_freq seems to be 22 Hz
                    dcc.Store(id='storage', data=[0])  ,
                    dcc.Store(id='store', data=dict(shared_dict))  ,
	                #html.Div(id='store', style={'display': 'none'}),#, data=dict(shared_dict))
                    ],  
                )
            )

if __name__ == '__main__':
    ## Create shared memory handled by a different processor for the ROS subscribers
    manager = Manager()
    resolution = 50
    shared_dict = manager.dict()
    #shared_dict["z"] = [0,1,1,1,1,1,1,50]
    #shared_dict["x"] = [0]
    #shared_dict["y"] = [0]
    
    # Create a queue to share data between the processes
    record = Queue(maxsize=1)
    record.put(0)
    #print("record", record.get())
    #notes = Queue(maxsize=20) # failed attempt at creating a queue for notes; may visit if I have spare time
    #notes.put('')

    # Set up the Dash graphing layout
    setup_dash_app(shared_dict)

    # Give a separate process to the ROS subsibers
    p1 = Process(target=init_variables, args=(shared_dict,))
    p1.start()#; p1.join()
    #init_variables()
    
    p2 = Process(target=init_publisher, args=(record,)) #notes,))
    p2.start()#; p1.join()
    #init_publisher()

    # Run the Dash app using app.run
    app.run(debug=True, host='0.0.0.0') # seemed to be same speed and settings as above # setting debug to false does not seem to speed up the program  
    #p3 = Process(target=app.run(debug=True))#, args=(record,))
    #p3.start()
