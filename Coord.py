# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:52:51 2021

@author: spenc
"""

import random as rand  
import math, time
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd  # note that this is the accepted community naming convention to import pandas
import numpy as np
import matplotlib.pyplot as plt

class Coord:
    '''An improved class to represent lat/lon values.'''
    
    def __init__(self,lat,lon):
        self.lat = float(lat)  # make sure it's a float
        self.lon = float(lon)
        
    # Follows the specification described in the Aviation Formulary v1.46
    # by Ed Williams (originally at http://williams.best.vwh.net/avform.htm)
    def dist_to(self, other):
        lat1 = Coord.deg2rad(self.lat)
        lon1 = Coord.deg2rad(self.lon)
        lat2 = Coord.deg2rad(other.lat)
        lon2 = Coord.deg2rad(other.lon)
        
        # there are two implementations of this function.
        # implementation #1:
        #dist_rad = math.acos(math.sin(lat1) * math.sin(lat2) 
        #                   + math.cos(lat1) * math.cos(lat2) * math.cos(lon1-lon2))

        # implementation #2: (less subject to numerical error for short distances)
        dist_rad=2*math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 +
                   math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))

        return Coord.rad2nm(dist_rad)
    

    def __str__(self):
        return "(%f,%f)" % (self.lat,self.lon)
    
    def __repr__(self):
        return "Coord(%f,%f)" % (self.lat,self.lon)        

    def deg2rad(degrees):
        '''Converts degrees (in decimal) to radians.'''
        return (math.pi/180)*degrees

    def rad2nm(radians):
        '''Converts a distance in radians to a distance in nautical miles.'''
        return ((180*60)/math.pi)*radians
    
    def bearing(self,other):
        '''Calculates relative bearing to other object'''
        
        lat1 = Coord.deg2rad(self.lat)
        lon1 = Coord.deg2rad(self.lon)
        lat2 = Coord.deg2rad(other.lat)
        lon2 = Coord.deg2rad(other.lon)
        x = lon2 - lon1
        y = lat2 - lat1
        if x == 0 and y == 0:
            return 0
        if x >= 0 and y >= 0:
            return int(round(math.degrees(math.atan(x/y))))
        if x >= 0 and y < 0:
            return int(180 + round(math.degrees(math.atan(x/y))))
        if x < 0 and y >= 0:
            return int(360 + round(math.degrees(math.atan(x/y))))
        if x < 0 and y < 0:
            return int(180 + round(math.degrees(math.atan(x/y))))
        
                
    def bearing_to_rads(self, crs):
        '''Converts nautical bearing to unit circle radians'''
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
