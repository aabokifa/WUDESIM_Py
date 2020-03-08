# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:21:49 2019

@author: aaa6859
"""

import WUDESIM-Py as WUDESIM
#from WUDESIM_Py.src import WUDESIM

import matplotlib.pyplot as plt

import pandas as pd

#%%

### Example 1: Running a full simulation

# start WUDESIM
WUDESIM_proj = WUDESIM()

# Run full simulation
WUDESIM_proj.RUN_FULL_SIM("CTOWN.INP","CTOWN.RPT","WUDESIM.INP","WUDESIM.RPT")

# Retreive pipe results of EPANET and WUDESIM simulations
PIPE_RESULTS_EPANET  = WUDESIM_proj.GET_TIMESERIES_PIPE_EPANET('P121')
PIPE_RESULTS_WUDESIM = WUDESIM_proj.GET_TIMESERIES_PIPE_WUDESIM('P121')

# Retreieve node results of EPANET and WUDESIM simulations
NODE_RESULTS_EPANET  = WUDESIM_proj.GET_TIMESERIES_NODE_EPANET('J184')
NODE_RESULTS_WUDESIM = WUDESIM_proj.GET_TIMESERIES_NODE_WUDESIM('J184')

#%% 

### Example 2: Getting the properties of dead-end branches

# start WUDESIM
WUDESIM_proj = WUDESIM()

# open a new EPANET project
WUDESIM_proj.ENGINE_OPEN_EPANET_PROJ("CTOWN.INP","CTOWN.RPT")

# Find dead-end pipes
WUDESIM_proj.ENGINE_FIND_DEADENDS()

# Run EPANET simulation
WUDESIM_proj.ENGINE_RUN_EPANET_SIM()

# Calculate dead-end properties
WUDESIM_proj.ENGINE_CALC_DEADEND_PROPERTIES_EPANET()

# Get DEB properties
BRAN_PROPERTIES = WUDESIM_proj.GET_ALL_BRAN_PROPERTIES_EPANET()
PIPE_PROPERTIES = WUDESIM_proj.GET_ALL_PIPE_PROPERTIES_EPANET()
NODE_PROPERTIES = WUDESIM_proj.GET_ALL_NODE_PROPERTIES_EPANET()

#%% 

### Example 3: Visualizing the layout of dead-end branches

# start WUDESIM
WUDESIM_proj = WUDESIM()

# Run full simulation
WUDESIM_proj.RUN_FULL_SIM("CTOWN.INP","CTOWN.RPT","WUDESIM.INP","WUDESIM.RPT")

# Get pipe properties
PIPE_PROPS = WUDESIM_proj.GET_ALL_PIPE_PROPERTIES_EPANET()

# Get IDs of laminar and transitional dead-end pipes
PIPE_IDs = list(PIPE_PROPS['Pipe_ID'].loc[PIPE_PROPS['Avg_Reynolds']<4000])

# Visualize dead-end pipes
WUDESIM_proj.VISUALIZE_LAYOUT_PIPES(EPANET_INP="CTOWN.INP",pipe_ids=PIPE_IDs)


#%%