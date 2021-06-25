#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

SE_file = 'shielding_and_energy.txt'

# get number of shielding thicknesses
Nsheilding = int(np.loadtxt(SE_file, unpack=True, max_rows=1))

print('Number of shielding thicknesses: ',Nsheilding)

NE = np.loadtxt(SE_file, skiprows=3, max_rows=1).astype(int)

print('NE for each shielding thickness: ', NE)

AL_thickness = np.loadtxt(SE_file, skiprows=5, max_rows=Nsheilding, unpack=True)

print('Shielding thicknesses (cm): ', AL_thickness)

E = np.zeros(np.sum(NE))

for i in range(Nsheilding):
	print(np.sum(NE[:i]))

	E[np.sum(NE[:i]):np.sum(NE[:i+1])] = np.loadtxt(SE_file, skiprows = 7+Nsheilding+2*i+np.sum(NE[:i]), max_rows=NE[i], unpack=True) 
	

print(E)