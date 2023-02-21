# !/usr/bin/env python3
import numpy as np
from collections import deque
import dash 
import time
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_daq as daq
import dash_bootstrap_components as dbc

time1 = deque(maxlen = 50)
X = deque(maxlen = 50)
Y = deque(maxlen = 50)

def TADA_angle(inclination_angle_deg, alpha_deg):
    # code to solve plantarflexion and eversion angles for TADA foot
    # theta: foot inclination angle; desired downward inclination angle
    # alpha: downward direction vector: atan(f/c) where f is plantarflexion angle and
    # c is eversion angle, beta: wedge angle: 5 deg, solve for q1 and q5

    theta = inclination_angle_deg*np.pi/180; 
    beta = 5*np.pi/180; # fixed
    q3 = 2*np.real(np.arccos(np.sin(theta/2)/np.sin(beta))); 
    alpha = alpha_deg * np.pi/180;
    Motor1_angle_unwrapped = 180/np.pi*(alpha - np.arctan2(np.tan(q3/2),np.cos(beta)));
    Motor2_angle_unwrapped = 180/np.pi*(-(alpha + np.arctan2(np.tan(q3/2),np.cos(beta)))); 
    
    Motor1_angle = (Motor1_angle_unwrapped  + 180) % ( 360 ) - 180
    Motor2_angle = (Motor2_angle_unwrapped  + 180) % ( 360 ) - 180
    
    q1 = Motor1_angle*np.pi/180;
    q5 = Motor2_angle*np.pi/180;
    q2 = np.pi/36; q4 = q2;
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
    
    Plantarflexion_angle = 180/np.pi*R05[0,2];
    Eversion_angle = 180/np.pi*R05[1,2];
    return (Plantarflexion_angle, Eversion_angle)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])#(__name__)

# Main Dash app that processes and sorts the incoming ROS data and returns the appropiate scatter data that is added to the graphs
# high-level callback for input widgets
@app.callback(
    [ Output('polar-graph', 'extendData'), Output('Theta', 'value'), Output('theta-gauge', 'value'), Output('Theta_num', 'value'),  Output('Alpha', 'value'), Output('alpha-gauge', 'value'), Output('Alpha_num', 'value'),],# 
    [ Input('our-power-button-1', 'on'), Input('Theta', 'value'), Input('Theta_num', 'value'), Input('Alpha', 'value'), Input('Alpha_num', 'value'), Input('dropdown_kill', 'value'), State('notes-input', 'value')], 
     prevent_initial_call=True
    )

def update_output(on, value4, value3, value1, value0, value2, note): #, value3): 
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    theta1 = value4 if trigger_id == "Theta" else value3
    alpha1 = value1 if trigger_id == "Alpha" else value0
    record.put(int(on)) if trigger_id == "our-power-button-1" else record.put(int(on))
    notes.put(note) if trigger_id == "our-power-button-1" else notes.put(note)
    angle.put(alpha1)
    angle.put(theta1)
    
    (Plantarflexion_angle, Eversion_angle) = TADA_angle(theta1,alpha1)
    polar_info = [dict(x=[[Eversion_angle]], y=[[Plantarflexion_angle]]), [0], 10]
    return (polar_info, theta1, theta1, theta1, alpha1, alpha1, alpha1) 

def init_publisher(record,angle,notes): 

    while True:
        rec = record.get()
        note = notes.get()
        if rec==1: 
            pub_data = 1
            pub_data1 = note
        else: 
            pub_data = 0
            pub_data1 = ''
        
        alpha1 = angle.get()
        theta1 = angle.get()
        time.sleep(0.1)

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
    
    figure_polar = go.Figure()
    figure_p = go.Scatter(x=[0], y=[0], mode= 'markers', name='Polar graph')
    figure_polar.add_trace(figure_p)
    figure_polar['layout']['yaxis']['range']=[-10, 10]
    figure_polar['layout']['xaxis']['range']=[-10, 10]

    app.layout = html.Div(
               # Graphing
                html.Div(
                    [
                    html.Div(children=[ html.Div([html.Label('TADA Graphical Display')],style={'paddingTop': '1rem','paddingBottom': '1rem', 'textAlign': 'center'})]),
                     # Input widgets
                    html.Div(children=[ html.Div([daq.BooleanSwitch(id='motor_torque', on=False, label='Motor Torque', labelPosition="top")],style={"width": "33%"}),
                                        #html.Div([html.Button('Rehome', id='rehome'), html.Button('Home', id='home')],style={"width": "33%"}),
                                        html.Div([dbc.Button('Rehome', id='rehome', className="me-md-2", size='sm'), dbc.Button('Home', id='home', className="me-md-2", size='sm'),],
                                        className="d-grid gap-2 d-md-flex justify-content-md-center", style={"width": "33%"}),
                                        html.Div([daq.BooleanSwitch(id='calibrate', on=False, label='Calibrate', labelPosition="top")],style={"width": "33%"})], 
                             style=dict(display='flex',paddingBottom='1rem'), ), 
                    
                    html.Div(children=[ html.Div([dcc.Dropdown(['None', 'Motor', 'IMU', 'Europa', 'Xsens', 'Data processing', 'All'], 'None', id='dropdown_kill'), html.Div(id='dropdown_kill-result') ], 
                                                 style={"width": "100%", 'textAlign': 'center'}),],style=dict(display='flex',paddingBottom='1rem')), 
                    
                    html.Div([ html.Div(id='Theta-result'),],style={'textAlign': 'center','paddingBottom':'0rem'}),
                    html.Div(children=[
                        # slider or numeric input
                        html.Div([ dcc.Slider(id='Theta', value=0, min=0, max=10, updatemode='drag'),
                                  dcc.Input(id='Theta_num', type='number',value=0, min=0, max=10, debounce=False), #daq.Knob(id='Theta', value=0, min=0, max=10)]# knob does not have instantaneous updates like how the slider has drag updates
                                  daq.Gauge(id='theta-gauge', label='Theta', min=0, max=10, size=200)],
                                  style={"width": "33%", 'textAlign': 'center'}),
                        
                        html.Div([dcc.Graph(id = 'polar-graph', figure=figure_polar)], style={"width": "33%"}),
                        
                        html.Div([ dcc.Slider(id='Alpha', value=0, min=-180, max=180, updatemode='drag'),  
                                  dcc.Input(id='Alpha_num', type='number',value=0, min=-180, max=180, debounce=False), #daq.Knob(id='Alpha', value=0, min=-180, max=180),]
                                  daq.Gauge(id='alpha-gauge', label='Alpha', min=-180, max=180, size=200) ]  
                                 ,style={"width": "33%", 'textAlign': 'center'}),
                        ],style=dict(display='flex')), 
                    
                    html.Div(children=[ html.Div([dcc.Dropdown(['None', 'Static', 'Adaptive (Moment)'], 'None', id='TADA_mode'), html.Div(id='tada_mode-result') ], style={"width": "100%", 'textAlign': 'center'}),],
                             style=dict(display='flex',paddingBottom='1rem')),                     
                    
                    #html.Div([html.Button("Download", id="btn"), Download(id="download")]),
                    html.Div( children= [
                              html.Div(children=[html.Div(id='power-button-result-1'), daq.PowerButton(id='our-power-button-1', on=False, label='Record')],  style={"width": "50%", 'paddingBottom':'1rem'}),
                              html.Div(children=[dcc.Textarea(rows=3, id="notes-input", placeholder="Notes"), html.Div(id='notes-result')], style={"width": "50%",'paddingBottom':'1rem'}),
                                 ], style=dict(display='flex')), 

                    html.Div(children=[
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown0")],style={"width": "33%", 'textAlign': 'center'}),
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0},{"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}], value=0,id="dropdown1")],style={"width": "33%", 'textAlign': 'center'}),
                        html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown2")],style={"width": "33%", 'textAlign': 'center'} )
                        ]
                        , style=dict(display='flex')), 
                    
                    dcc.Graph(id = 'live-graph', figure=figure),
		            dcc.Interval(id = 'graph-update', interval = 500, n_intervals = 0), # 200ms seems to be the fastest with ROS; interval does not work reliably under 50 ms giving 20 Hz samp_freq, the fastest samp_freq seems to be 22 Hz
                    dcc.Store(id='storage', data=[0])  ,
                    dcc.Store(id='storage_theta_alpha', data=[0])  ,
                    dcc.Store(id='store', data=dict(shared_dict))  ,
                    ],  
                )
            )

if __name__ == '__main__':
    ## Create shared memory handled by a different processor for the ROS subscribers
    #manager = Manager()
    #resolution = 50
    shared_dict = dict() # manager.dict()
    
    # Create a queue to share data between the processes
    #record = Queue(maxsize=1)
    #record.put(0)
    #angle = Queue(maxsize=2)
    #angle.put(0)
    #angle.put(0)
    #notes = Queue()
    #notes.put('0')
    record = 0
    angle = [0,0]
    notes= '0'

    # Set up the Dash graphing layout
    setup_dash_app(shared_dict)
    
    # Give a separate process to the ROS publishers
    #p2 = Process(target=init_publisher, args=(record,angle,notes,))
    #p2.start()#; p1.join()
    #init_publisher()

    # Run the Dash app using app.run
    app.run(debug=True, host='0.0.0.0') # seemed to be same speed and settings as above # setting debug to false does not seem to speed up the program  
    #p3 = Process(target=app.run(debug=True))#, args=(record,))
    #p3.start()
