#!/usr/bin/env python

"""
takes data from data.txt and turns it into arrays to be used in gravity_opt.py
"""

import csv
import numpy as np

def get_data(input_data, find_max=None):
    with open(input_data) as input_file:
        as_lists = list(csv.reader(input_file))
    data_arrays = []
    for lst in as_lists:
        as_array = []
        for i in lst:
            as_float = float(i)
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
    P_mech_data, P_load_data, omega_data = get_data('fake_data.txt')
    P_mech_range = get_data('fake_data.txt', 'find_max')
    eff = np.divide(P_load_data, P_mech_data)
    print P_mech_range 
