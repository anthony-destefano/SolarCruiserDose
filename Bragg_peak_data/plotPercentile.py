#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

#  python .\plotPercentile.py .\total_dose_vs_E.txt .\depth_percentile_vs_E_0.05.txt .\depth_percentile_vs_E_0.1.txt .\depth_percentile_vs_E_0.5.txt .\depth_percentile_vs_E_0.9.txt .\depth_percentile_vs_E_0.95.txt

N = len(sys.argv) - 2

fig, ax1 = plt.subplots()
fig.set_size_inches(8, 7)
ax2 = ax1.twinx()
ax1.minorticks_on() # https://stackoverflow.com/questions/19940518/cannot-get-minor-grid-lines-to-appear-in-matplotlib-figure
ax1.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
ax2.minorticks_on() # https://stackoverflow.com/questions/19940518/cannot-get-minor-grid-lines-to-appear-in-matplotlib-figure
ax2.grid(b=True, which='both', linestyle='--') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python


filename = sys.argv[1]
E, total_dose = np.loadtxt(filename, unpack=True)
ax2.loglog(E, total_dose, 'k-.', label=filename)
ax2.set_ylabel(r'Dose per fluence (rads / (#/cm$^2$))')

for i in range(0, N):
	filename = sys.argv[i+2]

	E, depth = np.loadtxt(filename, unpack=True)

	ax1.loglog(E, depth/10000., label=filename)

ax1.set_xlabel('Energy (eV)')
ax1.set_ylabel('Depth in Kapton (micron)')
ax1.set_title('Dose Percentile < Depth vs. Energy')
ax1.legend()
ax2.legend()
plt.savefig("dose_depth_percentile_vs_energy.png", dpi=1000)
plt.show()