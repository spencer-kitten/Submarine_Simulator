# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:25:25 2021

@author: spenc
"""

from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
from Location_Getter import *

def plot_in_KML(ships_list,plotting_merchants,fishing_list,plotting_fishing,plotting_submarine):
    kml2 = kml.KML()  # create the kml object
    # if we are going to have multiple placemarks in a kml doc,
    # we need to put them in a "folder" within the kml structure...
    # Create a KML Folder and add it to the Document
    ns = '{http://www.opengis.net/kml/2.2}'
    kml_id = "some_id"
    kml_name = "random point 2"
    kml_description = "Another random point"
    folder = kml.Folder(ns, 'fid', 'f name', 'f description')
    kml2.append(folder)
    # create a new kml Placemark object
    pnt = kml.Placemark(name="Fishing Spot", description="Where the fish are")
    # add its geometry, a (shapely) Point
    pnt.geometry = Point(Fishing.lon,Fishing.lat)  # lon, lat optional height
    # append the Placemark to the folder
    folder.append(pnt)
      # A Linestring is a connected set of line segments.
      
    merchant_plot_linestrings = {}
    for ship in ships_list:
        lin = kml.Placemark(name="Merchant Track", description=" ")
        coords = plotting_merchants[ship]
        lin.geometry = LineString(coords)
        folder.append(lin) 
     
    fishing_plot_linestrings = {}
    for fship in fishing_list:
        lin = kml.Placemark(name="Fishing Track", description=" ")
        coords = plotting_fishing[fship]
        lin.geometry = LineString(coords)
        folder.append(lin) 
        
    lin = kml.Placemark(name="Submairne Track", description=" ")
    coords = plotting_submarine
    lin.geometry = LineString(coords)
    folder.append(lin) 

    with open('Waterspace.kml','w') as f: 
        f.write(kml2.to_string(prettyprint=True))
        