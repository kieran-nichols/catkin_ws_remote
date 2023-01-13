# !/usr/bin/env python3
import rospy
import pandas as pd
import json
import numpy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
## Plotly setup
# from https://www.geeksforgeeks.org/plot-live-graphs-using-python-dash-and-plotly/
# from https://stackoverflow.com/questions/72496810/live-update-multiple-y-axis-in-plotly-dash
# from https://stackoverflow.com/questions/63589249/plotly-dash-display-real-time-data-in-smooth-animation
# from https://gitlab.com/chambana/ros-dashboard/-/blob/master/ros_dashboard.py
# from https://www.geeksforgeeks.org/multiprocessing-python-set-2/
# form https://stackoverflow.com/questions/65321096/plotly-dash-and-callbacks-that-invoke-multiprocessing-code
import dash 
import time
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from multiprocessing import Process, Manager, freeze_support, Pool, Pipe, Queue
import functools

app = dash.Dash()#(__name__)

# Main Dash app that processes and sorts the incoming ROS data and returns the appropiate scatter data that is added to the graphs
# This callback is quicker with direct javascript code that is embedded in the triple quotations marks
app.clientside_callback(
    """
    function (n_intervals, value0, value1, value2, data_orig) {
        var obj = JSON.parse(data_orig);
        var data;
        if (obj) {
            data = [obj.y[0]/100, obj.y[1], obj.y[2], obj.y[3], obj.y[4], obj.y[5], obj.y[6], obj.y[7]];
        }
        else {
            data = [0,0,0,0,0,0,0,0];
        }
        var i = 0;
        var j = 0;
        var val0 = value0; 
        var val1 = value1;
        var val2 = value2;
        var n = n_intervals;
        var samp_freq = 1

        var x0 = data[0];
	    var x1 = data[3];
        var x2 = data[4];
        var y00 = data[val0];
        var y01 = data[val1];
        var y02 = data[val2];
        var resolution = 50;
        var y1 = data[1];
        
        var return_data = [{x:[[x0]], y:[[y1]]}, [0], resolution];

        if (val0 >= 1) {
            return_data = [{x:[[x0]], y:[[y00]]}, [0], resolution];
            var y10 = data[val0+3];
            if (x1 != 0) {   
                return_data = [{x:[[x0], [x1]], y:[[y00], [y00]]}, [0,3], resolution];
            if (y10 >= 10 ) {
                return_data = [{x:[[x0], [x1], [x2]], y:[[y00], [y00], [y10]]}, [0,3,6], resolution];
            } }
        }   
             
        return [return_data, 0]
    }
    """,
    [Output('live-graph', 'extendData')],
    [Input('graph-update', 'n_intervals'), Input("dropdown0", "value"),   Input("dropdown1", "value"),  Input("dropdown2", "value"), State('store', 'children')]#, State('storage', 'data')]
) 

# Seondary callback function for ROS which Dash calls and it includes the fast_ros_dict_to_json, callback and init_variables functions
@app.callback(Output('store', 'children'), Input('graph-update', 'n_intervals')) # )

def fast_ros_dict_to_json(n_intervals): # try using Store to store the extra shared_dicts and n to eventually plot
    #n = n_intervals%20;
    #print(n)
    #return json.dumps(dict({"shared":shared_dict},{"index":n})) # trying to find way to combine the ros messages that are read 20 times before the scatter is rendered
    return json.dumps(dict(shared_dict)) # float and int are json compatible

def callback(data, shared_dict): # needed to convert to python float # this function is called at the publisher's freq (100 Hz)
    shared_dict["y"] = [int(data.data[0]),float(data.data[1]),float(data.data[4]),float(data.data[7]),float(data.data[8]),float(data.data[11]),float(data.data[0]),200] # [1,2,3,4,5,6,7,8]
    #rospy.loginfo(rospy.get_caller_id()) # to check the subscribe time stamps for the sampling freq

def init_variables(shared_dict): # set up ROS subscibers
    rospy.init_node('listener', anonymous=True)
    #rospy.Rate(10).sleep()  ## no need for setting the rate it gets called according to the publisher; it seems to be a little funky if I set the rate    
    rospy.Subscriber('chatter', numpy_msg(Floats), callback, shared_dict) # added on shared_dict as an optional callback_arg parameter 
    #callback(0,shared_dict)
    rospy.spin()

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
        html.Div(
	        [
                html.Label('TADA Graphical Display',style={'paddingTop': '2rem'}),
                html.Div(children=[
                    html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown0")],style={"width": "33%"}),
                    html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0},{"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}], value=0,id="dropdown1")],style={"width": "33%"}),
                    html.Div(children=[dcc.Dropdown(options = [{"label": "empty", "value": 0}, {"label": "ankle_angle", "value": 1}, {"label": "imu_ang_vel", "value": 2}],value=0, id="dropdown2")],style={"width": "33%"} )]
                  , style=dict(display='flex')), 
                dcc.Graph(id = 'live-graph', figure=figure),
		        dcc.Interval(id = 'graph-update', interval = 200, n_intervals = 0), # 200ms seems to be the fastest with ROS; interval does not work reliably under 50 ms giving 20 Hz samp_freq, the fastest samp_freq seems to be 22 Hz
                dcc.Store(id='storage', data=[0])  ,
	            html.Div(id='store', style={'display': 'none'})#, data=dict(shared_dict))
            ]
        )
    )

if __name__ == '__main__':
    ## Create shared memory handled by a different processor for the ROS subscribers
    manager = Manager()
    resolution = 50
    shared_dict = manager.dict()
    shared_dict["y"] = [0,1,1,1,1,1,1,50]

    # Set up the Dash graphing layout
    setup_dash_app(shared_dict)

    # Give a separate process to the ROS subsibers
    p1 = Process(target=init_variables, args=(shared_dict,))
    p1.start()#; p1.join()
    #init_variables()

    # Run the Dash app using app.run
    #app.run(debug=True, threaded=True, processes=1) # threaded true not good for multi processing
    app.run(debug=True) #, host='0.0.0.0') # seemed to be same speed and settings as above
    # setting debug to false does not seem to speed up the program  

# Extra code and notes  
    # for the second and 3rd scatters
        #if (val1 >= 1) {
        #    return_data = [{x:[[x0]], y:[[y01]]}, [0], resolution];
        #    var y10 = data[val1+3][n];
        #    if (x1 != 0) {   
        #        return_data = [{x:[[x0], [x1]], y:[[y01], [y01]]}, [0,4], resolution];
        #    }
             
        #    if (y3 >= 10 ) {
        #        return_data = [{x:[[x0], [x2]], y:[[y01], [y10]]}, [0,7], resolution];
        #    }
        #} 
             
        #return [return_data, 0]

#@functools.lru_cache(maxsize=32) # does not seem to help
