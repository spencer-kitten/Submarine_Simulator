# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 19:50:47 2021

@author: spenc

http://127.0.0.1:8050/
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
from Location_Getter import Location_Dictionary
from plot_in_KML import *

def start_location():
    '''Generate starting location for each ship'''
    random_start_variable = rand.random()
    if random_start_variable < 0.5:
        return Coord(Location_Dictionary['A'].lat + rand.random()/250,Location_Dictionary['A'].lon + rand.random()/250)
    else:
        return Coord(Location_Dictionary['C'].lat + rand.random()/250,Location_Dictionary['C'].lon + rand.random()/250)

# Time related functions for plotting. Variable b is max allowed time to pass for simulation
b = 100000
t = float(time.time())
t_max = float(time.time()) + b
t_plotting = {}


#Create a list of ships for later class-object creation
ships_list = []
number_of_merchant_ships = 5
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



# Create list of fishing ships
fishing_list = []
fishing_dict = {}
number_of_fishing_ships = 3
fishing_ship_generic_name = 'Fishing_'
i = 1
while i <= number_of_fishing_ships:
    fname = fishing_ship_generic_name + str(i)
    fishing_list.append(fname)
    t_plotting[fname] = []
    i += 1

# Populate dictionary with fishing vessles
for fships in fishing_list:
    '''Create Fishing Vessels'''
    fishing_dict[fships] = Fishing_Ship(Location_Dictionary['Fishing'])
    
    # Populate dictionary with working keys for sonar display
    fishing_plot_key_brg = 'BRG'
    fish_key_building_string_brg = fishing_plot_key_brg + '_' + str(fships)
    data[fish_key_building_string_brg] = []
    
# Plotting in KML 
plotting_merchants = {}
plotting_fishing = {}
plotting_submarine = []

        
# Create submarine
submarine = Submarine(Location_Dictionary['Submarine_Start'],crs = 90,spd = 12)

#### Begin webpage

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('USS Lubbock (SSN-806)'),
        html.Div(id='live-update-text'),
        dcc.Input(id='my-crs', value=90, type='text'),
        dcc.Input(id='my-spd', value=12, type='text'),
        dcc.Input(id='my-depth', value=150, type='text'),
        dcc.Graph(id = 'live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=3*1000, # in milliseconds
            n_intervals=0
    
        ),
        dcc.Store(id= 'Data', data = data),
        html.Label(id = 'run'),
        # dcc.RadioItems(
        #     options=[
        #         {'label': 'Run Simulation', 'value': 'RUN'},
        #         {'label': 'Stop Simulation', 'value': 'STOP'}
        #     ],
        #     value='RUN'
        #     ),
    ])
)

# End webpage, begin callback functions

# For ownship's infomration and changes to parameters of submarine
@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'),
              Input(component_id='my-crs', component_property='value'),
              Input(component_id='my-spd', component_property='value'),
              Input(component_id='my-depth', component_property='value'))
def update_data(n,crs,spd,depth):
    style = {'padding': '5px', 'fontSize': '16px'}
    global ships_list
    global submarine
    for ships in ships_list:
        # Update position of Merchant Shipping
        ships_dict[ships].update_position(ships_dict[ships].spd)
        
    for fships in fishing_list:
        # Update position of Fishing Ship 
        fishing_dict[fships].update_position(fishing_dict[fships].crs)
        
    # Update position, course, and depth of submarine. 
    submarine.update_position(submarine.crs)
    sub_crs = int(crs)
    sub_spd = int(spd)
    sub_depth = int(depth)
    submarine.change_crs(sub_crs)
    submarine.change_depth(sub_depth)
    submarine.change_speed(sub_spd)
    range_to_tgt1 = submarine.loc.dist_to(ships_dict['Merch_1'].loc)       
    return [
        html.Span('lat: {}'.format(str(submarine.loc.lat)), style=style),
        html.Span('lon: {}'.format(str(submarine.loc.lon)), style=style),
        html.Span('crs: {}'.format(str(submarine.crs)), style=style),
        html.Span('spd: {}'.format(str(submarine.spd)), style=style),
        html.Span('depth: {}'.format(str(submarine.depth)), style=style)
        
    ]



# Sonar "waterfall" dispaly
@app.callback(Output('live-update-graph', 'figure'),
              #Output('Data', 'data'),
              Input('interval-component', 'n_intervals'),
              Input(component_id='my-crs', component_property='value'),
              Input(component_id='run', component_property='value'))
def update_graph_live(n,crs,run):
    # Create the graph with subplots

    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.update_layout(xaxis_range=[-180,180])
    
    
    for ship in ships_list:
    
        #populate figure with each ship's new information
        merch_key_building_string_brg = merchant_plot_key_brg + '_' + str(ship)
        
        # Merchant relative bearing plotting
        true_bearing = submarine.loc.bearing(ships_dict[ship].loc)
        relative_bearing = submarine.loc.rel_bearing_to(submarine.crs,true_bearing)
    
        data[merch_key_building_string_brg].append(relative_bearing)
        
        #time related aritmatic for plotting
        t = round(t_max - float(time.time()))
        t = b - t
        t_plotting[ship].append(t)
        
        fig.append_trace({
            
            'x': data[merch_key_building_string_brg],
            'y': t_plotting[ship],
            'name': true_bearing,
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
        if len(t_plotting[ship]) > 61:
            fig.update_layout(yaxis_range=[t_plotting[ship][-60],t])
        
        # Plotting merchants in KML
        global plotting_merchants
        if ship not in plotting_merchants:
            plotting_merchants[ship] = []
        plotting_merchants[ship].append((ships_dict[ship].loc.lon,ships_dict[ship].loc.lat))


    for fships in fishing_list:
        #populate figure with each ship's new information
        fish_key_building_string_brg = merchant_plot_key_brg + '_' + str(fships)
        
        # Merchant relative bearing plotting
        true_bearing = submarine.loc.bearing(fishing_dict[fships].loc)
        relative_bearing = submarine.loc.rel_bearing_to(submarine.crs,true_bearing)
        
        data[fish_key_building_string_brg].append(relative_bearing)
        
        t = round(t_max - float(time.time()))
        t = b - t
        t_plotting[fships].append(t)
        
        fig.append_trace({
            
            'x': data[fish_key_building_string_brg],
            'y': t_plotting[fships],
            'name': true_bearing,
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
        if len(t_plotting[fships]) > 21:
            fig.update_layout(yaxis_range=[t_plotting[fships][-20],t])
 
        #Plotting fishing in KML
        global plotting_fishing
        if fships not in plotting_fishing:
                plotting_fishing[fships] = []
        plotting_fishing[fships].append((fishing_dict[fships].loc.lon,fishing_dict[fships].loc.lat))
    
    
    # Store coordinates of submarine for KML plotting
    global plotting_submarine
    plotting_submarine.append((submarine.loc.lon,submarine.loc.lat))
    loc = str(submarine.loc)
    
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
    
    # Create function to plot all tracks in KML once user presses "stop" or something





