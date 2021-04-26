#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

#  python .\computeDose.py DSNE_SPE DSNE_Table_3.3.1.10.2-1.txt angleWeights.txt 1.42E-3

fileDirectory    = sys.argv[1]
energyCenterFile = './' + fileDirectory + '/' + sys.argv[2]
angleCenterFile  = './' + fileDirectory + '/' + sys.argv[3]
density = float(sys.argv[4]) # kg/cm^3

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
		
		TRIM_filename = './' + fileDirectory + "/IONIZ_DSNE_"
		if angle[j] < 10.:
			TRIM_filename = TRIM_filename + '0'

		TRIM_filename = TRIM_filename + str(int(angle[j])) + "deg_" + str(int(energy[i])) + "keV.txt"

		#print(TRIM_filename)

		depth, E_ion, E_recoil = np.loadtxt(TRIM_filename, unpack=True, skiprows=26)

		dose = (E_ion + E_recoil) * 1.E8 * 1.60218E-19 * flux[i] * weight[j] / density

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

plt.loglog(Ebin_left, int_dose_E)
plt.title('Integral Dose vs. Energy\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Energy (keV)')
plt.ylabel('Integral Dose (rad > Energy)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(fileDirectory + "_Integral_Dose_vs_Energy.png", dpi=800)

plt.figure()
plt.loglog(energy, dose_energy/Ebin_width)
plt.title('Differential Dose vs. Energy\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Energy (keV)')
plt.ylabel('Dose (rad/keV)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(fileDirectory + "_Differential_Dose_vs_Energy.png", dpi=800)

plt.figure()
plt.loglog(depth/10000., int_dose_depth)
plt.title('Integral Dose vs. Depth\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Depth (microns)')
plt.ylabel('Integral Dose (rad < Depth)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(fileDirectory + "_Integral_Dose_vs_Depth.png", dpi=800)

plt.figure()
plt.loglog(depth/10000., dose_depth/(depth[0]/10000.))
plt.title('Differential Dose vs. Depth\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Depth (microns)')
plt.ylabel('Dose (rad/micron)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(fileDirectory + "_Differential_Dose_vs_Depth.png", dpi=800)

plt.figure()
plt.plot(angle, dose_angle/(angbin_width*np.pi/180. * 2*np.pi))
plt.title('Differential Dose vs. Angle\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Incident Angle (degrees)')
plt.ylabel('Dose (rad/steradians)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig(fileDirectory + "_Differential_Dose_vs_Angle.png", dpi=800)

plt.show()


