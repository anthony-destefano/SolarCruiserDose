#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob


fileDirectory    = sys.argv[1]
energyCenterFile = './' + fileDirectory + '/' + sys.argv[2]
angleCenterFile  = './' + fileDirectory + '/' + sys.argv[3]
density = float(sys.argv[4]) # kg/cm^3

energy, flux, Ebin_width     = np.loadtxt(energyCenterFile, unpack=True)
angle , weight, angbin_width = np.loadtxt(angleCenterFile , unpack=True)

NE    = energy.size
Ntheta = angle.size

dose_depth  = np.zeros(100)
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


plt.loglog(energy, dose_energy/Ebin_width)
plt.title('Dose vs. Energy\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Energy (keV)')
plt.ylabel('Dose (rad/keV)')

plt.figure()
plt.loglog(depth/10000., dose_depth/(depth[0]/10000.))
plt.title('Dose vs. Depth\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Depth (microns)')
plt.ylabel('Dose (rad/micron)')

plt.figure()
plt.plot(angle, dose_angle/(angbin_width*np.pi/180. * 2*np.pi))
plt.title('Dose vs. Angle\nTotal Dose = ' + str(np.round(dose_tot/1000.)) + ' krads')
plt.xlabel('Incident Angle (degrees)')
plt.ylabel('Dose (rad/steradians)')

plt.show()


