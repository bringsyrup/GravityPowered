#!/usr/bin/env python

"""
takes data from data text file and turns it into numpy arrays for gravity_opt.py
"""

import csv
import numpy as np

def get_data(input_data, find_max=None):
    with open(input_data) as input_file:
        data_lists = list(csv.reader(input_file))
    data_arrays = []
    for lst in data_lists:
        as_array = []
        for i in lst:
            try:
                as_float = float(i)
            except (TypeError, ValueError):
                print "The data file contains invalid characters. Read README.txt for assistance."
                break
            as_array.append(as_float)
        data_arrays.append(as_array)
    P_mech_data = np.asarray(data_arrays[0])
    P_load_data = np.asarray(data_arrays[1])
    omega_data = np.asarray(data_arrays[2])
    if find_max == "find_max":
        return max(P_mech_data)
    else:
        return P_mech_data, P_load_data, omega_data

if __name__=='__main__':

    get_data()
    
