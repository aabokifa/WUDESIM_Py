# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:21:49 2019

@author: aaa6859
"""

# import WUDESIM
from WUDESIM_Py.src import WUDESIM
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wntr
from cal_metrics import compare_metrics
import random
###############################################################################
#%%
# define names of Input/Output files
network = 'ky6_shape'
EPANET_INP  = network +".inp"
EPANET_RPT  = network +".RPT"
WUDESIM_INP = "WUDESIM.INP"
WUDESIM_RPT = network+"_WUDESIM.RPT"
threshold = 0.2
###############################################################################
#%% 
# open WUDESIM
WUDESIM_proj = WUDESIM()
### Run full EPANET+WUDESIM simulation 
WUDESIM_proj.RUN_FULL_SIM(EPANET_INP,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT)
###############################################################################
#%%
### GET IDs of dead-ends 

# Get IDs of all dead-end branches
ALL_BRANCH_IDs = list()
ALL_BRANCH_IDs =  WUDESIM_proj.GET_ALL_BRANCH_IDs()

# Get IDs of all dead-end junctions
ALL_NODE_IDs =  list()
ALL_NODE_IDs =  WUDESIM_proj.GET_ALL_NODE_IDs()  

# GET IDs of the inner junctions
wn = wntr.network.WaterNetworkModel(EPANET_INP)
node_list = wn.junction_name_list
INNER_NODE_IDs = [node for node in node_list if node not in ALL_NODE_IDs]
# Get IDs of all dead-end pipes
ALL_PIPE_IDs = list()
ALL_PIPE_IDs =  WUDESIM_proj.GET_ALL_PIPE_IDs()  
###############################################################################
#%%

# Get average properties of dead-end from EPANET simulation

# dead-end pipes
PIPE_PROPERTIES_EPANET = pd.DataFrame
PIPE_PROPERTIES_EPANET = WUDESIM_proj.GET_ALL_PIPE_PROPERTIES_EPANET()

# dead-end junctions
NODE_PROPERTIES_EPANET = pd.DataFrame
NODE_PROPERTIES_EPANET = WUDESIM_proj.GET_ALL_NODE_PROPERTIES_EPANET()


#%%
# EPANET results
NODE_RESULTS_EPANET = pd.DataFrame()
NODE_RESULTS_EPANET = WUDESIM_proj.GET_RESULTS_NODE_EPANET(ALL_NODE_IDs[0])

# WUDESIM results
NODE_RESULTS_WUDESIM = pd.DataFrame()
NODE_RESULTS_WUDESIM = WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(ALL_NODE_IDs[0])

# Plot comparison between EPANET and WUDESIM
fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
plt.plot(NODE_RESULTS_EPANET['TIME_STEP'],NODE_RESULTS_EPANET['QUALITY'])    
plt.plot(NODE_RESULTS_WUDESIM['TIME_STEP'],NODE_RESULTS_WUDESIM ['QUALITY'])
#plt.legend(['EPANET_QUAL','WUDESIM_QUAL'])    
plt.xlim([0,336])



###############################################################################
#%% 

### Identify pipes operating under laminar flow

# Get IDs of the pipes that have an average Reynolds <=2300
Laminar_Pipes = PIPE_PROPERTIES_EPANET.loc[PIPE_PROPERTIES_EPANET['Avg_Reynolds']<=2300]
Laminar_Pipes_IDs = list(Laminar_Pipes['Pipe_ID'].values)
print ("Number of dead end nodes", len(ALL_NODE_IDs))
print ("Number of Laminar pipes in nominal conditions", len(Laminar_Pipes_IDs))

# Plot their locations
fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
WUDESIM_proj.VISUALIZE_PIPES(EPANET_INP=EPANET_INP,pipe_ids=Laminar_Pipes_IDs,labels=False,ax=ax)
#%% plot metrics
concentration = pd.DataFrame(index = node_list,columns=['EPANET','WUDESIM'])
NODE_RESULTS_EPANET = WUDESIM_proj.GET_RESULTS_NODE_EPANET(ALL_NODE_IDs[0])
NODE_RESULTS_WUDESIM = WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(ALL_NODE_IDs[0])
ALL_NODE_IDs = [node  for node in ALL_NODE_IDs 
                 if WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['DEMAND(m3/s)'][0] !=0]
epanet = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_EPANET['TIME_STEP'])))
wudesim = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_WUDESIM['TIME_STEP'])))
for n,node in enumerate(ALL_NODE_IDs):
    quality_epa =  WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['QUALITY'].tolist()
    quality_wudesim =  WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(node)['QUALITY'].tolist()
    epanet[n] = quality_epa
    wudesim[n] = quality_wudesim
    concentration.loc[node]['WUDESIM'] = np.average(quality_wudesim[200:336])
    concentration.loc[node]['EPANET'] = np.average(quality_epa[200:336])
inner = np.zeros((len(INNER_NODE_IDs), len(NODE_RESULTS_EPANET['TIME_STEP'])))
#for n, node in enumerate(INNER_NODE_IDs):
#    inner[n] = WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['QUALITY'].tolist()
#    concentration.loc[node] = 0
compare_metrics(epanet, wudesim,  threshold, network+'_nominal')

#%%
from matplotlib import cm
fig, ax = plt.subplots(1,2,figsize=(8, 4),dpi=150)
plt.tight_layout()
wntr.graphics.network.plot_network(wn,
                                   node_attribute=concentration['EPANET'],
                                   node_size = 50,
                                   node_range=[0, 1], add_colorbar=False,
                                   node_cmap=cm.RdYlGn, ax=ax[0])
ax[0].set_title('(a)')
wntr.graphics.network.plot_network(wn,
                                   node_attribute=concentration['WUDESIM'],
                                   node_size =50,
                                   node_range=[0, 1], add_colorbar=False,
                                   node_cmap=cm.RdYlGn, ax=ax[1])
ax[1].set_title('(b)')
plt.tight_layout()
fig.savefig('./results/'+network+'_network_nominal.pdf',bbox_inches='tight')
#%%
    
epanet_avg = np.average(epanet,axis=0)
wudesim_avg = np.average(wudesim,axis=0)
epanet_std = np.std(epanet,axis=0)
wudesim_std = np.std(wudesim,axis=0)
#epanet_min= np.amin(epanet[~np.all(epanet == 0, axis=1)],axis=0)
#wudesim_min = np.amin(wudesim[~np.all(wudesim == 0, axis=1)],axis=0)
epanet_min= np.amin(epanet,axis=0)
wudesim_min = np.amin(wudesim,axis=0)
epanet_max = np.amax(epanet,axis=0)
wudesim_max = np.amax(wudesim,axis=0)

fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
plt.plot(NODE_RESULTS_EPANET['TIME_STEP'], epanet_avg,'k', lw =2)    

plt.fill_between(
            NODE_RESULTS_EPANET['TIME_STEP'], epanet_avg - epanet_std,
            epanet_avg + epanet_std,
            color="k", alpha=0.3
        )
plt.plot(NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_avg, 'b', lw =2)
plt.fill_between(
            NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_avg - wudesim_std,
            wudesim_avg + wudesim_std,
            color="b", alpha=0.3
        )  
plt.hlines(0.2, 30, 300, 'r', lw=3)
#plt.legend(['EPANET','WUDESIM'], loc='best')    
plt.xlim([100,336])
plt.ylim([0,4])
plt.xlabel('Time [h]',size = 14)
plt.ylabel('Chlorine Consentration [mg/L]',size = 14)
#%%

###############################################################################
###############################################################################


#%% Modify pattern pattern

reduced_ratio = 0.5
percent = 100
wn = wntr.network.WaterNetworkModel(EPANET_INP)
node_list = wn.junction_name_list
k = int(percent/100.*len(node_list))

# list of random sampled nodes 
random_sample = random.sample(node_list, k)

for node in random_sample:
    junction = wn.get_node(node)
    junction.demand_timeseries_list[0].base_value *=0.5
    
#es = et.EPANetSimulation(EPANET_INP )
#for pattern in es.network.patterns:
#    for time in  range(pattern, es.ENgetpatternlen(pattern)[1]+1):
#        value = es.ENgetpatternvalue(pattern, time)[1]*reduced_ratio
#        es.ENsetpatternvalue(pattern,time,value)
        
# Permanently change values = write to new file
REDUCED = 'REDUCED.INP'
wn.write_inpfile(REDUCED)
###############################################################################
#%% 
# open WUDESIM
WUDESIM_proj = WUDESIM()
### Run full EPANET+WUDESIM simulation 
WUDESIM_proj.RUN_FULL_SIM(REDUCED,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT)
###############################################################################
#%%

### GET IDs of dead-ends 

# Get IDs of all dead-end branches
ALL_BRANCH_IDs = list()
ALL_BRANCH_IDs =  WUDESIM_proj.GET_ALL_BRANCH_IDs()

# Get IDs of all dead-end junctions
ALL_NODE_IDs =  list()
ALL_NODE_IDs =  WUDESIM_proj.GET_ALL_NODE_IDs()  

# Get IDs of all dead-end pipes
ALL_PIPE_IDs = list()
ALL_PIPE_IDs =  WUDESIM_proj.GET_ALL_PIPE_IDs()  
###############################################################################
#%%

# Get average properties of dead-end from EPANET simulation

# dead-end pipes
PIPE_PROPERTIES_EPANET = pd.DataFrame
PIPE_PROPERTIES_EPANET = WUDESIM_proj.GET_ALL_PIPE_PROPERTIES_EPANET()

# dead-end junctions
NODE_PROPERTIES_EPANET = pd.DataFrame
NODE_PROPERTIES_EPANET = WUDESIM_proj.GET_ALL_NODE_PROPERTIES_EPANET()

###############################################################################
#%% 

### Identify pipes operating under laminar flow

# Get IDs of the pipes that have an average Reynolds <=2300
Laminar_Pipes = PIPE_PROPERTIES_EPANET.loc[PIPE_PROPERTIES_EPANET['Avg_Reynolds']<=2300]
Laminar_Pipes_IDs = list(Laminar_Pipes['Pipe_ID'].values)
print ("Number of Laminar pipes in reduced conditions", len(Laminar_Pipes_IDs))
# Plot their locations
fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
WUDESIM_proj.VISUALIZE_PIPES(EPANET_INP=EPANET_INP,pipe_ids=Laminar_Pipes_IDs,labels=False,ax=ax)

##############################################################################

#%% plot metriccs
NODE_RESULTS_EPANET_REDUCED = WUDESIM_proj.GET_RESULTS_NODE_EPANET(ALL_NODE_IDs[0])
NODE_RESULTS_WUDESIM_REDUCED = WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(ALL_NODE_IDs[0])
ALL_NODE_IDs = [node  for node in ALL_NODE_IDs
                 if WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['DEMAND(m3/s)'][0] !=0]
epanet_reduced = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_EPANET['TIME_STEP'])))
wudesim_reduced = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_WUDESIM['TIME_STEP'])))

for n,node in enumerate(ALL_NODE_IDs):
    quality_epa =  WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['QUALITY'].tolist()
    quality_wudesim =  WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(node)['QUALITY'].tolist()
    epanet_reduced[n] = quality_epa
    wudesim_reduced[n] = quality_wudesim

compare_metrics(epanet_reduced, wudesim_reduced, threshold, network+'_reduced')
#%%   
epanet_reduced_avg = np.average(epanet_reduced,axis=0)
wudesim_reduced_avg = np.average(wudesim_reduced,axis=0)

epanet_reduced_std = np.std(epanet_reduced,axis=0)
wudesim_reduced_std = np.std(wudesim_reduced,axis=0)

epanet_reduced_min= np.amin(epanet_reduced,axis=0)
wudesim_reduced_min = np.amin(wudesim_reduced,axis=0)


epanet_reduced_max = np.amax(epanet_reduced,axis=0)
wudesim_reduced_max = np.amax(wudesim_reduced,axis=0)

# Plot comparison between EPANET and WUDESIM AVERAGE 
fig, axs = plt.subplots(1,3,figsize=(9, 3),dpi=150)
axs[1].plot(NODE_RESULTS_EPANET['TIME_STEP'], epanet_avg, 'k--', lw =2)    
axs[1].plot(NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_avg,'r--', lw =2)
axs[1].plot(NODE_RESULTS_EPANET['TIME_STEP'], epanet_reduced_avg,'k', lw =2)    
axs[1].plot(NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_reduced_avg, 'r', lw =2)
#plt.legend(['EPANET nominal demand','WUDESIM nominal demand',
#            'EPANET reduced demand','WUDESIM reduced demand'], loc='best')    
axs[1].set_xlim([100,336])
axs[1].set_ylim([0,1.3])
axs[1].set_xlabel('Time [h]')
axs[1].set_ylabel('Chlorine Consentration [mg/L]')
axs[1].set_title('(b)')
#fig.savefig('./results/'+network+'_avg.pdf',bbox_inches='tight')
 
# Plot comparison between EPANET and WUDESIM ON ONE NODE
axs[0].plot(NODE_RESULTS_EPANET['TIME_STEP'], NODE_RESULTS_EPANET['QUALITY'], 'k--', lw =2)    
axs[0].plot(NODE_RESULTS_WUDESIM['TIME_STEP'], NODE_RESULTS_WUDESIM['QUALITY'],'r--', lw =2)
axs[0].plot(NODE_RESULTS_EPANET['TIME_STEP'], NODE_RESULTS_EPANET_REDUCED['QUALITY'],'k', lw =2)    
axs[0].plot(NODE_RESULTS_WUDESIM['TIME_STEP'], NODE_RESULTS_WUDESIM_REDUCED['QUALITY'], 'r', lw =2)
#plt.legend(['EPANET nominal demand','WUDESIM nominal demand',
#            'EPANET reduced demand','WUDESIM reduced demand'], loc='best')    
axs[0].set_xlim([100,336])
axs[0].set_ylim([0,1.3])
axs[0].set_xlabel('Time [h]')
axs[0].set_ylabel('Chlorine Consentration [mg/L]')
axs[0].set_title('(a)')
#axs[0].savefig('./results/'+network+'_avg.pdf',bbox_inches='tight')
#plot reduced percentage
per_epanet = (epanet_avg - epanet_reduced_avg)/(epanet_avg+0.0001)*100
per_wudesim = (wudesim_avg - wudesim_reduced_avg)/(wudesim_avg+0.0001)*100
    
#fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
axs[2].plot(NODE_RESULTS_EPANET['TIME_STEP'][1:], per_epanet[1:],'k', lw =2)    
axs[2].plot(NODE_RESULTS_WUDESIM['TIME_STEP'][1:], per_wudesim[1:] , 'r', lw =2)
#plt.legend(['EPANET','WUDESIM'], loc='best')    
axs[2].set_xlim([100,336])
axs[2].set_xlabel('Time [h]')
axs[2].set_ylabel('Chlorine Consentration Reduction [%]')
axs[2].set_title('(c)')
plt.tight_layout()
fig.savefig('./results/'+network+'_sum.pdf',bbox_inches='tight')

#%% plot shaded

# Plot comparison between EPANET and WUDESIM
fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
plt.plot(NODE_RESULTS_EPANET['TIME_STEP'], epanet_reduced_avg,'k', lw =2)    

plt.fill_between(
            NODE_RESULTS_EPANET['TIME_STEP'], epanet_reduced_avg - epanet_reduced_std,
            epanet_reduced_avg + epanet_reduced_std,
            color="k", alpha=0.3
        )
plt.plot(NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_reduced_avg, 'b', lw =2)
plt.fill_between(
            NODE_RESULTS_WUDESIM['TIME_STEP'], wudesim_reduced_avg - wudesim_reduced_std,
            wudesim_reduced_avg + wudesim_reduced_std,
            color="b", alpha=0.3
        )  
plt.hlines(0.2, 50, 300, 'r', lw=3)
#plt.legend(['EPANET','WUDESIM',], loc='best')    
plt.xlim([100,336])
plt.ylim([0,4])
plt.xlabel('Time [h]',size = 14)
plt.ylabel('Chlorine Consentration [mg/L]',size = 14)

#%%
#%% plot shaded difference
#
## Plot comparison between EPANET and WUDESIM
#fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
#plt.plot(NODE_RESULTS_EPANET['TIME_STEP'][50:], epanet_per_avg[50:],'k', lw =2)    
#plt.fill_between(
#            NODE_RESULTS_EPANET['TIME_STEP'][50:], epanet_per_min[50:],
#            epanet_per_max[50:],
#            color="k", alpha=0.3
#        )
#
##plt.plot(NODE_RESULTS_WUDESIM['TIME_STEP'][50:], wudesim_per_avg[50:], 'b', lw =2)
##plt.fill_between(
##            NODE_RESULTS_WUDESIM['TIME_STEP'][50:], wudesim_per_min[50:],
##            wudesim_per_max[50:],
##            color="b", alpha=0.3
##        )  
#plt.legend(['EPANET','WUDESIM',], loc='best')    
##plt.ylim([0,4])
#plt.xlabel('Time [h]',size = 14)
#plt.ylabel('Chlorine Consentration Reduction [%]',size = 14)
#%%
###############################################################################
#%% number of laminar pipes
#num = []
#reduced_ratios = np.arange(1,11)*0.1
#for reduced_ratio in reduced_ratios :
#    es = et.EPANetSimulation(EPANET_INP )
#    for pattern in es.network.patterns:
#        for time in  range(pattern, es.ENgetpatternlen(pattern)[1]+1):
#            value = es.ENgetpatternvalue(pattern, time)[1]*reduced_ratio
#            es.ENsetpatternvalue(pattern,time,value)
#            
#    # Permanently change values = write to new file
#    REDUCED = 'REDUCED.INP'
#    es.ENsaveinpfile(REDUCED)
#    WUDESIM_proj = WUDESIM()
#    ### Run full EPANET+WUDESIM simulation 
#    WUDESIM_proj.RUN_FULL_SIM(REDUCED,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT)
#    
#    # dead-end pipes
#    PIPE_PROPERTIES_EPANET = pd.DataFrame
#    PIPE_PROPERTIES_EPANET = WUDESIM_proj.GET_ALL_PIPE_PROPERTIES_EPANET()
#    Laminar_Pipes = PIPE_PROPERTIES_EPANET.loc[PIPE_PROPERTIES_EPANET['Avg_Reynolds']<=2300]
#    Laminar_Pipes_IDs = list(Laminar_Pipes['Pipe_ID'].values)
#    num.append(len(Laminar_Pipes_IDs ))
#%%
#fig, ax = plt.subplots(figsize=(6, 6),dpi=150)
#plt.plot(reduced_ratios, num,'k-*', lw =2)       
#plt.xlabel('Reduction ratio',size = 14)
#plt.ylabel('Number of laminar pipes',size = 14)


#%%
#npzfile = np.load('ky8_metrics.npz')
#vuls = npzfile['vuls']
#rels = npzfile['rels']
#ress = npzfile['ress']
#network = 'ky8'
#percents = np.linspace(0,1,21)
#percents *= 100.
#fig, axs = plt.subplots(1,3,figsize=(9, 3),dpi=150)
#plt.tight_layout()
#axs[0].plot(percents, np.average(vuls, axis=1),'r', lw =2)    
#
#axs[0].fill_between(
#            percents, np.amin(vuls, axis=1),
#            np.amax(vuls, axis=1),
#            color="k", alpha=0.3
#        )
##    axs[0].set_xlabel('Percent of conservation nodes')
#axs[0].set_ylabel('Vulnerability')
#axs[0].set_title('(a)')
#
#axs[1].plot(percents, np.average(rels, axis=1),'r', lw =2)    
#
#axs[1].fill_between(
#            percents, np.amin(rels, axis=1),
#            np.amax(rels, axis=1),
#            color="k", alpha=0.3
#        )
##    axs[1].set_xlabel('Percent of conservation nodes')
#axs[1].set_ylabel('Reliability')
#axs[1].set_title('(b)')
#
#axs[2].plot(percents, np.average(ress, axis=1),'r', lw =2)    
#
#axs[2].fill_between(
#            percents, np.amin(ress, axis=1),
#            np.amax(ress, axis=1),
#            color="k", alpha=0.3
#        )
##    axs[2].set_xlabel('Percent of conservation nodes')
#axs[2].set_ylabel('Resilience')
#axs[2].set_title('(c)')
#fig.text(0.5, -0.04, 'Percent of conservation nodes', ha='center')
#plt.show()
#fig.savefig('./results/'+network+'_random.pdf',bbox_inches='tight')
#    

compare_metrics(wudesim,  wudesim_reduced, threshold, network+'_wudesim_nr')