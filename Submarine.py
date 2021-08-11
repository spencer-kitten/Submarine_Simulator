# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:57:49 2021

@author: spenc
"""

import random as rand  
import math, time
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd  # note that this is the accepted community naming convention to import pandas
import numpy as np
import matplotlib.pyplot as plt


from Coord import Coord

class Submarine:
    '''Improved class to store data of USS Lubbock'''
    
    def __init__(self,loc,crs = rand.randrange(0, 360),spd = 3, depth = 150):
        self.loc = loc
        self.crs = crs
        self.spd = spd
        self.depth = depth
        
    def update_position(self,crs):
        '''Shamelessly stolen. Not accurate for large distances. Untested at poles.'''
        R = 6967420 #Radius of the Earth in yds
        brng = math.radians(crs)
        d = self.spd*(2000/3600) #Distance in yds

        lat1 = Coord.deg2rad(self.loc.lat)
        lon1 = Coord.deg2rad(self.loc.lon)

        lat2 = math.asin(math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        
        self.loc = Coord(lat2,lon2)
        
    def change_depth(self,new_depth = 150):
        '''changes depth at 1ft per second'''
        
        current_depth = self.depth
        
        
        if current_depth == new_depth:
            # Staying the same depth
            return
        elif current_depth < new_depth:
            # Going deep 
            current_depth += 1
            self.depth = current_depth
            return
        else:
            # Going Shallow
            current_depth -= 1
            self.depth = current_depth
            
    def change_speed(self,new_speed = 3, cavitate = False):
        '''Changes speed at 0.5 kts per second if cavitate = False, 2kts per second if cavitate = True'''
        
        current_speed = self.spd
        
        if cavitate == False:
            rate = 0.5
        else:
            rate = 2
        
        if current_speed == new_speed:
            return
        elif current_speed < new_speed:
            current_speed += rate
            self.spd = current_speed
            return
        else:
            current_speed -= rate
            self.spd = current_speed
            return
        
    def change_crs(self,new_crs, rudder = 10):
        '''Changes course at 1 degree per second at 10degree rudder.'''
        
        current_crs = self.crs
        
        
        if current_crs == new_crs:
            self.crs = new_crs
            return
        else:
            working_crs = current_crs + 180
            if new_crs < current_crs:
                new_crs += 360
            if working_crs >= new_crs:
                current_crs += 1*rudder/10
            else:
                current_crs -= 1*rudder/10
                
        if current_crs >= 360:
            self.crs = current_crs - 360
        elif current_crs < 0:
            self.crs = current_crs + 360
        else: 
            self.crs = current_crs 
        
            
        
        
            
    def __str__(self):
        return "(%f,%f), spd = %f, crs = %d" % (self.loc.lat,self.loc.lon,self.spd, self.crs)

 

