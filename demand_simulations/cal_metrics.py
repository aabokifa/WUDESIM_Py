# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 08:28:17 2020

@author: lx2347
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
def cal_metrics(data, threshold):
    
    endtime = np.shape(data)[1]
    starttime = 100
    time = np.arange(starttime, endtime)
    data = data[:,time]
    nn = len(data)
    tn = len(time)
    
    
    state = np.zeros((nn,tn)) # state indicator
    deft = np.zeros((nn,tn)) # state indicator
    transition = np.zeros((nn,tn-1)) #transition indicator 
    res = np.zeros(nn) # resillience metrics for each junction 
    rel = np.zeros(nn) #reliability metrics for each junction
    vul = np.zeros(nn)
    for n, x in enumerate(data):
        state[n] = [1 if i>threshold else 0 for i in x]
        deft[n] = [max(0,threshold-i)/threshold for i in x]
        transition[n] = [1 if x[i]<threshold and x[i+1]>threshold else 0 for i in range(tn-1)]
        rel[n] = np.sum(state[n])/tn
        res[n] = np.sum(transition[n]) / (tn-np.sum(state[n]))
        vul[n] = np.sum(deft[n]) / (tn-np.sum(state[n]))
    
#    vul = (nn-np.sum(state, axis=0))/nn # for the entire network 

    return time, rel, vul[~np.isnan(vul)], res[~np.isnan(res)]


def compare_metrics(epanet, wudesim, threshold, filename, reduce=False, plot=True, save=True):
    time_epa, rel_epa, vul_epa, res_epa = cal_metrics(epanet, threshold)
    time_wud, rel_wud, vul_wud, res_wud = cal_metrics(wudesim, threshold)
    N = len(epanet)
    if plot == True:
        fig1, axs1 = plt.subplots(1,3,figsize=(9, 3),dpi=150)
        plt.tight_layout()
        fig2, axs2 = plt.subplots(1,3,figsize=(9, 3),dpi=150)
        plt.tight_layout()
#        axs1[0].plot(time_epa, vul_epa, 'k', label ='EPANET')
#        axs1[0].plot(time_wud, vul_wud, 'r', label ='WUDESIM')
#        axs1[0].set_xlabel('Time [h]')
#        axs1[0].set_ylabel('Vulnebility')
##        axs1[0].legend()
#        
#        axs2[0].plot(time_epa, vul_epa, 'k', label ='EPANET')
#        axs2[0].plot(time_wud, vul_wud, 'r', label ='WUDESIM')
#        axs2[0].set_xlabel('Time [h]')
#        axs2[0].set_ylabel('Vulnebility')
#        axs2[0].set_title('(a)')
##        axs2[0].legend()
        
        bins = np.linspace(0, 1, 10)
        width = 0.04
        label=['EPANET','WUDESIM']
        n,_, _ = axs1[2].hist([vul_epa,vul_wud], bins, color = ['k','r'],label=label)
        axs1[2].set_ylabel('Number of junctions')
        axs1[2].set_xlabel('Vulnerability')
#        axs1[1].legend()
        
        n[0] = n[0]/np.sum(n[0])
        n[1] = n[1]/np.sum(n[1])
        b= np.array([(bins[i] +bins[i+1])/2 for i in range(len(bins)-1)])
        axs2[2].bar(b - 0.5*width, n[0], width, color='k', label='EPANET')
        axs2[2].bar(b + 0.5*width, n[1], width, color='r', label='WUDESIM')
        axs2[2].set_ylabel('Probability')
        axs2[2].set_xlabel('Vulnerability')
        axs2[2].set_title('(c)')
        
        bins = np.linspace(0, 1, 10)
        width = 0.04
        label=['EPANET','WUDESIM']
        n,_, _ = axs1[0].hist([rel_epa,rel_wud], bins, color = ['k','r'],label=label)
        axs1[0].set_ylabel('Number of junctions')
        axs1[0].set_xlabel('Reliability')
#        axs1[1].legend()
        
        n[0] = n[0]/np.sum(n[0])
        n[1] = n[1]/np.sum(n[1])
        b= np.array([(bins[i] +bins[i+1])/2 for i in range(len(bins)-1)])
        axs2[0].bar(b - 0.5*width, n[0], width, color='k', label='EPANET')
        axs2[0].bar(b + 0.5*width, n[1], width, color='r', label='WUDESIM')
        axs2[0].set_ylabel('Probability')
        axs2[0].set_xlabel('Reliability')
        axs2[0].set_title('(a)')
#        axs2[1].legend()
        
    #    axs[2].hist([res_epa,res_wud], bins, color = ['k','r'],label=label)
        n,_, _ = axs1[1].hist([res_epa,res_wud], bins, color = ['k','r'],label=label)
        axs1[1].set_ylabel('Number of junctions')
        axs1[1].set_xlabel('Resillience')
#        axs1[2].legend()
        
        n[0] = n[0]/np.sum(n[0])
        n[1] = n[1]/np.sum(n[1])
        b= np.array([(bins[i] +bins[i+1])/2 for i in range(len(bins)-1)])
        axs2[1].bar(b - 0.5*width, n[0], width, color='k', label='EPANET')
        axs2[1].bar(b + 0.5*width, n[1], width, color='r', label='WUDESIM')
        axs2[1].set_ylabel('Probability')
        axs2[1].set_xlabel('Resillience')
        axs2[1].set_title('(b)')
#        axs2[2].legend()
        plt.show()
        fig2.savefig('./results/'+filename+'.pdf',bbox_inches='tight')
    
    #%% sumerize
    summary = pd.DataFrame(index=['EPANET', 'WUDESIM'],
                           columns=[ 'reliability', 'resilience','vulnerability',]) 
    
    summary.xs('EPANET')['vulnerability'] =  np.average(vul_epa)
    summary.xs('EPANET')['reliability'] =  np.average(rel_epa)
    summary.xs('EPANET')['resilience'] =  np.average(res_epa)
    summary.xs('WUDESIM')['vulnerability'] =  np.average(vul_wud)
    summary.xs('WUDESIM')['reliability'] =  np.average(rel_wud)
    summary.xs('WUDESIM')['resilience'] =  np.average(res_wud)
    print(summary)
    if save == True: 
        
        summary.to_csv('./results/'+filename+'.csv')
    return summary
    
        
    