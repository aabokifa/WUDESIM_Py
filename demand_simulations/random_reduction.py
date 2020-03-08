# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:50:40 2020

@author: lx2347
"""
import numpy as np
import random
from WUDESIM_Py.src import WUDESIM
from cal_metrics import cal_metrics
import matplotlib.pyplot as plt 
import wntr

def RandomReduction(network, reduced_ratio, n_level, num_trail):
    
    EPANET_INP  = network +".inp"
    EPANET_RPT  = network +".RPT"
    WUDESIM_INP = "WUDESIM.INP"
    WUDESIM_RPT = network+"WUDESIM.RPT"

#    es = et.EPANetSimulation(EPANET_INP)
#    node_list = list(es.network.nodes)
#    DEMAND = et.Node.value_type['EN_BASEDEMAND']
    
    wn = wntr.network.WaterNetworkModel(EPANET_INP)
    node_list = wn.junction_name_list
    percents = np.linspace(0,1,n_level)
    threshold = 0.2
    
    rels = np.zeros((n_level, num_trail))
    vuls = np.zeros((n_level, num_trail))
    ress = np.zeros((n_level, num_trail))
    for pp, percent in enumerate(percents):  
        print ("================================ percent = %.4f" %percent )
        # if no reduction, run WUDESIM directly
        if percent == 0:
                # open WUDESIM
                WUDESIM_proj = WUDESIM()
                ### Run full EPANET+WUDESIM simulation 
                WUDESIM_proj.RUN_FULL_SIM(EPANET_INP,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT)
                
                # Get IDs of all dead-end junctions
                ALL_NODE_IDs =  list()
                ALL_NODE_IDs =  WUDESIM_proj.GET_ALL_NODE_IDs()  
                
                # Get results
                NODE_RESULTS_WUDESIM = WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(ALL_NODE_IDs[0])
                ALL_NODE_IDs = [node  for node in ALL_NODE_IDs 
                                 if WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['DEMAND(m3/s)'][0] !=0]
                wudesim = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_WUDESIM['TIME_STEP'])))
                for n,node in enumerate(ALL_NODE_IDs):
                    quality_wudesim =  WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(node)['QUALITY'].tolist()
                    wudesim[n] = quality_wudesim
                    
                # get metrics
                _, rel, vul, res = cal_metrics(wudesim, threshold)
                
                
                vuls[pp,:] =  np.average(vul)
                rels[pp,:] =  np.average(rel)
                ress[pp,:] =  np.average(res)
         
        else:
        # randomly sample set of nodes 30x...
            for s in range(0, num_trail):
                wn = wntr.network.WaterNetworkModel(EPANET_INP)
                print ("%i th trail out of %i" %(s, num_trail))
                # number of nodes to have reduced demands
                k = int(percent*len(node_list))
                
                # list of random sampled nodes 
                random_sample = random.sample(node_list, k)
                
                for node in random_sample:
                    junction = wn.get_node(node)
                    junction.demand_timeseries_list[0].base_value *=0.5
#                    d  = es.network.nodes[node].results[DEMAND][0]
#                    d *=  reduced_ratio
#                    ret2 = es.ENsetnodevalue(node, DEMAND, d)
#                    if ret2:
#                        print (ret2)
                    
                # Permanently change values = write to new file
                REDUCED = 'random_reduced.INP'
                wn.write_inpfile(REDUCED)
#                es.ENsaveinpfile(REDUCED) 
#                et.EPANetSimulation.clean(es)
                
                # open WUDESIM
                WUDESIM_proj = WUDESIM()
                ### Run full EPANET+WUDESIM simulation 
                WUDESIM_proj.RUN_FULL_SIM(REDUCED,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT)
                
                # Get IDs of all dead-end junctions
                ALL_NODE_IDs =  list()
                ALL_NODE_IDs =  WUDESIM_proj.GET_ALL_NODE_IDs()  
                
                
                NODE_RESULTS_WUDESIM = WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(ALL_NODE_IDs[0])
                ALL_NODE_IDs = [node  for node in ALL_NODE_IDs 
                                 if WUDESIM_proj.GET_RESULTS_NODE_EPANET(node)['DEMAND(m3/s)'][0] !=0]
                wudesim = np.zeros((len(ALL_NODE_IDs), len(NODE_RESULTS_WUDESIM['TIME_STEP'])))
                for n,node in enumerate(ALL_NODE_IDs):
                    quality_wudesim =  WUDESIM_proj.GET_RESULTS_NODE_WUDESIM(node)['QUALITY'].tolist()
                    wudesim[n] = quality_wudesim
        
                
                _, rel, vul, res = cal_metrics(wudesim, threshold)
                
                vuls[pp,s] =  np.average(vul)
                rels[pp,s] =  np.average(rel)
                ress[pp,s] =  np.average(res)
            
            
    # Plot comparison between EPANET and WUDESIM
    percents *= 100.
    fig, axs = plt.subplots(1,3,figsize=(9, 3),dpi=150)
    axs[0].plot(percents, np.average(vuls, axis=1),'r', lw =2)    
    
    axs[0].fill_between(
                percents, np.amin(vuls, axis=1),
                np.amax(vuls, axis=1),
                color="k", alpha=0.3
            )
#    axs[0].set_xlabel('Percent of conservation nodes')
    axs[0].set_ylabel('Vulnerability')
    
    axs[1].plot(percents, np.average(rels, axis=1),'r', lw =2)    
    
    axs[1].fill_between(
                percents, np.amin(rels, axis=1),
                np.amax(rels, axis=1),
                color="k", alpha=0.3
            )
#    axs[1].set_xlabel('Percent of conservation nodes')
    axs[1].set_ylabel('Reliability')
    
    axs[2].plot(percents, np.average(ress, axis=1),'r', lw =2)    
    
    axs[2].fill_between(
                percents, np.amin(ress, axis=1),
                np.amax(ress, axis=1),
                color="k", alpha=0.3
            )
#    axs[2].set_xlabel('Percent of conservation nodes')
    axs[2].set_ylabel('Resilience')
    
    fig.text(0.5, -0.04, 'Percent of conservation nodes', ha='center')
    plt.tight_layout()
    plt.show()
#    fig.savefig('./results/'+network+"_random_sample.pdf", dpi=150)
    
    return vuls, rels, ress
    

#%%
network = 'ky6'
reduced_ratio = 0.5
n_level = 21
num_trail =30
vuls, rels, ress = RandomReduction(network, reduced_ratio,n_level, num_trail)
    
#%%
from matplotlib.ticker import FormatStrFormatter
percents = np.linspace(0,1,n_level)
percents *= 100.
fig, axs = plt.subplots(1,3,figsize=(9, 3),dpi=150)
axs[2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.tight_layout()
axs[2].plot(percents, np.average(vuls, axis=1),'r', lw =2)    

axs[2].fill_between(
            percents, np.amin(vuls, axis=1),
            np.amax(vuls, axis=1),
            color="k", alpha=0.3
        )
#    axs[0].set_xlabel('Percent of conservation nodes')
axs[2].set_ylabel('Vulnerability')
axs[2].set_title('(c)')

axs[0].plot(percents, np.average(rels, axis=1),'r', lw =2)    

axs[0].fill_between(
            percents, np.amin(rels, axis=1),
            np.amax(rels, axis=1),
            color="k", alpha=0.3
        )
#    axs[1].set_xlabel('Percent of conservation nodes')
axs[0].set_ylabel('Reliability')
axs[0].set_title('(a)')

axs[1].plot(percents, np.average(ress, axis=1),'r', lw =2)    

axs[1].fill_between(
            percents, np.amin(ress, axis=1),
            np.amax(ress, axis=1),
            color="k", alpha=0.3
        )
#    axs[2].set_xlabel('Percent of conservation nodes')
axs[1].set_ylabel('Resilience')
axs[1].set_title('(b)')
fig.text(0.5, -0.04, 'Percent of conservation junctions', ha='center')
plt.show()
plt.tight_layout()
fig.savefig('./results/'+network+'_random.pdf',bbox_inches='tight')
    
              

    
        
        