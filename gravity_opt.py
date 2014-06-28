#!/usr/bin/env python

'''
** use optional positional argument "n" for a gear ratio of (R/r)^n. Else n = 5.
'''
import numpy as np
from matplotlib.pyplot import * 
import argparse


parser = argparse.ArgumentParser(description="Gravity-powered alternator optimization") 
parser.add_argument("P", type=float, help="power load, W")
parser.add_argument("t", type=float, help="desired run-time, minutes")
parser.add_argument("n", type=int, nargs='?', help="integer number of gear-ups, integer")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-s", "--specs", action="store_true", help="print characterization graphs for generator")
args = parser.parse_args()

def alternator_data(): #the data in this function is a placeholder!
	P_mech_data = np.linspace(0, 100, 11)	
	omega_data = [0., 30., 60., 80., 95., 100., 105., 115., 135., 160., 200.]
	coefficients = np.polyfit(P_mech_data, omega_data, 4)
	return coefficients

def get_output(n):
	m_weight = torque_gen * pow(R, n-1) / (g * pow(r, n))
	v_weight = omega * pow(r, n) / pow(R, n-1)
	dist = v_weight * t_sec
	pack_ans = [m_weight, v_weight, dist]
	return pack_ans

def sigfigs(x):
    format = "%.2e"
    as_string = format % x
    return as_string

if args.specs:
	coefficients = alternator_data()
	omega_poly = np.poly1d(coefficients)
	P_mechs = np.arange(0, 100, 1)
	omegas = omega_poly(P_mechs)

	P_e = np.linspace(0, 100, 1000)
	eff_poly = -0.0002 * pow(P_e - 50, 2) + 0.5	

	fig = figure()
	subplot(211)
	plot(P_e, eff_poly)
	xlabel('Power load (W)')
	ylabel('Efficiency')
	subplot(212)
	plot(P_mechs, omegas)
	xlabel('Mechanical power of alternator (W)')
	ylabel('Rotational frequency of alternator')
	suptitle('Alternator characterization', fontsize=20)
	show()
else:
	g = 9.8 #gravitational constant, m/s^2
	r = .0635 #small gear radius, m
	R = .3429 #large gear radius based on 27" OD bicycle wheel, m
	t_sec = args.t * 60 #convert t to seconds

	efficiency = -0.0002 * pow(args.P - 50, 2) + 0.5 #this equation is a placeholder

	if efficiency <= 0:
		print "not a valid power load for this generator. Try option --specs for more info."
	else:
		P_mech = args.P / efficiency
		coefficients = alternator_data()
		omega = 0.
		for coefficient in range(len(coefficients)):
			omega += coefficients[coefficient] * pow(P_mech, 4 - coefficient)
		torque_gen = P_mech / omega

		if args.n:
			unpack_ans = get_output(args.n)
		else:
			unpack_ans = get_output(5)

		#convert answers to sci notation with 3 sig figs
		M_weight = sigfigs(unpack_ans[0])
		V_weight = sigfigs(unpack_ans[1])
		Dist = sigfigs(unpack_ans[2])

		if args.verbose:
			print "%s m required at %s m/s using a %s kg mass" % (Dist, V_weight, M_weight)
		else:
			print " %s m \n %s m/s \n %s kg" % (Dist, V_weight, M_weight)