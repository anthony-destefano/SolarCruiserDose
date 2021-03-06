#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import glob

def double_power_law(x, a, b, c, d):
	return np.log10((10.**x / a)**b + (10.**x / c)**d)

def ret_double_power_law(x, a, b, c, d):
	return (x / a)**b + (x / c)**d

#N = len(sys.argv) - 2

# python .\fitDosePercentile.py .\percentiles.txt

percentile_list_filename = sys.argv[1]

percentiles = np.loadtxt(percentile_list_filename, unpack=True)

N = percentiles.size

fit_vals = np.array([[]])

for i in range(0, N):
	filename = 'depth_percentile_vs_E_' + str(percentiles[i]) + '.txt'
	print(filename)

	E, depth = np.loadtxt(filename, unpack=True)

	popt, pcov = curve_fit(double_power_law, np.log10(E), np.log10(depth), bounds=(0, [1E6, 1., 1E6, 2.]))

	fit_vals = np.append(fit_vals, [popt])

	plt.loglog(E, depth, label=filename)
	plt.loglog(E, ret_double_power_law(E, popt[0], popt[1], popt[2], popt[3]), label=str(popt) + '  fit to ' + filename)
	#print(popt)

plt.legend()
plt.show()

#print(fit_vals.reshape((N, 4)))
fit_vals = fit_vals.reshape((N, 4))
np.savetxt('percentile_fit_params.txt', fit_vals, delimiter=' ')
