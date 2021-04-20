#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

#file_dir = 'C:\Users\adestefa\Documents\Code\SRIM-2013\SRIM Outputs\SolarCruiserRCD'

E = np.logspace(2., np.log10(4096.E2), 13)
i = 0

peaks = np.zeros(13)

for filename in glob.glob('IONIZ_Bragg*'):
    print(filename)

    depth, E_ion, E_recoil = np.loadtxt(filename, unpack=True, skiprows=26)

    peak_idx = np.argmax(E_ion+E_recoil)

    peaks[i] = depth[peak_idx]
    i = i+1
    # plt.loglog(depth, E_ion)
    # plt.show()

data = np.array([E, peaks])
data = data.T

np.savetxt('peak_vs_E.txt', data, delimiter=' ')