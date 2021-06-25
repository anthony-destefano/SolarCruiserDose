#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob


def dose_from_depth(x, depth, Edep):
	dmin = 0. 
	dmax = depth[-1]# cm
	N = np.shape(depth)[0]

	i = int((N-1)*(x - dmin)/(dmax - dmin))
	if x > depth[i]: # not sure why we have to do this b/c of int... but we want to force the ordering
		i += 1
	#print(i, x, depth[i])

	dose = 0.
	if i > 0:
		dose = (depth[i] - x) * Edep[i] / (depth[i] - depth[i-1]) # eV
	else:
		dose = (depth[i] - x) * Edep[i] / depth[i] # eV

	dose += np.sum(Edep[i+1:])

	dose *= 1.60218E-19 / (2.321e-3) # J * cm^2 / (kg * #)

	return dose

SE_file = 'shielding_and_energy.txt'

TRIM_directory = sys.argv[1]


# get number of shielding thicknesses
Nsheilding = int(np.loadtxt(SE_file, unpack=True, max_rows=1))

print('Number of shielding thicknesses: ',Nsheilding)

NE = np.loadtxt(SE_file, skiprows=3, max_rows=1).astype(int)

print('NE for each shielding thickness: ', NE)

AL_thickness = np.loadtxt(SE_file, skiprows=5, max_rows=Nsheilding, unpack=True) # cm

print('Shielding thicknesses (cm): ', AL_thickness)

E       = np.zeros(np.sum(NE)) # keV
dose_Si = np.zeros(np.sum(NE)) 

for i in range(Nsheilding):
	#print(np.sum(NE[:i]))

	E[np.sum(NE[:i]):np.sum(NE[:i+1])] = np.loadtxt(SE_file, skiprows = 7+Nsheilding+2*i+np.sum(NE[:i]), max_rows=NE[i], unpack=True) 
	

for file in glob.glob(TRIM_directory + '\\IONIZ*.txt'):
	print('reading...', file)
	idx_d = int(file[-12:-10])
	idx_E = int(file[-9:-7])
	idx_t = int(file[-6:-4])

	idx = np.sum(NE[:idx_d]) + idx_E

	# print(idx_d, idx_E, idx_t)
	print('Al shielding thickness = ', AL_thickness[idx_d], ' cm, Ion energy = ',  E[idx], ' keV')

	depths, Eion, Erecoil = np.loadtxt(file, unpack=True, skiprows=27)
	depths *= 1.e-8 # cm
	Etot = (Eion + Erecoil) * 1.e8 # eV/cm/ion

	dose_Si[idx] = dose_from_depth(AL_thickness[idx_d], depths, Etot)

	print('Energy dep = ', np.format_float_scientific(dose_Si[idx], precision=2, trim='k', unique=False), ' eV')

for i in range(Nsheilding):
	plt.loglog(E[np.sum(NE[:i]):np.sum(NE[:i+1])], dose_Si[np.sum(NE[:i]):np.sum(NE[:i+1])], label=str(np.format_float_scientific(AL_thickness[i], precision=2, trim='k', unique=False))+' cm Al')

plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Proton Energy (keV)')
plt.ylabel('Dose per fluence (gray/(#/cm2))')
plt.legend()
plt.show()

np.savetxt('dose_vs_energy_vs_sheilding.txt', np.c_[E, dose_Si])