#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import glob

#  python .\generate_ITS_input_monoBeam.py 1.E-6 1E3 37 50 150 run01 6.379724E-04 1.0E-03 5000 320 4 COSINE-LAW

# E in MeV, depth in um
def get_depth_from_energy(E): 
	return 2.* 2.088E-1 / ( (E/2.04E-3)**-1.686 + (E*1.E6)**-0.782 )

Emin = float(sys.argv[1]) # MeV
Emax = float(sys.argv[2]) # MeV
NE   = int(sys.argv[3])
ITS_material_bins     = int(sys.argv[4])
ITS_materal_thickness = float(sys.argv[5]) # in microns OVERWITTEN
ITS_filename_id       = sys.argv[6]
ITS_electron_cutoff   = float(sys.argv[7]) # MeV
ITS_photon_cutoff     = float(sys.argv[8]) # MeV
ITS_hist_per_batch    = int(sys.argv[9])
ITS_batches           = int(sys.argv[10])

ITS_run_Nproc = int(sys.argv[11])
ITS_Direction = sys.argv[12] # COSINE-LAW, BEAM




E = np.logspace(np.log10(Emin), np.log10(Emax), NE)

batch_filename = ITS_filename_id + '.bat'
open(batch_filename, 'w').close()

for Ei in E:
	Elabel = str(np.format_float_scientific(Ei, precision=3))
	ITS_input_filename  = ITS_filename_id +  '_' + Elabel + "_MeV_monobeam_Kapton.inp"
	ITS_output_filename = ITS_filename_id +  '_results_' + Elabel + "_MeV_monobeam_Kapton.out"

	if Ei > 1.: # force higher cutoff, histories are too long otherwise
		ITS_electron_cutoff = 0.01 # MeV
		ITS_photon_cutoff   = 0.01 # MeV
	if Ei > 32.:
		ITS_electron_cutoff = 0.1 # MeV
		ITS_photon_cutoff   = 0.1 # MeV
	if Ei > 320.:
		ITS_electron_cutoff = 1. # MeV
		ITS_photon_cutoff   = 1. # MeV

	ITS_materal_thickness = get_depth_from_energy(Ei)

	with open(ITS_input_filename, 'w') as ITS_f:
		print(ITS_input_filename)

		print('ECHO 1', file=ITS_f)
		print('TITLE', file=ITS_f)
		print('Kapton ' + str(ITS_materal_thickness) + ' microns with ' + Elabel + ' MeV mono-energetic electron environment', file=ITS_f)
		print('GEOMETRY 1\n', file=ITS_f)

		print('4 ' + str(ITS_material_bins) + ' ' + str(ITS_materal_thickness/10000.) + ' * Kapton as RCD (cm)', file=ITS_f)

		print('************************* SOURCE ********************************', file=ITS_f)
		print('* energy (MeV)', file=ITS_f)
		print('ELECTRONS', file=ITS_f)
		print('ENERGY ' + str(Ei), file=ITS_f)

		if ITS_Direction == 'COSINE-LAW':
			print('\nDIRECTION', file=ITS_f)
			print(' COSINE-LAW 0 90', file=ITS_f)
		if ITS_Direction == 'BEAM':
			print('\nDIRECTION 0.0', file=ITS_f)
		print('CUTOFFS ' + str(ITS_electron_cutoff) + ' ' + str(ITS_photon_cutoff) + ' * electron and photon cut-offs (MeV)\n', file=ITS_f)

		print('* run size options', file=ITS_f)
		print('HISTORIES-PER-BATCH ' + str(ITS_hist_per_batch), file=ITS_f)
		print('BATCHES ' + str(ITS_batches), file=ITS_f)

	with open(batch_filename, 'a') as bat_f:
		print('mpiexec -n ' + str(ITS_run_Nproc) + ' .\\itstigp2_mpi.exe ' + ITS_input_filename + ' ' + ITS_output_filename, file=bat_f)
		print('python ..\\read_ITS_v2.py ' + ITS_output_filename + ' ' + str(ITS_material_bins) + ' 1.0 1.42 ' + ITS_output_filename + ' SAVE_TOT_DOSE ' + str(Ei) , file=bat_f)