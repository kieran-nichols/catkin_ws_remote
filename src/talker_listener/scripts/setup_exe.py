# !/usr/bin/env python3

from distutils.core import setup
import py2exe

import pandas as pd
import json
import numpy as np
from collections import deque
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
import dash_bootstrap_components as dbc
from dash_extensions import Download

setup(console=['listener_control_no_ros.py'])
