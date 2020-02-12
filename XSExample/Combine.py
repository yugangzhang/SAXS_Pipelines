#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Imports
########################################

import sys, os
#SciAnalysis_PATH='/home/kyager/current/code/SciAnalysis/main/'
#SciAnalysis_PATH='/nsls2/xf11bm/software/SciAnalysis/'
SciAnalysis_PATH='/home/group/Software/SciAnalysis/'
SciAnalysis_PATH in sys.path or sys.path.append(SciAnalysis_PATH)

import glob
from SciAnalysis import tools
from SciAnalysis.XSAnalysis.Data import *
from SciAnalysis.XSAnalysis import Protocols



### Define folder

#source_dir = '../raw/'
source_dir = '../analysis/HDF5/'
output_dir = '../analysis/HDF5/'


## Define sample and key info
fp = 'DJ_single_crystal_2_th0.15'
pattern = fp + '*' 

Key = 'sector_average'

## Get relevent files
infiles = glob.glob(os.path.join( res_dir, pattern+'.h5'))
def fp_pat( s ):
    return s[-15:-8]
infiles =  sorted(infiles, key=fp_pat) 
print(len(infiles))

## Combine data
N = len(infiles)
for k in range(N):
    hfile =infiles[k]
    h5r = h5todict( hfile )
    if k ==0:
        X = h5r[Key]['data'][:,0]
        Y = np.zeros([len(x), N ])
    Y[:,k] = h5r[Key]['data'][:,1]
    
    
## Save data to h5 file

d = { 'X': x, 'Y': Y  }
dicttoh5( d, res_dir + fp + '.h5', h5path='/', mode='a', overwrite_data=True)


















