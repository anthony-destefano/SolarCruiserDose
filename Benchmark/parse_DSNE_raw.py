#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

# python parse_DSNE_raw.py DSNE_Table3.3.1.1-1_ISS_DailyTrappedProtonFluences_Raw.txt DSNE_Table3.3.1.1-1_ISS_DailyTrappedProtonFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.1-2_ISS_DailyTrappedElectronFluences_Raw.txt DSNE_Table3.3.1.1-2_ISS_DailyTrappedElectronFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.1-4_ISS_DailyTrappedBeltsTIDInsideShielding_Raw.txt DSNE_Table3.3.1.1-4_ISS_DailyTrappedBeltsTIDInsideShielding.txt 5

# python parse_DSNE_raw.py DSNE_Table3.3.1.2.1-1_LEO185x1806_DailyTrappedProtonFluences_Raw.txt DSNE_Table3.3.1.2.1-1_LEO185x1806_DailyTrappedProtonFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.2.1-2_LEO185x1806_DailyTrappedElectronFluences_Raw.txt DSNE_Table3.3.1.2.1-2_LEO185x1806_DailyTrappedElectronFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.2.1-3_LEO185x1806_DailyTrappedBeltsTIDInsideShielding_Raw.txt DSNE_Table3.3.1.2.1-3_LEO185x1806_DailyTrappedBeltsTIDInsideShielding.txt 5

# python parse_DSNE_raw.py DSNE_Table3.3.1.2.2-1_RadBeltTransit_TrappedProtonFluences_Raw.txt DSNE_Table3.3.1.2.2-1_RadBeltTransit_TrappedProtonFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.2.2-2_RadBeltTransit_TrappedElectronFluences_Raw.txt DSNE_Table3.3.1.2.2-2_RadBeltTransit_TrappedElectronFluences.txt 3
# python parse_DSNE_raw.py DSNE_Table3.3.1.2.2-3_RadBeltTransit_TrappedBeltsTIDInsideShielding_Raw.txt DSNE_Table3.3.1.2.2-3_RadBeltTransit_TrappedBeltsTIDInsideShielding.txt 5


filename_in  = sys.argv[1]
filename_out = sys.argv[2]
row_length   = int(sys.argv[3])

data = np.loadtxt(filename_in, unpack=True)

N = int(np.shape(data)[0])
data = data.reshape((int(N/row_length), row_length))

np.savetxt(filename_out, data)
