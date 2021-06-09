#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import glob

# python .\convert_L2CPE_to_ITS_input.py FLX_ELE SWMX_IMP 95 50 50 150 run01 6.379724E-04 1.0E-03 500000 32000

#  mpiexec -n 4 .\itstigp2_mpi.exe ..\L2CPE_Electrons\FLX_ELE_95_SWMX_IMP_Kapton_150um_run01.inp FLX_ELE_95_SWMX_IMP_Kapton_150um_run02.out

particle_type        = sys.argv[1] # FLX_ELE
solar_cycle_data_set = sys.argv[2] # SWMX_IMP
percentile           = sys.argv[3] # 50, 95, 5, User_Def, Maximum, Minimum, Mean
NE                   = int(sys.argv[4]) # number of energy bins

ITS_material_bins     = int(sys.argv[5])
ITS_materal_thickness = float(sys.argv[6]) # in microns
ITS_filename_id       = sys.argv[7]
ITS_input_filename    = particle_type + '_' + percentile + '_' + solar_cycle_data_set + '_Kapton_' + str(int(ITS_materal_thickness)) + 'um_' + ITS_filename_id +  '.inp' 
ITS_electron_cutoff   = float(sys.argv[8]) # MeV
ITS_photon_cutoff     = float(sys.argv[9]) # MeV
ITS_hist_per_batch    = int(sys.argv[10])
ITS_batches           = int(sys.argv[11])

percentile_column = 0
if percentile == '50':
	percentile_column = 2
elif percentile == '95':
	percentile_column = 3
elif percentile == '5':
	percentile_column = 4
elif percentile == 'User_Def':
	percentile_column = 5
elif percentile == 'Maximum':
	percentile_column = 6
elif percentile == 'Minimum':
	percentile_column = 7
elif percentile == 'Mean':
	percentile_column = 8

bin_flux_avg = np.zeros(NE)
N_files = 0

for file in list(glob.glob(particle_type + '*' + solar_cycle_data_set + '.DAT')):
	N_files += 1
	print(N_files, file)

	E1, E2, bin_flux = np.loadtxt(file, skiprows = 36+NE, max_rows = NE, usecols = (0,1,percentile_column), unpack=True)

	bin_flux_avg += bin_flux

	#print(E1, E2, bin_flux)


print("Total files read: ", N_files)

bin_flux_avg /= float(N_files)

# compute CDF ( < E2)
flux_CDF = np.cumsum(bin_flux_avg)

flux_norm = flux_CDF[NE-1]
flux_CDF /= flux_norm # normalize to 1
#print(flux_CDF)

# plt.loglog(E2, flux_CDF)
# # plt.figure()
# # plt.loglog((E1+E2)/2., bin_flux_avg)
# plt.show()

# Find when CDF equals 1
# NE_lt_1 = 0
# while flux_CDF[NE_lt_1] != 1.:
# 	NE_lt_1 += 1

# Print out ITS input file
print("Generating ITS inp file: " + ITS_input_filename)

with open(ITS_input_filename, 'w') as ITS_f:
	print('ECHO 1', file=ITS_f)
	print('TITLE', file=ITS_f)
	print('Kapton ' + str(ITS_materal_thickness) + ' microns with L2-CPE V1.3 electron environment', file=ITS_f)
	print('GEOMETRY 1\n', file=ITS_f)

	print('4 ' + str(ITS_material_bins) + ' ' + str(ITS_materal_thickness/10000.) + ' * Kapton as RCD (cm)', file=ITS_f)
	print('SPECTRUM ' + str(NE+1), file=ITS_f)
	print('* CDF converted from ' + particle_type + '_' + percentile + '_' + solar_cycle_data_set, file=ITS_f)
	print('* Normalization constant = ' + str(np.format_float_scientific(flux_norm, precision=10)) + ' #/cm^2/sec', file=ITS_f)

	#np.set_printoptions(precision = 10)
	for i in range(0, NE):
		print(np.format_float_scientific(flux_CDF[NE - 1 - i], precision=10), file=ITS_f)
	print(np.format_float_scientific(0.0e0, precision=10), file=ITS_f)

	# the CDF needs to go from 1 to 0, so we need to include the 0-point
	print('* energy (MeV)', file=ITS_f)

	np.set_printoptions(precision = 10)
	for i in range(0, NE):
		print(np.format_float_scientific(E2[NE - 1 - i]/1000., precision=10), file=ITS_f) # units of MeV, not keV

	print(np.format_float_scientific(E1[0]/1000., precision=10), file=ITS_f) # units of MeV, not keV

	print('\nDIRECTION', file=ITS_f)
	print(' COSINE-LAW 0 90', file=ITS_f)
	print('CUTOFFS ' + str(ITS_electron_cutoff) + ' ' + str(ITS_photon_cutoff) + ' * electron and photon cut-offs (MeV)\n', file=ITS_f)

	print('* run size options', file=ITS_f)
	print('HISTORIES-PER-BATCH ' + str(ITS_hist_per_batch), file=ITS_f)
	print('BATCHES ' + str(ITS_batches), file=ITS_f)