#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

def lin_inv_int(x0, x1, y0, y1, y):
	return (x1-x0) * (y-y0) / (y1-y0) + x0

def lin_int(x0, x1, y0, y1, x):
	return (y1-y0) * (x-x0) / (x1-x0) + y0

def pow_inv_int(x0, x1, y0, y1, y):
	return x0 * (y/y0)**(np.log(x1/x0)/np.log(y1/y0))

def pow_int(x0, x1, y0, y1, x):
	return y0 * (x/x0)**(np.log(y1/y0)/np.log(x1/x0))

#file_dir = 'C:\Users\adestefa\Documents\Code\SRIM-2013\SRIM Outputs\SolarCruiserRCD'

percentile = float(sys.argv[1])/100.
density    = float(sys.argv[2]) # kg/cm^3

NE = 29

E = np.zeros(NE)#np.logspace(np.log2(1.E5/(2.**16)), np.log2(4096.E2), NE, base = 2.)
i = 0

depth_perc = np.zeros(NE)
total_dose = np.zeros(NE)

for filename in glob.glob('IONIZ_Bragg*'):
    print(filename)

    depth, E_ion, E_recoil = np.loadtxt(filename, unpack=True, skiprows=26)

    E_tot = E_ion + E_recoil
    E_sum = np.sum(E_tot)
    E_tot = E_tot / E_sum

    E_cum = np.zeros(100)


    for j in range(0, 100):
    	E_cum[j] = np.sum(E_tot[0:j])
    	if j == 0 and percentile < E_cum[j]:
    		depth_perc[i] = lin_inv_int(0., depth[0], E_cum[0], E_cum[1], percentile)
    	elif percentile >= E_cum[j-1] and percentile <= E_cum[j]:
    		depth_perc[i] = pow_inv_int(depth[j-1], depth[j], E_cum[j-1], E_cum[j], percentile)

    E[i] = 1.E5/(2.**16) * 2.**i

    total_dose[i] = np.sum(E_ion + E_recoil) * 1.E8 * 1.60218E-19  / density # rads

    #print(E[i], depth_perc[i])
    i = i+1
    # plt.loglog(depth, E_ion)
    # plt.show()

data = np.array([E, depth_perc])
data = data.T
np.savetxt('depth_percentile_vs_E_' + str(percentile) + '.txt', data, delimiter=' ')

data = np.array([E, total_dose])
data = data.T
np.savetxt('total_dose_vs_E.txt', data, delimiter=' ')
