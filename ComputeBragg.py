#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

import glob

file_dir = 'C:\Users\adestefa\Documents\Code\SRIM-2013\SRIM Outputs\SolarCruiserRCD'

for name in glob.glob(file_dir + '\IONIZ_Bragg*'):
    print(name)