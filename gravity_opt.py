#!/usr/bin/env python

'''
this version optimizes for energy efficiency and returns optimal power load and number of gear-ups, "n"
'''

import numpy as np
from matplotlib.pyplot import *
import argparse as ap
#from sympy import *
#import spicy as sp

parser = ap.ArgumentParser(description="Gravity-powered generator optimization")
parser.add_argument("max_n", type=int, help= "max number of gear-ups in optimization, integer")
parser.add_argument("max_mass", type=int, help="max mass allowed in optimization")
parser.add_argument("time", type=float, help="minimum desired run-time")
parser.add_argument("-s", "--specs", action="store_true", help="prints charachterization data for generator")
args = parser.parse_args()

dist = 1.5 #max distance allowed. might change to iterable later?
g = 9.8 #gravitational constant, m/s^2
min_mass = 0
P_mech_range = 400 #this is the mechanical power range used to get power load data

#generate characterization curves in range(0, max_P)
def generate_curves(max_P):
    #generate polymonial from P_mech vs P_load data
    P_mech_data = np.linspace(1, P_mech_range, 11)
    P_load_data = [0., 10., 30., 60., 100., 140., 175., 190., 195., 198., 200.]
    coefficients = np.polyfit(P_mech_data, P_load_data, 4)
    P_load_poly = np.poly1d(coefficients)
    P_mechs = np.arange(0, max_P, 1)
    P_load = P_load_poly(P_mechs)
    #generate efficiency curve 
    eff_data = P_load_data / P_mech_data
    coeffs = np.polyfit(P_load_data, eff_data, 4)
    eff_poly = np.poly1d(coeffs)
    P_loads = np.arange(0, int(max(P_load)))
    efficiency = eff_poly(P_loads)
    return P_mechs, P_load, P_loads, efficiency, coeffs 

#if specs option on, show full generator characterization curves
if args.specs:
    P_mechs, P_load, P_loads, eff, coeffs = generate_curves(P_mech_range)
    fig = figure()
    subplot(211)
    plot(P_mechs, P_load)
    subplot(212)
    plot(P_loads, eff)
    show()
#else, generate data for finding optimal power load from max_mass
else:
    P_mech_max = args.max_mass * g * dist / args.time
    P_mechs, P_load, P_loads, eff, coeffs = generate_curves(P_mech_max)
    eff_max = max(eff)
    print eff_max
    for P in P_loads:
        for i in range(len(coeffs)):
            eff_i = coeffs[i] * pow(P, len(coeffs - 1) - i)
            #print eff_i
            if eff_i == eff_max:
                print P
            
'''
Efficiency = []
for item in P_mech_array:
    for coefficient in range(len(coefficients)):
        P_load += coefficients[coefficient] * pow(item, len(coefficients) - coefficient)
'''      
