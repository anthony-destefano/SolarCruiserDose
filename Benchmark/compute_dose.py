#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

import glob

thickness_filename = sys.argv[1]
energy_filename    = sys.argv[2]
angle_filename     = sys.argv[3]
TRIM_directory     = sys.argv[4]
density_SI         = float(sys.argv[5]) # kg/cm^3

SPENVIS_flux_filename = sys.argv[6]
SPENVIS_flux_header   = int(sys.argv[7])
SPENVIS_flux_rows     = int(sys.argv[8])

thickness     = np.loadtxt(thickness_filename, unpack=True)/10. # cm of aluminum, last row is silicon
energy        = np.loadtxt(energy_filename, unpack=True)        # MeV
angle, weight = np.loadtxt(angle_filename, unpack=True)		    # degrees

# energy must match what's read from energy_filename
energy_SPENVIS, Iflux, Dflux = np.loadtxt(SPENVIS_flux_filename, unpack=True, skiprows=SPENVIS_flux_header, max_rows=SPENVIS_flux_rows, delimiter=',')

dose_matrix = np.zeros((np.shape(thickness)[0], np.shape(energy)[0], np.shape(angle)[0]))

for file in glob.glob(TRIM_directory + '\\IONIZ*.txt'):
	idx_d = int(file[-12:-10])
	idx_E = int(file[-9:-7])
	idx_t = int(file[-6:-4])

	E_beam = np.sqrt(energy[idx_E] * energy[idx_E+1])

	depth, ions, recoil = np.loadtxt(file, unpack=True, skiprows=27)

	depth *= 1.E-8 # ang to cm
	dose_SI = (ions[-1] + recoil[-1]) * 1.E8 * 1.60218E-19 / density_SI * (Iflux[idx_E] - Iflux[idx_E+1]) * 2592000. # rads?

	dose_matrix[idx_d, idx_E, idx_t] += dose_SI

# for i in range(np.shape(thickness)[0]):
# 	plt.loglog(energy, dose_matrix[i,:,0], label=str(thickness[i]) + ' cm')

# plt.legend()
# plt.show()

dose_shielding = np.zeros(np.shape(thickness)[0])
for i in range(np.shape(thickness)[0]):
	dose_shielding[i] = np.sum(dose_matrix[i,:,:])

plt.loglog(thickness, dose_shielding)
plt.show()
	