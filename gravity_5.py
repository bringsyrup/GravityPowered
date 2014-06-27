#!/usr/bin/env python

'''
- This script calculates the mass and vertical travel distance required to 
power a given load for t minutes given specs on a rectified alternator.
- The required spec is alternator rpm for a given power load, P. 
- It also calculates the vertical velocity of the mass, for practical purposes.
- use -h or --help option for usage
'''

import math as m
import argparse

parser = argparse.ArgumentParser(description="5-gear gravity-powered alternator") 

#constants:
g = 9.8 #gravity constant, m/s^2
r = .0635 #small gear radius, m
R = .3429 #large gear radius based on 27" OD bicycle wheel, m

#positional arguments
parser.add_argument("rpm", type=float, help="required rpm for power load, rpm")
parser.add_argument("P", type=float, help="power load, W")
parser.add_argument("t", type=float, help="desired run-time, minutes")

#optional arguments
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

#converts v_gen and t_sec to m/s and seconds, respectively 
v_gen = args.rpm * 2 * m.pi * r / 60 
t_sec = args.t * 60 

#the calculation of m_weight depends on P and v_gen. ask Casey for alternator specs
v_weight = v_gen * m.pow(r/R, 4)
m_weight = args.P / (g * v_weight)
dist = v_weight * t_sec

def sigfigs(x):
    format = "%.2e"
    as_string = format % x
    return as_string

#convert answers to 3 significant figures
Dist = sigfigs(dist)
V_weight = sigfigs(v_weight)
M_weight = sigfigs(m_weight)

if args.verbose:
	print "%s m required at %s m/s using a %s kg mass" % (Dist, V_weight, M_weight)
else:
	print Dist + " m"
	print V_weight + " m/s"
	print M_weight + " kg"