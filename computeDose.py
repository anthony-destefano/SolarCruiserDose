#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

#  python .\computeDose.py DSNE DSNE DSNE_Table_3.3.1.10.2-1 DSNE_Table_3.3.1.10.2-1.txt angleWeights.txt 1.42E-3
#  python .\computeDose.py DSNE ESP-PSYCHIC ESP-PSYCHIC_totalfluence_2-year_subL1 ESP-PSYCHIC_totalfluence_2-year_subL1.txt angleWeights.txt 1.42E-3
#  python .\computeDose.py L2CPE L2CPE L2-CPE_2-year_95-percentile p95_sunward_solarwind_IMP.txt angleWeights.txt 1.42E-3

fileDirectory            = sys.argv[1]
energy_angleDirectory    = sys.argv[2]
outputPrefix             = sys.argv[3]
energyCenterFile = './' + energy_angleDirectory + '/' + sys.argv[4]
angleCenterFile  = './' + energy_angleDirectory + '/' + sys.argv[5]
density = float(sys.argv[6]) # kg/cm^3

energy, flux, Ebin_width, Ebin_left = np.loadtxt(energyCenterFile, unpack=True)
angle , weight, angbin_width        = np.loadtxt(angleCenterFile , unpack=True)

NE     = energy.size
Ntheta = angle.size
Ndepth = 100

dose_depth  = np.zeros(Ndepth)
dose_energy = np.zeros(NE)
dose_angle  = np.zeros(Ntheta)

for i in range(0, NE):
	
	for j in range(0, Ntheta):
		
		TRIM_filename = './' + fileDirectory + "/IONIZ_" + fileDirectory + '_'
		if angle[j] < 10.:
			TRIM_filename = TRIM_filename + '0'
		# str(int(energy[i]))
		if fileDirectory == 'DSNE':
			TRIM_filename = TRIM_filename + str(int(angle[j])) + "deg_" + str(int(energy[i])) + "keV.txt"
		
		# https://numpy.org/doc/stable/reference/generated/numpy.format_float_scientific.html
		if fileDirectory == 'L2CPE':
			TRIM_filename = TRIM_filename + str(int(angle[j])) + "deg_" + str(np.format_float_scientific(energy[i], precision=2, trim='k', unique=False)) + "keV.txt" #str(np.format_float_scientific(energy[i], precision=2, exp_digits=1))
			
			TRIM_filename = str(np.char.replace(TRIM_filename, 'e-', 'E-'))
			TRIM_filename = str(np.char.replace(TRIM_filename, 'e+', 'E+'))

		#print(TRIM_filename)

		depth, E_ion, E_recoil = np.loadtxt(TRIM_filename, unpack=True, skiprows=26)

		dose = (E_ion + E_recoil) * 1.E8 * 1.60218E-19 * flux[i] * weight[j] / density # rad

		dose_depth     = dose_depth     + dose
		dose_energy[i] = dose_energy[i] + np.sum(dose)
		dose_angle[j]  = dose_energy[j] + np.sum(dose)

dose_tot = np.sum(dose_energy)

# compute integral dose vs energy
int_dose_E = np.zeros(NE)
for i in range(0, NE):
	int_dose_E[i] = np.sum(dose_energy[i:NE-1])

# compute integral dose vs depth
int_dose_depth = np.zeros(Ndepth)
for i in range(0, Ndepth):
	int_dose_depth[i] = np.sum(dose_depth[0:i])

# https://stackoverflow.com/questions/8218608/scipy-savefig-without-frames-axes-only-content
plt.loglog(Ebin_left, int_dose_E)
plt.title('Environment = '+outputPrefix+'\nIntegral Dose in Slab vs. Energy\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Energy (keV)')
plt.ylabel('Integral Dose (rad > Energy)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(outputPrefix + "_Integral_Dose_vs_Energy.png", dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.loglog(energy, dose_energy/Ebin_width)
plt.title('Environment = '+outputPrefix+'\nDifferential Dose in Slab vs. Energy\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Energy (keV)')
plt.ylabel('Dose (rad/keV)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(outputPrefix + "_Differential_Dose_vs_Energy.png", dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.loglog(depth/10000., int_dose_depth)
plt.title('Environment = '+outputPrefix+'\nIntegral Dose in Slab vs. Depth\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Depth (microns)')
plt.ylabel('Integral Dose (rad < Depth)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(outputPrefix + "_Integral_Dose_vs_Depth.png", dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.loglog(depth/10000., dose_depth/(depth[0]/10000.))
plt.title('Environment = '+outputPrefix+'\nDifferential Dose in Slab vs. Depth\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Depth (microns)')
plt.ylabel('Dose (rad/micron)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(outputPrefix + "_Differential_Dose_vs_Depth.png", dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.plot(angle, dose_angle/(angbin_width*np.pi/180. * 2*np.pi))
plt.title('Environment = '+outputPrefix+'\nDifferential Dose in Slab vs. Angle\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Incident Angle (degrees)')
plt.ylabel('Dose (rad/steradians)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(outputPrefix + "_Differential_Dose_vs_Angle.png", dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.show()


