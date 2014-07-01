"""
constants for gravity_opt.py
"""

r = .0635 #small gear radius, meters, but can be any units because the gear ratio is a fraction
R = .3429 #large gear radius, meters, based on 27" OD bike wheel
dist = 1.5 #max pracitcal distance allowed for vertical dropt of weight
g = 9.8 #gravitational constant, m/s^2
P_mech_range = 400 
'''
P_mech_range is currently used to generate the full mechanical power range for the fake data. /
When real data exists get rid of this and replace P_mech_data (in gravity_opt.py) with data /
array. Similarly, all other current data arrays in gravity_opt.py are fake stand-ins.
'''
