# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 19:50:47 2021

@author: spenc
"""

import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

import random as rand  
import math, time
import pandas as pd  # note that this is the accepted community naming convention to import pandas
import numpy as np
import matplotlib.pyplot as plt
from plot_in_KML import *

from Coord import Coord
from Merchant_Ship import *
from Fishing_Ship import Fishing_Ship
from Submarine import *
from Location_Getter import A, B, C, Fishing, Submarine_Start # need to pair with function that creates data from KML

def start_location():
    '''Generate starting location for each ship'''
    random_start_variable = rand.random()
    if random_start_variable < 0.5:
        return Coord(A.lat + rand.random()/250,A.lon + rand.random()/250)
    else:
        return Coord(C.lat + rand.random()/250,C.lon + rand.random()/250)

# Time related functions for plotting. Variable b is max allowed time to pass for simulation
b = 100
t = float(time.time())
t_max = float(time.time()) + b
t_plotting = {}

#Create a list of ships for later class-object creation
ships_list = []
number_of_merchant_ships = 3
merchant_ship_generic_name = 'Merch_'
i = 1
while i <= number_of_merchant_ships:
    name = merchant_ship_generic_name + str(i)
    ships_list.append(name)
    t_plotting[name] = []
    i += 1

# Data storage dictionaries. ships_dict holds all created merchants, data used for plotting
data = {}
ships_dict = {}
for ships in ships_list:
    pause_time = 0
    '''Create Merchants'''
    ships_dict[ships] = Merchant_Ship(start_location(), wait = pause_time)
    pause_time += 120
    
    # Populate dictionary with working keys for sonar display
    merchant_plot_key_brg = 'BRG'
    
    merch_key_building_string_brg = merchant_plot_key_brg + '_' + str(ships)
    data[merch_key_building_string_brg] = []
        
# Create submarine
submarine = Submarine(Submarine_Start,crs = 95,spd = 1000)

#### Begin webpage

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Submarine Game'),
        html.Div(id='live-update-text'),
        dcc.Input(id='my-crs', value=90, type='text'),
        dcc.Input(id='my-depth', value=150, type='text'),
        dcc.Graph(id = 'live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

# End webpage, begin callback functions

# For ownship's infomration and changes to parameters of submarine
@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'),
              Input(component_id='my-crs', component_property='value'),
              Input(component_id='my-depth', component_property='value'))
def update_data(n,crs,depth):
    style = {'padding': '5px', 'fontSize': '16px'}
    
    for ships in ships_list:
        # Update position of Merchant Shipping
        ships_dict[ships].update_position(ships_dict[ships].spd)
        
    # Update position, course, and depth of submarine. 
    submarine.update_position(submarine.crs)
    sub_crs = int(crs)
    sub_depth = int(depth)
    submarine.change_crs(sub_crs)
    submarine.change_depth(sub_depth)
    
    return [
        html.Span('lat: {}'.format(str(submarine.loc.lat)), style=style),
        html.Span('lon: {}'.format(str(submarine.loc.lon)), style=style),
        html.Span('crs: {}'.format(str(submarine.crs)), style=style),
        html.Span('depth: {}'.format(str(submarine.depth)), style=style)
    ]



# Sonar "waterfall" dispaly
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'),
              Input(component_id='my-crs', component_property='value'))
def update_graph_live(n,crs):
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    
    for ship in ships_list:
        #populate figure with each ship's new information
        merch_key_building_string_brg = merchant_plot_key_brg + '_' + str(ship)
        
        #time related aritmatic for plotting
        t = round(t_max - float(time.time()))
        t = b - t
        t_plotting[ship].append(t)
        
        # Merchant relative bearing plotting
        data[merch_key_building_string_brg].append(submarine.loc.bearing(ships_dict[ship].loc))
        
        
        fig.append_trace({
            
            'x': data[merch_key_building_string_brg],
            'y': t_plotting[ship],
            'name': 'sub',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)


    return fig




### Plot submarine maybe use this to plot pd stuff
# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(n):
#     data = {
#         'Latitude': [],
#         'Longitude': [],
#     }

#     # Collect some data
#     data['Longitude'].append(submarine.loc.lon)
#     data['Latitude'].append(submarine.loc.lat)


#     # Create the graph with subplots
#     fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
#     fig['layout']['margin'] = {
#         'l': 30, 'r': 10, 'b': 30, 't': 10
#     }
#     fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

#     fig.append_trace({
#         'x': data['Longitude'],
#         'y': data['Latitude'],
#         'name': 'sub',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)


#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    
    # Create function to plot all tracks in KML once user presses "stop" or something





