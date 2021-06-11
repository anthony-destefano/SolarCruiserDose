#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

N = 100

def D_slab(R, d, E):
	dmin = 0.
	dmax = d[N-1]

	iR = int((R - dmin) / (dmax - dmin) * (N-1))

	if iR < 0 or iR > N-1 or ():
		return 0.0

	# bi = np.log10(E[iR+1]/E[iR]) / np.log10(d[iR+1]/d[iR])

	# return E[iR] * (R/d[iR])**bi
	#print(iR)
	return E[iR]


def int_D_slab(a, b, d, E):
	dmin = 0.
	dmax = d[N-1]

	ia = int((a - dmin) / (dmax - dmin) * (N-1))
	ib = int((b - dmin) / (dmax - dmin) * (N-1))

	if ia < 0 or ia > N-1 or ib < 0 or ib > N-1:
		return 0.0

	if ia == ib:
		return E[ia] * (b - a)

	return E[ia] * (d[ia] - a) + E[ib] * (b - d[ib-1]) + np.sum(E[ia+1:ib-1]) * (ib-ia-2) * d[0]


def D_sphere(r, R, d, E):
	#print(D_slab(R-r, d, E) -D_slab(R+r, d, E), int_D_slab(R-r, R+r, d, E))
	return R/r * (D_slab(R-r, d, E) - D_slab(R+r, d, E)) + int_D_slab(R-r, R+r, d, E)/r

ICRU_sphere_radius = float(sys.argv[1]) # cm
ICRU_depth         = float(sys.argv[2]) # cm

for filepath in glob.iglob('IONIZ_ICRU*.txt'):
	Ei = float(filepath[14:17])

	depth, ions, recoils = np.loadtxt(filepath, skiprows=29, unpack=True)

	E_dep = (ions + recoils) * 1.e8 # eV/cm

	depth /= 1.e8 # ang to cm


	dose = D_sphere(ICRU_depth, ICRU_sphere_radius, depth, E_dep) * 1.60218e-19 * 1.e3 # Sv * cm^2
	print(Ei, dose)