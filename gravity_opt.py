#!/usr/bin/env python

'''
this version optimizes for energy efficiency and returns optimal power load, mass, and number of gear-ups
'''

import math as m
import numpy as np
from matplotlib.pyplot import *
import argparse as ap
import constants as c

def generate_curves(max_P):
    #generate P_load vs P_mech curve from P_mech and P_load data
    P_mech_data = np.linspace(1, c.P_mech_range, 11)
    P_load_data = [0., 10., 30., 60., 100., 140., 175., 190., 195., 198., 200.]
    coeffs_load = np.polyfit(P_mech_data, P_load_data, 4)
    P_load_poly = np.poly1d(coeffs_load)
    P_mechs = np.linspace(0, max_P, max_P)
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
    #P_loads = np.linspace(0, max(P_load), max(P_load))
    efficiency = eff_poly(P_load)
    if not args.specs:
        return P_mechs, P_load, omega_poly, coeffs_load, coeffs_eff, efficiency
    else:
        return P_mechs, P_load, omega, efficiency 

def get_gears(mass, power, omega):
    base = c.r / c.R
    arg = power / (c.R * omega * mass * c.g)
    gears = m.log(arg, base)
    return gears

def sigfigs(as_float):
    if type(as_float)=='numpy.ndarray':
        as_float = float(as_float)
    format = "%.2e"
    as_string = format % as_float
    return as_string

if __name__=='__main__':

    parser = ap.ArgumentParser(description="Gravity-powered generator optimization")
    parser.add_argument("max_mass", type=int, help="max mass allowed in optimization")
    parser.add_argument("time", type=float, help="minimum desired run-time")
    parser.add_argument("-s", "--specs", action="store_true", help="prints characterization data for generator")
    parser.add_argument("-v", "--verbose", action="store_true", help="print answers in sci notation with 3 significant figures instead of as integers")
    args = parser.parse_args()

        #if specs option on, show full generator characterization curves
    if args.specs:
        axis = 14 #set axis fontsize
        line = 3.
        P_mechs, P_load, omega, eff = generate_curves(P_mech_range)
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
        P_mech_max = args.max_mass * c.g * c.dist / args.time
        P_mechs, P_load, omega_poly, coeffs_load, coeffs_eff, eff = generate_curves(P_mech_max)
        eff_opt = max(eff)
        P_load_opt = P_load[np.where(eff==eff_opt)]
        P_mech_opt = P_mechs[np.where(P_load==P_load_opt)]
        omega_opt = omega_poly(P_mech_opt)
        mass_opt = P_mech_opt * args.time / (c.g * c.dist)
        gears_opt = get_gears(mass_opt, P_mech_opt, omega_opt)
        if args.verbose:
            P_load_opt = sigfigs(P_load_opt)
            mass_opt = sigfigs(mass_opt)
            gears_opt = sigfigs(gears_opt)
            print " %s Watt load \n %s kg mass \n %s gear-ups" % (P_load_opt, mass_opt, gears_opt)
        else:
            print " %d Watt load \n %d kg mass \n %d gear-ups" % (P_load_opt, mass_opt, gears_opt)
