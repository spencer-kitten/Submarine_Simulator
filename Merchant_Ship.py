# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:56:34 2021

@author: spenc
Need to make map imported from somewhere else
"""

import random as rand  
import math, time
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd  # note that this is the accepted community naming convention to import pandas
import numpy as np
import matplotlib.pyplot as plt

from Coord import Coord

from Location_Getter import Location_Dictionary



class Merchant_Ship:
    '''Improved class to store Merchant Ship data'''

    
    def __init__(self,loc,speed=16,crs = 000, wait = 0):
        self.loc = loc
        self.initial = str()
        self.track = False
        self.wait = wait
        if self.wait > 0:
            self.spd = 0
        else:
            self.spd = 16
        
        if self.loc.dist_to(Location_Dictionary['A']) < 1:
            self.crs = self.loc.bearing(Location_Dictionary['B'])
            self.initial = 'A'
        elif self.loc.dist_to(Location_Dictionary['B']) < 1:
            self.crs = self.loc.bearing(Location_Dictionary['C'])
            self.initial = 'B'
        elif self.loc.dist_to(Location_Dictionary['C']) < 1:
            self.crs = self.loc.bearing(Location_Dictionary['B'])
            self.initial = 'C'
            

            
    def update_position(self, spd, wait = 0):
        '''Shamelessly stolen. Not accurate for large distances. Untested at poles'''
        
        pause = self.wait
        if self.wait > 0:
            self.spd = 0
            pause -= 1
            self.wait = pause
        else:
            self.spd = 16
            
        R = 6967420 #Radius of the Earth in yds
        brng = math.radians(self.crs)
        d = self.spd*(2000/3600) #Distance in yds

        lat1 = Coord.deg2rad(self.loc.lat)
        lon1 = Coord.deg2rad(self.loc.lon)

        lat2 = math.asin(math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        
        self.loc = Coord(lat2,lon2)
        
        if self.loc.dist_to(Location_Dictionary['B']) < .5:
            self.track = True
        
        if self.track == False:
            self.crs = self.loc.bearing(Location_Dictionary['B'])
            return   
        elif self.track == True and self.initial == 'A':
            self.crs = self.loc.bearing(Location_Dictionary['C'])
        elif self.track == True and self.initial == 'C':
            self.crs = self.loc.bearing(Location_Dictionary['A'])


        
    def __str__(self):
        return "(%f,%f), spd = %f, crs = %d" % (self.loc.lat,self.loc.lon,self.spd, self.crs)
    
   
      
    