# 1st argument is directory of output files, preceeding with ./
# 2nd argument is number of total zones to read
# 3rd argument is which normalization to use (DSNE, ISS, or user-defined),
#  this must match the environment used, otherwise the selection is invalid

import fileinput
import glob
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fluence = 0

if sys.argv[3] == 'DSNE':
    fluence = 2.74E+10 # electrons/cm2-day, from DSNE trapped electrons
elif sys.argv[3] == 'ISS':
    fluence = 1.974E+10 # electrons/cm2-day, from ISS spec trapped electrons
elif float(sys.argv[3]) > 0.0:
    fluence = float(sys.argv[3])
else:
    print('ERROR: argument 3 must be DSNE, ISS or user-defined > 0')

nskip = 5 # space between header and rows of #s to read, should not change
skip = 0
skip_flag = 0
nrows = int(sys.argv[2]) # number of zones to keep track of
n = 0
read_flag = 0
n_files = 0 # calculated on the fly, assuming the same amount of zones

areal_density  = np.zeros((0,nrows))
energy_deposit = np.zeros((0,nrows))

directory = sys.argv[1]

for line in fileinput.input(files=glob.glob(directory + '/*.out')):
    if "ENERGY DEPOSITION" in line:
        areal_density = np.append(areal_density, np.zeros((1,nrows)), axis=0)
        energy_deposit = np.append(energy_deposit, np.zeros((1,nrows)), axis=0)
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

        areal_density[n_files,n] = a.iloc[0][5] - a.iloc[0][4] # g/cm2
        energy_deposit[n_files,n] = a.iloc[0][12] # MEV-CM2/G-SOURCE PARTICLE
        n += 1

    if skip_flag == 1 and read_flag == 1 and n >= nrows:
        skip_flag = 0
        read_flag = 0
        n = 0
        n_files += 1
        
dose = energy_deposit * 1.6021E-13 * 1.0E5 * fluence # rads/time of fluence used

####raw_energy_dep = areal_density * energy_deposit

# not including the last layer, which is assumed to be the silicon detector
####total_dose = (np.sum(raw_energy_dep[:,0:nrows-1],axis=1)
####/ np.sum(areal_density[:,0:nrows-1],axis=1)* 1.6021E-13 * 1.0E5 * fluence).reshape((nrows,1))# rads/day

# get the thicknesses from the cpp file to make plotting nicer
read_flag = 0
nskip = 1
n = 0
thicknesses = np.zeros((1,n_files))

for line in fileinput.input(files = directory + '/' + directory[2:] + '.cpp'):
    if "thicknesses[n_files]" in line:
        read_flag = 1

    if skip_flag == 0 and read_flag == 1 and skip <= nskip:
        skip += 1
    if skip_flag == 0 and read_flag == 1 and skip > nskip:
        skip_flag = 1
        skip = 0

    if skip_flag == 1 and read_flag == 1 and n < n_files:
        line = line.replace(',', '')
        thicknesses[0,n] = float(line) # cm
        n += 1





# print(total_dose)
# print(dose)
# print(np.append(dose, total_dose, axis=1))

#####dose = np.append(dose, total_dose, axis=1)
#print(dose)
#print(np.append(dose, total_dose.reshape((n_files,1)), axis=0))

# the '\r\n' new line works for windows notepad, otherwise the defualt is '\n' and the newlines don't show,
#  although they will show when copy-pasted into excel
#np.savetxt('results_' + directory[2:] + '.txt', np.asmatrix(np.append(thicknesses, dose.T, axis=0).T),newline='\r\n')
np.savetxt('results_' + directory[2:] + '.txt', dose.T,newline='\r\n')

#plt.loglog(thicknesses.T, dose)
#plt.show()

#print(dose.T)
###print(areal_density)
print(energy_deposit)
#print(dose)