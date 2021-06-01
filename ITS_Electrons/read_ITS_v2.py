import fileinput
import glob
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# python .\read_ITS_v2.py .\RCD-MPI\FLX_ELE_95_SWMX_IMP_Kapton_150um_run05.out 50 1.163178618e17 1.42 '11-month Solar Wind Electron Dose in 150 um of Kapton'

ITS_filename = sys.argv[1]
nrows        = int(sys.argv[2]) # number of zones to keep track of
fluence      = float(sys.argv[3]) # #/cm^2 / timeframe
density      = float(sys.argv[4]) # g/cm^3
plotSubTitle = sys.argv[5]   

nskip = 5 # space between header and rows of #s to read, should not change
skip = 0
skip_flag = 0
n = 0
read_flag = 0
n_files = 0 # calculated on the fly, assuming the same amount of zones

areal_density  = np.zeros(nrows)
depth          = np.zeros(nrows)
energy_deposit = np.zeros(nrows)

for line in fileinput.input(files=glob.glob(ITS_filename)):
    if "ENERGY DEPOSITION" in line:
        #areal_density = np.append(areal_density, np.zeros((1,nrows)), axis=0)
        #energy_deposit = np.append(energy_deposit, np.zeros((1,nrows)), axis=0)
        read_flag = 1

    if skip_flag == 0 and read_flag == 1 and skip <= nskip:
        skip += 1
    if skip_flag == 0 and read_flag == 1 and skip > nskip:
        skip_flag = 1
        skip = 0

    if skip_flag == 1 and read_flag == 1 and n < nrows:
        line = line.replace(' - ', ' ')
        df = pd.DataFrame({'raw': [line]})
        a = df['raw'].str.split(expand=True).astype(float)

        areal_density[n]  = a.iloc[0][5] - a.iloc[0][4] # g/cm2
        depth[n]          = a.iloc[0][5] / density # cm           
        energy_deposit[n] = a.iloc[0][12] # MEV-CM2/G-SOURCE PARTICLE
        n += 1

    if skip_flag == 1 and read_flag == 1 and n >= nrows:
        skip_flag = 0
        read_flag = 0
        n = 0
        #n_files += 1
        
dose = energy_deposit * 1.6021E-13 * fluence # rads/time of fluence used

print(depth)
ITS_filename = ITS_filename.replace('.', '')
ITS_filename = ITS_filename.replace('\\', '-')
np.savetxt('doseResults_' + ITS_filename + '.txt', np.c_[depth, dose])

tot_dose = np.sum(dose)
cum_dose = np.cumsum(dose)
depth *= 1.E4 # cm to um

plt.loglog(depth, dose * areal_density / density)
plt.xlabel('Depth (microns)')
plt.ylabel('Differential Dose (rads/micron)')
plt.title('Differential Dose vs. Depth\n' + plotSubTitle + '\nTotal dose = ' + str(np.round(tot_dose)) + ' rads')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig('DifferentialDose_' + ITS_filename + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.loglog(depth, cum_dose)
plt.xlabel('Depth (microns)')
plt.ylabel('Integral Dose (rads < depth)')
plt.title('Integral Dose vs. Depth\n' + plotSubTitle + '\nTotal dose = ' + str(np.round(tot_dose)) + ' rads')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.savefig('IntegralDose_' + ITS_filename + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.show()