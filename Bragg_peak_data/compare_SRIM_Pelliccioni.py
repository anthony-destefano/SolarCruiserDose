#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

TRIM_dose_vs_E_filename            = sys.argv[1]
Pelliccioni2000_dose_vs_E_filename = sys.argv[2]

E_TRIM, dose_TRIM = np.loadtxt(TRIM_dose_vs_E_filename, unpack=True) 
E_P2000, dose_P2000 = np.loadtxt(Pelliccioni2000_dose_vs_E_filename, unpack=True)


plt.loglog(E_TRIM, dose_TRIM/100., marker='.', label='TRIM', markersize=15)
plt.loglog(E_P2000, dose_P2000, marker='^', label='Pelliccioni 2000 Table A2.7')
plt.xlabel('Energy (eV)')
plt.ylabel(r'Dose per Fluence (Sv / (#/cm$^2$))')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.legend()
plt.savefig("comparison_dose_vs_energy.png", dpi=1000)
plt.show()