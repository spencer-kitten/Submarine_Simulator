# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:57:18 2021

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


class Fishing_Ship:
    '''Improved class to store Merchant Ship data'''
    
    def __init__(self,loc,speed=3):
        self.spd = speed 
        self.loc = Coord(loc.lat + rand.random()/125,loc.lon + rand.random()/125)
        self.crs = rand.randint(0,359)
            
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
        
        # Ensure course never exceeds 359, just resets to 000
        if crs >= 359:
            crs = -1
        self.crs = crs + 1
  
    def __str__(self):
        return "(%f,%f), spd = %f, crs = %d" % (self.loc.lat,self.loc.lon,self.spd, self.crs)
    