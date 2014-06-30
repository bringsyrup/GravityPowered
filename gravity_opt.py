#!/usr/bin/env python

'''
this version optimizes for energy efficiency and returns optimal power load and number of gear-ups
'''

import math as m
import numpy as np
from matplotlib.pyplot import *
import argparse as ap

parser = ap.ArgumentParser(description="Gravity-powered generator optimization")
parser.add_argument("max_n", type=int, help= "max number of gear-ups in optimization, integer")
parser.add_argument("max_mass", type=int, help="max mass allowed in optimization")
parser.add_argument("time", type=float, help="minimum desired run-time")
parser.add_argument("-s", "--specs", action="store_true", help="prints characterization data for generator")
args = parser.parse_args()

#defined constants
r = .0635 #small gear radius, m
R = .3429 #large gear radius, m
dist = 1.5 #max practical distance allowed
g = 9.8 #gravitational constant, m/s^2
P_mech_range = 400 #this is currently used to generate the mechanical power range, but when data exists get rid of P_mech_range and replace P_mech_data with a data array. Similarly, all other current data arrays are stand-ins until real data is aquired. If more than one data set is available, I should figure out how to parse in arrays from a script containing the data sets.

def generate_curves(max_P):
    #generate P_load vs P_mech curve from P_mech and P_load data
    P_mech_data = np.linspace(1, P_mech_range, 11)
    P_load_data = [0., 10., 30., 60., 100., 140., 175., 190., 195., 198., 200.]
    coeffs_load = np.polyfit(P_mech_data, P_load_data, 4)
    P_load_poly = np.poly1d(coeffs_load)
    P_mechs = np.arange(0, max_P, 1)
    P_load = P_load_poly(P_mechs)
    #generate omega vs P_mech curve from omega data and P_mech_data
    omega_data = [0., 30., 60., 80., 95., 100., 105., 115., 135., 160., 200]
    coeffs_omega = np.polyfit(P_mech_data, omega_data, 4)
    omega_poly = np.poly1d(coeffs_omega)
    omega = omega_poly(P_mechs)
    #generate efficiency vs load curve from P_load_data and P_mech_data
    eff_data = P_load_data / P_mech_data
    coeffs_eff = np.polyfit(P_load_data, eff_data, 4)
    eff_poly = np.poly1d(coeffs_eff)
    P_loads = np.linspace(0, max(P_load), len(P_load))
    efficiency = eff_poly(P_loads)
    if not args.specs:
        return P_mechs, P_loads, omega_poly, coeffs_load, coeffs_eff, efficiency
    else:
        return P_mechs, P_load, omega, P_loads, efficiency 

def get_optimals(self_values, coeffs, scalar_opt):
    for value in self_values: #attempting to print P_load corresponding to eff_max
        scalar_i = 0.
        for i in range(len(coeffs)):
            scalar_i = coeffs[i] * pow(value, len(coeffs) - (1 + i))
        print scalar_i
        if scalar_i == scalar_opt:
            optimal_value = value
            return optimal_value 

def get_gears(radius, Radius, mass, power, omega, gravity):
    base = radius / Radius
    arg = power / (Radius * omega * mass * gravity)
    gears = m.log(arg, base)
    return gears

#if specs option on, show full generator characterization curves
if args.specs:
    P_mechs, P_load, omega, P_loads, eff = generate_curves(P_mech_range)
    fig = figure()
    subplot(311)
    plot(P_mechs, omega)
    xlabel("mechanical power input, W")
    ylabel("rotational velocity, rad/s")
    subplot(312)
    plot(P_mechs, P_load)
    xlabel("mechanical power input, W")
    ylabel("electrical power output, W")
    subplot(313)
    plot(P_loads, eff)
    xlabel("electrical power output, W")
    ylabel("power efficiency, %")
    suptitle("full characterization curves from data")
    show()
#else, generate data for finding optimal power load from max_mass
else:
    P_mech_max = args.max_mass * g * dist / args.time
    P_mechs, P_loads, omega_poly, coeffs_load, coeffs_eff, eff = generate_curves(P_mech_max)
    eff_opt = max(eff)
    P_load_opt = get_optimals(P_loads, coeffs_eff, eff_opt)
    P_mech_opt = get_optimals(P_mechs, coeffs_load, P_load_opt) 
    omega_opt = omega_poly(P_mech_opt)
    mass_opt = P_mech_opt * args.time / (g * dist)
    gears_opt = get_gears(r, R, mass_opt, P_mech_opt, omega_opt, g)
    print " %s Watt optimal load \n %s kg optimal mass \n %s gear-ups" % (P_load_opt, mass_opt, gears_opt)

