# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:15:34 2021

@author: spenc
Uncomment Lines 234 and 235 to run in real time.
"""


# Current issues:, doesnt display anything, user input 

import random as rand  
import math, time
import pandas as pd  # note that this is the accepted community naming convention to import pandas
import numpy as np
import matplotlib.pyplot as plt
from plot_in_KML import *


   
def start_location():
    '''Generate starting location for each ship'''
    random_start_variable = rand.random()
    if random_start_variable < 0.5:
        return Coord(A.lat + rand.random()/250,A.lon + rand.random()/250)
    else:
        return Coord(C.lat + rand.random()/250,C.lon + rand.random()/250)
    
def bearing_to_rads(crs):
    '''Converts nautical bearing to unit circle radians'''
    # I don't even end up using this
    if crs == 360:
        crs = 0
        
    if crs < 90:
        crs = (math.pi/180)*(90-crs)
    elif crs == 90:
        crs = (math.pi/180)*0
    elif crs >90 and crs < 180:
        crs = (math.pi/180)*(360 - (crs - 90))
    elif crs == 180:
        crs = (math.pi/180)*(270)
    elif crs > 180 and crs < 270:
        crs = (math.pi/180)*(180 + 90 - (crs - 180))
    elif crs == 270:
        crs = (math.pi/180)*180
    elif crs > 270 and crs < 360:
        crs = (math.pi/180)*(360 - crs + 90)
    else:
        crs = (math.pi/180)*90
    
    return crs
    

if __name__ == "__main__":
    
########### find a way to import from kml...
    from Coord import Coord
    from Merchant_Ship import *
    from Fishing_Ship import Fishing_Ship
    from Submarine import Submarine
    from Location_Getter import A, B, C, Fishing, Submarine_Start # need to pair with function that creates data from KML

    # Populate Merchant List
    ships_list = []
    number_of_merchant_ships = 50
    merchant_ship_generic_name = 'Merch_'
    i = 1
    while i <= number_of_merchant_ships:
        name = merchant_ship_generic_name + str(i)
        ships_list.append(name)
        i += 1
    
    ships_dict = {}
        
    # Populate Fishing List
    fishing_list = []
    fishing_dict = {}
    number_of_fishing_ships = 10
    fishing_ship_generic_name = 'Fishing_'
    i = 1
    while i <= number_of_fishing_ships:
        fname = fishing_ship_generic_name + str(i)
        fishing_list.append(fname)
        i += 1
    
    submarine = Submarine(Submarine_Start, 90)
    
    # Plotting in KML 
    plotting_merchants = {}
    plotting_fishing = {}
    plotting_submarine = []
    
    for ships in ships_list:
        pause_time = 0
        '''Create Merchants'''
        ships_dict[ships] = Merchant_Ship(start_location(), wait = pause_time)
        pause_time += 120
        
    for fships in fishing_list:
        '''Create Fishing Vessels'''
        fishing_dict[fships] = Fishing_Ship(Fishing)
    
    # Begin loop by storing initialization time
    t = float(time.time())
    t_max = float(time.time()) + 60*100
    i = 0
    
    while t < t_max:
        '''Main time loop. Updates positions of all vessles, then pauses until one second has elapsed.'''
        
        # Used to hold the current second just before incrementing 
        t_now = float(time.time())

        for ships in ships_list:
            # Update position of Merchant Shipping
            ships_dict[ships].update_position(ships_dict[ships].spd)
            
            
        for fships in fishing_list:
            # Update position of Fishing Ship 
            fishing_dict[fships].update_position(fishing_dict[fships].crs)
            
        # Update position and depth of submarine
        submarine.update_position(submarine.crs)
        submarine.change_depth(700)
        submarine.change_speed(12)
        if i < 200:
            submarine.change_crs(271)
        
        if i > 200 and i < 500:
            submarine.change_crs(200)
        
        if i > 800 and i < 3000:
            submarine.change_crs(30)
            
        if i > 3000:
            submarine.change_crs(submarine.loc.bearing(Fishing))
        
        i += 1
            
        for ship in ships_list:
            # Save coordinates of merchants for KML plotting
            if ship not in plotting_merchants:
                plotting_merchants[ship] = []
            plotting_merchants[ship].append((ships_dict[ship].loc.lon,ships_dict[ship].loc.lat))
            
        for fship in fishing_list:
            # Store coordinates for kml plotting of fishing ships
            if fship not in plotting_fishing:
                plotting_fishing[fship] = []
            plotting_fishing[fship].append((fishing_dict[fship].loc.lon,fishing_dict[fship].loc.lat))
        

        # Store coordinates of submarine for KML plotting
        plotting_submarine.append((submarine.loc.lon,submarine.loc.lat))
    
        t = t + 1
######### Real time############################
        #while t_now + 1 > float(time.time()):
            #time.sleep(0.00001)
            
    plot_in_KML(ships_list,plotting_merchants,fishing_list,plotting_fishing,plotting_submarine)

        
        
        
        
        
        
    
    
    

        