#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Imports
########################################

import sys, os
#SciAnalysis_PATH='/home/kyager/current/code/SciAnalysis/main/'
SciAnalysis_PATH='/nsls2/xf11bm/software/SciAnalysis/'
#SciAnalysis_PATH='/home/group/Software/SciAnalysis/'
SciAnalysis_PATH in sys.path or sys.path.append(SciAnalysis_PATH)

import glob
from SciAnalysis import tools
from SciAnalysis.XSAnalysis.Data import *
from SciAnalysis.XSAnalysis import Protocols



# Define some custom analysis routines
########################################
# TBD



# Experimental parameters
########################################

if False:
    # PhotonicSciences CCD
    from SciAnalysis.XSAnalysis.DataRQconv import *
    calibration = CalibrationRQconv(wavelength_A=0.9184) # 13.5 keV
    calibration.set_image_size(1042) # psccd Photonic Sciences CCD
    calibration.set_pixel_size(pixel_size_um=101.7)
    calibration.set_distance(0.232) # Bigger number moves theory rings outwards (larger spacing)
    calibration.set_beam_position(22.0, 1042-22.0)
    calibration.set_angles(det_orient=45, det_tilt=-21, det_phi=0, incident_angle=0., sample_normal=0.)
    print('ratio Dw = {:.3f}'.format(calibration.get_ratioDw()))

    mask_dir = SciAnalysis_PATH + '/SciAnalysis/XSAnalysis/masks/'
    mask = Mask(mask_dir+'CCD/psccd_generic-mask.png')
    
elif False:
    # Custom Dectris Pilatus 800k (lower-left modules removed)
    calibration = Calibration(wavelength_A=0.9184) # 13.5 keV
    calibration.set_image_size(981, height=1043) # Pilatus1M
    calibration.set_pixel_size(pixel_size_um=172.0)
    #calibration.set_beam_position(201, 1043-313)
    calibration.set_beam_position(409, 1043-419)

    #calibration.set_distance(0.355)
    calibration.set_distance(0.257)

    mask_dir = SciAnalysis_PATH + '/SciAnalysis/XSAnalysis/masks/'
    mask = Mask(mask_dir+'Dectris/Pilatus800_custom-mask.png')
    #mask.load('./Pilatus800k_current-mask.png')

else:
    calibration = Calibration(wavelength_A=0.9184)
    calibration.set_image_size(487, height=619) # Pilatus300k
    calibration.set_pixel_size(pixel_size_um=172.0)

    #cms.SAXS.setCalibration([402, 443], 5.0, [25.00, 16.00]) # 2017-04-01, 13.5 keV, 5m, GISAXS
    calibration.set_beam_position(467.0, 619-27.0)
    calibration.set_distance(.265)
    mask_dir = SciAnalysis_PATH + '/SciAnalysis/XSAnalysis/masks/'
    mask = Mask(mask_dir+'Dectris/Pilatus300k_main_gaps-mask.png')


# Files to analyze
########################################
source_dir = '../raw/'
output_dir = './'

pattern = 'DJ_single_crystal_2*' #'*2538339*'
#pattern = 'BA_N3_1W*' #2/11/
#pattern = '*27145*'
#pattern = 'DJ_test2_th0.500*'
#pattern = '*2556952*'
#pattern = '*2714556*'

print(source_dir)

infiles = glob.glob(os.path.join(source_dir, pattern+'.tiff'))
infiles.sort()


# Analysis to perform
########################################

load_args = { 'calibration' : calibration, 
             'mask' : mask,
             #'rot180' : False,
             #'flip' : True, # PSCCD
             }
run_args = { 'verbosity' : 3,   
            }

process = Protocols.ProcessorXS(load_args=load_args, run_args=run_args)

# Examples:
#protocols = [ Protocols.circular_average_q2I(plot_range=[0, 0.2, 0, None]) ]
#protocols = [ Protocols.linecut_angle(q0=0.01687, dq=0.00455*1.5, show_region=False) ]
#protocols = [ Protocols.q_image(blur=1.0, bins_relative=0.5, plot_range=[-0.1, 3.0, 0, 3.0], _xticks=[0, 1.0, 2.0, 3.0], ztrim=[0.2, 0.01]) ]
#protocols = [ Protocols.qr_image(blur=1.0, bins_relative=0.5, plot_range=[-0.1, 3.0, 0, 3.0], _xticks=[0, 1.0, 2.0, 3.0], zmin=1010., ztrim=[None, 0.01]) ]
#protocols = [ Protocols.qr_image(blur=None, bins_relative=0.8, plot_range=[-0.1, 3.0, 0, 3.0], _xticks=[0, 1.0, 2.0, 3.0], ztrim=[0.38, 0.002], dezing_fill=True) ]
#protocols = [ Protocols.q_phi_image(bins_relative=0.25, plot_range=[0, 3.0, 0, +90]) ]

protocols = [

    #Protocols.calibration_check(show=False, AgBH=True, q0=1.369*0.25, dq=0.002, num_rings=10, ztrim=[0.2, 0.01], dpi=300) ,
    Protocols.circular_average(ylog=True, dq = .001, plot_range=[0.0, 1.5, None, None],  gridlines=True,  save_results = [ 'hdf5' ]  ) ,
    #Protocols.thumbnails(crop=None, resize=0.5, cmap=cmap_vge, ztrim=[0.06, 0.001], zmin=1000.0) , # PSCCD
    #Protocols.linecut_q(chi0= 90+0, dq=.5, ylog=True, gridlines=True, plot_range=[0.0, 1.5, None, None] ) ,
    Protocols.sector_average(angle=-0, dangle=20,dq = .001, show_region=False, ylog=True, gridlines=True, plot_range=[0.0, 1.5, None, None],  save_results = [ 'hdf5' ] ) ,
    #Protocols.linecut_q(chi0= 90+70, dq= .5, ylog=True, gridlines=True, plot_range=[0.0, 1.5, None, None]  , show_region= True,  save_results = [ 'hdf5' ]  ) ,
    #Protocols.qr_image(blur=None, colorbar=True, ) ,
    #Protocols.thumbnails(crop=None, resize=1.0, blur=None, cmap=cmap_vge, ztrim=[0.01, 0.001]) ,
    Protocols.HDF5(  save_results = [ 'hdf5' ] ), 
    #Protocols.metadata_extract()
    ]
    



# Run
########################################
print('Processing {} infiles...'.format(len(infiles)))
process.run(infiles, protocols, output_dir=output_dir, force = 1)


# Loop
########################################
# This is typically only used at the beamline (it loops forever, watching for new files).
#process.monitor_loop(source_dir=source_dir, pattern='*.tiff', protocols=protocols, output_dir=output_dir, force=False)
