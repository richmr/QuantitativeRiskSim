# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:44:19 2018

@author: tmthydvnprt
This function is adapted from the discussion at:
https://stackoverflow.com/questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-scipy-python

Though I've made it easy to use, I did NOT write this awesome code - mrich
"""
from ModelFit import do_fit
import numpy as np

# test
# Data taken from: https://compliancy-group.com/hipaa-fines-directory-year/

finesdata = np.array([3500000, 100000, 4348000, 475000, 2200000, 3200000, 5500000,
                      400000, 31000, 2500000, 2400000, 387200, 2300000, 239800, 
                      25000, 1550000, 3900000, 750000, 2200000, 650000, 2700000,
                      2750000, 5550000, 400000, 2140000, 650000])
        
do_fit(finesdata, "HIPAA Fines")