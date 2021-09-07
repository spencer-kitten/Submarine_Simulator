# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:17:42 2021

@author: spenc
"""
from Coord import Coord
from fastkml import kml

#kml_file = 'OA3801_Final.kml'
kml_file = 'default_map.kml'

with open(kml_file, 'rt', encoding="utf-8") as myfile:
    doc=myfile.read().encode('utf-8')
    
k = kml.KML()
k.from_string(doc)   
features = list(k.features())
f2 = list(features[0].features())
f3 = list(f2[0].features())

name_list = []
working_loc = []
loc_list = []
for item in f3:
    name_list.append(str(item.name))
    
    working_loc = []
    working_loc = str(item.geometry)
    working_loc = Coord(working_loc[28:-3], working_loc[9:27])
    loc_list.append(working_loc)
    
Location_Dictionary = {}
i = 0
while i < len(name_list):
    Location_Dictionary[name_list[i]] = loc_list[i]
    i += 1

# A = Coord(36.98379636973097,-122.4677868257454)
# B = Coord(36.75057618013649,-122.2015130187223)
# C = Coord(36.52989338191978,-122.1330797721352)
# Fishing = Coord(36.69405290523898,-122.0685036944752)
# Submarine_Start = Coord(36.70256301006251,-122.3822533150178)
# Warship_Start = []
    