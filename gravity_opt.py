#!/usr/bin/env python

'''
this version optimizes for energy efficiency and returns optimal power load, mass, and number of gear-ups
'''

import math as m
import numpy as np
from matplotlib.pyplot import *
import argparse as ap
from constants import *
import data

def generate_curves(data_file, max_P):
    #load raw data from text file and convert to arrays
    P_mech_data, P_load_data, omega_data = data.get_data(data_file)
    #generate P_load vs P_mech curve from P_mech and P_load data
    coeffs_load = np.polyfit(P_mech_data, P_load_data, 4)
    P_load_poly = np.poly1d(coeffs_load)
    P_mechs = np.linspace(0, max_P, max_P)
    P_load = P_load_poly(P_mechs)
    #generate omega vs P_mech curve from omega data and P_mech_data
    coeffs_omega = np.polyfit(P_mech_data, omega_data, 4)
    omega_poly = np.poly1d(coeffs_omega)
    omega = omega_poly(P_mechs)
    #generate efficiency vs load curve from P_load_data and P_mech_data
    eff_data = np.divide(P_load_data, P_mech_data) 
    coeffs_eff = np.polyfit(P_load_data, eff_data, 4)
    eff_poly = np.poly1d(coeffs_eff)
    #P_loads = np.linspace(0, max(P_load), max(P_load))
    efficiency = eff_poly(P_load)
    if not args.specs:
        return P_mechs, P_load, omega_poly, coeffs_load, coeffs_eff, efficiency
    else:
        return P_mechs, P_load, omega, efficiency 

def get_gears(mass, power, omega):
    base = r / R
    arg = power / (R * omega * mass * g)
    gears = m.log(arg, base)
    return gears

def sigfigs(as_float):
    if type(as_float)=='numpy.ndarray':
        as_float = float(as_float)
    format = "%.2e"
    as_string = format % as_float
    return as_string

if __name__=='__main__':

    parser = ap.ArgumentParser(description="Gravity-powered gear system for running generator with given data. For more info read README.txt.")
    parser.add_argument("max_mass", type=int, help="max mass allowed in optimization")
    parser.add_argument("time", type=float, help="minimum desired run-time")
    parser.add_argument("data_file", type=str, help="file must be .txt format and contain data as specified in README.txt")
    parser.add_argument("-s", "--specs", action="store_true", help="print best-fit polynomials for generator data")
    parser.add_argument("-v", "--verbose", action="store_true", help="print answers in sci notation with 3 significant figures instead of as integers")
    args = parser.parse_args()

    #if specs option on, show full generator characterization curves
    if args.specs:
        P_mech_range = data.get_data(args.data_file, 'find_max')
        P_mechs, P_load, omega, eff = generate_curves(args.data_file, P_mech_range)
        axis = 14 #set axis fontsize
        line = 3.
        subplot(311)
        plot(P_mechs, omega, linewidth=line)
        xlabel("mechanical power input, W", fontsize=axis)
        ylabel("rotational velocity, rad/s", fontsize=axis)
        subplot(312)
        plot(P_mechs, P_load, linewidth=line)
        xlabel("mechanical power input, W", fontsize=axis)
        ylabel("electrical power output, W", fontsize=axis)
        subplot(313)
        plot(P_load, eff, linewidth=line)
        xlabel("electrical power output, W", fontsize=axis)
        ylabel("power efficiency", fontsize=axis)
        suptitle("full characterization curves from data", fontsize=20)
        show()
    #else, get optimal values for load, mass, and number of gear-ups
    else:
        P_mech_max = args.max_mass * g * dist / args.time
        P_mechs, P_load, omega_poly, coeffs_load, coeffs_eff, eff = generate_curves(args.data_file, P_mech_max)
        eff_opt = max(eff)
        P_load_opt = P_load[np.where(eff==eff_opt)]
        P_mech_opt = P_mechs[np.where(P_load==P_load_opt)]
        if P_mech_opt <= 0. or m.isnan(P_mech_opt) == True:
            print "The maximum mass input is not high enough for this generator. Try --help for more info."
        else:
            omega_opt = omega_poly(P_mech_opt)
            mass_opt = P_mech_opt * args.time / (g * dist)
            gears_opt = get_gears(mass_opt, P_mech_opt, omega_opt)
            if args.verbose:
                P_load_opt = sigfigs(P_load_opt)
                mass_opt = sigfigs(mass_opt)
                gears_opt = sigfigs(gears_opt)
                print " %s Watt load \n %s kg mass \n %s gear-ups" % (P_load_opt, mass_opt, gears_opt)
            else:
                print " %d Watt load \n %d kg mass \n %d gear-ups" % (P_load_opt, mass_opt, gears_opt)
