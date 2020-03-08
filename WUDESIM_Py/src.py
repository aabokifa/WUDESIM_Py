# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 09:46:38 2019

WUDESIM WRAPPER

@author: aaa6859
"""

import ctypes

import pandas as pd

import os

from pkg_resources import resource_filename

import wntr

import matplotlib.pyplot as plt

import numpy as np

#%%

class WUDESIM:
    
    def __init__(self):
        
        ### Load WUDESIM library
    
        os.environ['PATH'] = resource_filename(__name__,'') + os.pathsep + os.environ['PATH']
        
        self.WUDESIM_DLL = ctypes.WinDLL('WUDESIM_LIB.dll')    
 
        self.ENGINE_CLOSE_WUDESIM_PROJ()
        
    #%%
        
    ###########################################################################
    ### define RUN FULL SIMULATION function
    ###########################################################################
        
    def RUN_FULL_SIM(self,EPANET_INP,EPANET_RPT,WUDESIM_INP,WUDESIM_RPT):
        """This function runs a full WUDESIM simulation and writes all output files 
        
        
        Parameters
        ----------
        EPANET_INP : String
            Name of the EPANET input (.INP) file
        EPANET_RPT : String
            Name of the EPANET report (.RPT) file
        WUDESIM_INP : String
            Name of the WUDESIM input (.INP) file
        WUDESIM_RPT : String
            Name of the WUDESIM report (.RPT) file
        """
        global EPANET_INP_glob
        global EPANET_RPT_glob
        global WUDESIM_INP_glob
        global WUDESIM_RPT_glob
        
        # convert string to c_char_p type
        EPANET_INP_glob  = ctypes.c_char_p(str.encode(EPANET_INP))
        EPANET_RPT_glob  = ctypes.c_char_p(str.encode(EPANET_RPT))
        WUDESIM_INP_glob = ctypes.c_char_p(str.encode(WUDESIM_INP))
        WUDESIM_RPT_glob = ctypes.c_char_p(str.encode(WUDESIM_RPT))
        
        # call the full simulation function
        self.WUDESIM_DLL.DE_RUN_FULL_SIM(EPANET_INP_glob,EPANET_RPT_glob,WUDESIM_INP_glob,WUDESIM_RPT_glob)
    
    #%%
        
    ###########################################################################
    ### define ENGINE functions
    ###########################################################################

    def ENGINE_OPEN_EPANET_PROJ(self,EPANET_INP,EPANET_RPT):
        """This function opens a new EPANET project
        
        Parameters
        ----------
        EPANET_INP : String
            Name of the EPANET input (.INP) file
        EPANET_RPT : String
            Name of the EPANET report (.RPT) file
        """
        global EPANET_INP_glob
        global EPANET_RPT_glob


        EPANET_INP_glob  = ctypes.c_char_p(str.encode(EPANET_INP)) 
        EPANET_RPT_glob  = ctypes.c_char_p(str.encode(EPANET_RPT))
        
        self.WUDESIM_DLL.DE_ENGINE_OPEN_EPANET_PROJ(EPANET_INP_glob,EPANET_RPT_glob)
    
    ###########################################################################

    def ENGINE_FIND_DEADENDS(self):
        """This function finds all the dead-end branches in the network
        """
        self.WUDESIM_DLL.DE_ENGINE_FIND_DEADENDS()
    
    ###########################################################################

    def ENGINE_RUN_EPANET_SIM(self):
        """This function runs an EPANET simulation of the whole network
        """
        self.WUDESIM_DLL.DE_ENGINE_RUN_EPANET_SIM()
    
    ###########################################################################

    def ENGINE_CALC_DEADEND_PROPERTIES_EPANET(self):
        """This function calculates the average properties of all the 
        dead-end branches in the network
        """
        self.WUDESIM_DLL.DE_ENGINE_CALC_DEADEND_PROPERTIES_EPANET()
    
    ###########################################################################

    def ENGINE_OPEN_WUDESIM_PROJ(self,WUDESIM_INP,WUDESIM_RPT):
        """This function opens a new WUDESIM project
        
        Parameters
        ----------
        WUDESIM_INP : String
            Name of the WUDESIM input (.INP) file
        WUDESIM_RPT : String
            Name of the WUDESIM report (.RPT) file
        """
        
        global WUDESIM_INP_glob
        global WUDESIM_RPT_glob
        
        WUDESIM_INP_glob = ctypes.c_char_p(str.encode(WUDESIM_INP))
        WUDESIM_RPT_glob = ctypes.c_char_p(str.encode(WUDESIM_RPT))
        self.WUDESIM_DLL.DE_ENGINE_OPEN_WUDESIM_PROJ(WUDESIM_INP_glob,WUDESIM_RPT_glob)
    
    ###########################################################################

    def ENGINE_GENERATE_STOC_DEMAND(self):
        """This function generates stochastic demands for the dead-end 
        branches selected in the WUDESIM_INP file
        """
        self.WUDESIM_DLL.DE_ENGINE_GENERATE_STOC_DEMAND()
    
    ###########################################################################

    def ENGINE_RUN_WUDESIM_SIM(self):
        """This function runs a WUDESIM simulation for the dead-end 
        branches selected in the WUDESIM_INP file
        """
        self.WUDESIM_DLL.DE_ENGINE_RUN_WUDESIM_SIM()
    
    ###########################################################################

    def ENGINE_CLOSE_WUDESIM_PROJ(self):
        """This function closes the WUDESIM DLL toolkit and releases all 
        the memory
        """
        self.WUDESIM_DLL.DE_ENGINE_CLOSE_WUDESIM_PROJ()
    
    #%%    
    
    ###########################################################################
    ### define WRITE output/report files functions
    ###########################################################################
    
    def WRITE_DEADEND_IDS(self):
        """This function writes the IDs of the dead-end branches to an output 
        file
        """
        self.WUDESIM_DLL.DE_WRITE_DEADEND_IDS()
    
    ###########################################################################

    def WRITE_DEADEND_PROPERTIES(self):
        """This function writes the properties of dead-end branches to an 
        output file
        """
        self.WUDESIM_DLL.DE_WRITE_DEADEND_PROPERTIES()
    
    ###########################################################################

    def WRITE_STOCHASTIC_DEMANDS(self):
        """This function writes the generated stochastic demands to an output
        file
        """
        self.WUDESIM_DLL.DE_WRITE_STOCHASTIC_DEMANDS()
    
    ###########################################################################

    def WRITE_WUDESIM_REPORT(self):
        """This function writes the WUDESIM report file
        """
        self.WUDESIM_DLL.DE_WRITE_WUDESIM_REPORT() 
       
    ###########################################################################

    def WRITE_EPANET_REPORT(self):
        """This function writes the EPANET report file
        """
        self.WUDESIM_DLL.DE_WRITE_EPANET_REPORT()     
        
    #%%   
    
    ###########################################################################
    ### define GET Property functions
    ###########################################################################
       
    def GET_BRAN_COUNT (self,property_type):    
        """This function returns the number of dead-end branches in the network
        
        Parameters
        ----------
        property_type : string
            Options:
                "BRAN_COUNT" :            The function returns the count of dead-end branches
        """

        switcher = {
        "BRAN_COUNT" :            self.WUDESIM_DLL.DE_GET_BRAN_COUNT(0),
                }
        return switcher.get(property_type,"INVALID")

    ###########################################################################
       
    def GET_STEP_COUNT (self,property_type):    
        """This function returns the number of simulation time steps
        
        Parameters
        ----------
        property_type : string
            Options:
                "EPANET_STEP_COUNT" :     The function returns the count of EPANET steps
                "STOCHASTIC_STEP_COUNT" : The function returns the count of stochastic steps
        """

        switcher = {
        "EPANET_STEP_COUNT" :     self.WUDESIM_DLL.DE_GET_STEP_COUNT(0),
        "STOCHASTIC_STEP_COUNT" : self.WUDESIM_DLL.DE_GET_STEP_COUNT(1),
                }
        return switcher.get(property_type,"INVALID")
    
    ###########################################################################

    def GET_BRAN_SIZE (self,property_type,branch_idx):
        """This function returns the size of a selected dead-end branch
        
        Parameters
        ----------
        property_type : string
            Options:
                "BRAN_SIZE": The function returns the size of the dead-end branch
        branch_idx : int
            The index of the dead-end branch
        """

        switcher = {
        "BRAN_SIZE" : self.WUDESIM_DLL.DE_GET_BRAN_SIZE(0,branch_idx)    
               }
        return switcher.get(property_type,"INVALID")
  
    ###########################################################################

    def GET_PIPE_PROPERTY(self,property_type,branch_idx,pipe_idx):
        """This function returns the properties of a specific dead-end pipe
        
        Parameters
        ----------
        property_type : string
            Options:
                "LENGTH":        The function returns the length of the pipe
                "DIAMETER":      The function returns the diameter of the pipe
        branch_idx : int
            The index of the dead-end branch
        pipe_idx : int
            The index of the dead-end pipe
        """

        self.WUDESIM_DLL.DE_GET_PIPE_PROPERTY.restype = ctypes.c_double
        switcher = {
        "LENGTH":     self.WUDESIM_DLL.DE_GET_PIPE_PROPERTY(0,branch_idx,pipe_idx),
        "DIAMETER":   self.WUDESIM_DLL.DE_GET_PIPE_PROPERTY(1,branch_idx,pipe_idx),
                }
        return switcher.get(property_type,"INVALID")
    
    #%%   
    
    ###########################################################################
    ### define WUDESIM GET Result functions
    ###########################################################################
    
    def GET_PIPE_RESULT_EPANET(self,property_type,branch_idx,pipe_idx,time_step):
        """This function returns the result of EPANET simulation for a 
        specific dead-end pipe at a specific time step
        
        Parameters
        ----------
        property_type : string
            Options:
                "REYNOLDS":   The function returns the Reynolds number
                "RES_TIME":   The function returns the residence time
                "FLOW":      The function returns the flow 
        branch_idx : int
            The index of the dead-end branch
        pipe_idx : int
            The index of the dead-end pipe
        time_step : int
            The time step
        """
        self.WUDESIM_DLL.DE_GET_PIPE_RESULT_EPANET.restype = ctypes.c_double
        switcher = {
        "REYNOLDS":     self.WUDESIM_DLL.DE_GET_PIPE_RESULT_EPANET(0,branch_idx,pipe_idx,time_step),
        "RES_TIME":     self.WUDESIM_DLL.DE_GET_PIPE_RESULT_EPANET(1,branch_idx,pipe_idx,time_step),
        "FLOW":         self.WUDESIM_DLL.DE_GET_PIPE_RESULT_EPANET(2,branch_idx,pipe_idx,time_step),
                }
        return switcher.get(property_type,"INVALID")
    
    ###########################################################################    

    def GET_PIPE_RESULT_WUDESIM(self,property_type,branch_idx,pipe_idx,time_step):
        """This function returns the result of WUDESIM simulation for a 
        specific dead-end pipe at a specific time step
        
        Parameters
        ----------
        property_type : string
            Options:
                "REYNOLDS":         The function returns the Reynolds number
                "RES_TIME":         The function returns the residence time
                "PECLET":           The function returns the Peclet number
        branch_idx : int
            The index of the dead-end branch
        pipe_idx : int
            The index of the dead-end pipe
        time_step : int
            The time step
        """

        self.WUDESIM_DLL.DE_GET_PIPE_RESULT_WUDESIM.restype = ctypes.c_double
        switcher = {
        "REYNOLDS":         self.WUDESIM_DLL.DE_GET_PIPE_RESULT_WUDESIM(0,branch_idx,pipe_idx,time_step),
        "RES_TIME":         self.WUDESIM_DLL.DE_GET_PIPE_RESULT_WUDESIM(1,branch_idx,pipe_idx,time_step),
        "PECLET":           self.WUDESIM_DLL.DE_GET_PIPE_RESULT_WUDESIM(2,branch_idx,pipe_idx,time_step),
                }
        return switcher.get(property_type,"INVALID")
    
    ###########################################################################

    def GET_NODE_RESULT_EPANET(self,property_type,branch_idx,node_idx,time_step):
        """This function returns the results of EPANET simulation for a 
        specific dead-end node at a specific time step
        
        Parameters
        ----------
        property_type : string
            Options:
                "QUALITY":  The function returns the water quality simulated by EPANET
                "DEMAND":   The function returns the water demand simulated by EPANET 
        branch_idx : int
            The index of the dead-end branch
        node_idx : int
            The index of the dead-end node
        time_step : int
            The time step
        """

        self.WUDESIM_DLL.DE_GET_NODE_RESULT_EPANET.restype = ctypes.c_double
        switcher = {
        "QUALITY":   self.WUDESIM_DLL.DE_GET_NODE_RESULT_EPANET(0,branch_idx,node_idx,time_step),
        "DEMAND":    self.WUDESIM_DLL.DE_GET_NODE_RESULT_EPANET(1,branch_idx,node_idx,time_step),    
                }
        return switcher.get(property_type,"INVALID")
    
    ###########################################################################

    def GET_NODE_RESULT_WUDESIM(self,property_type,branch_idx,node_idx,time_step):
        """This function returns the results of WUDESIM simulation for a 
        specific dead-end node at a specific time step
        
        Parameters
        ----------
        property_type : string
            Options:
                "QUALITY":  The function returns the concentration simulated by WUDESIM
        branch_idx : int
            The index of the dead-end branch
        node_idx : int
            The index of the dead-end node
        time_step : int
            The time step
        """

        self.WUDESIM_DLL.DE_GET_NODE_RESULT_WUDESIM.restype = ctypes.c_double
        switcher = {
        "QUALITY":   self.WUDESIM_DLL.DE_GET_NODE_RESULT_WUDESIM(0,branch_idx,node_idx,time_step),
                }
        return switcher.get(property_type,"INVALID")
    
    ###########################################################################

    def GET_STOC_FLOW(self,property_type,branch_idx,pipe_idx,time_step):
        """This function returns the stochastic flow generated by WUDESIM for 
        a specific dead-end pipe at a specific time step
        
        Parameters
        ----------
        property_type : string
            Options:
                "FLOW" :   The function returns the stochastic flow of the pipe
                "DEMAND" : The function returns the stochastic demand

        branch_idx : [type]
            The index of the dead-end branch
        pipe_idx : [type]
            The index of the dead-end pipe
        time_step : [type]
            The time step
        """

        self.WUDESIM_DLL.DE_GET_STOC_FLOW.restype = ctypes.c_double
        switcher = {
        "FLOW":   self.WUDESIM_DLL.DE_GET_STOC_FLOW(0,branch_idx,pipe_idx,time_step),
        "DEMAND": self.WUDESIM_DLL.DE_GET_STOC_FLOW(1,branch_idx,pipe_idx,time_step),
                }
        return switcher.get(property_type,"INVALID")  
     
    #%%   
    
    ###########################################################################
    ### define GET Index/ID functions
    ###########################################################################
    
    def GET_IDX_BRANCH(self,branch_id):
        """This function returns the index (int) of a dead-end branch 
        
        Parameters
        ----------
        branch_id : string
            The ID of the dead-end branch
        """
        all_branch_ids = self.GET_ALL_BRANCH_IDs()
        branch_idx = all_branch_ids.index(branch_id)
        return branch_idx
    
    ###########################################################################

    def GET_IDX_PIPE(self,pipe_id):
        """This function returns the index of a dead-end pipe 
        
        Returns
        -------
        [branch idx (int), pipe idx (int)]
        
        
        Parameters
        ----------
        pipe_id : string
            The ID of the dead-end pipe
        """
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
            
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
            
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for pipe_idx in range(BRAN_SIZE[branch_idx]):
                dum = self.GET_ID("PIPE_ID",branch_idx,pipe_idx)                
                if (pipe_id == dum): return [branch_idx,pipe_idx]           
    
    ###########################################################################

    def GET_IDX_NODE(self,node_id):
        """This function returns the index of a dead-end node
        
        Returns
        -------
        [branch idx (int), node idx (int)]
        
        
        Parameters
        ----------
        node_id : string
            The ID of the dead-end node
        """
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
            
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
            
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for node_idx in range(BRAN_SIZE[branch_idx]):
                dum = self.GET_ID("NODE_ID",branch_idx,node_idx)                
                if (node_id == dum): return [branch_idx,node_idx] 
                
    ###########################################################################
                
    def GET_ID(self,property_type,branch_idx,pipe_node_idx=0):
        """This function returns the ID of a dead-end branch/pipe/node
        
        Parameters
        ----------
        property_type : string
            Options:
                "PIPE_ID" : The function returns the ID of a dead-end pipe 
                "NODE_ID" : The function returns the ID of a dead-end node
                "BRAN_ID" : The function returns the ID of a dead-end branch
        branch_idx : int
            The index of the dead-end branch
        pipe_node_idx : int, optional
            The index of the dead-end pipe/node, by default 0
        """    

        self.WUDESIM_DLL.DE_GET_ID.restype = ctypes.c_char_p
        switcher = {
        "PIPE_ID" : self.WUDESIM_DLL.DE_GET_ID(0,branch_idx,pipe_node_idx).decode("utf-8"), 
        "NODE_ID" : self.WUDESIM_DLL.DE_GET_ID(1,branch_idx,pipe_node_idx).decode("utf-8"),
        "BRAN_ID" : self.WUDESIM_DLL.DE_GET_ID(2,branch_idx,pipe_node_idx).decode("utf-8"),         
                }
        return switcher.get(property_type,"INVALID")
    
    #%%     
        
    ###########################################################################
    ### define GET ALL IDs functions
    ###########################################################################
    
    def GET_ALL_BRANCH_IDs(self):
        """This function returns a list of the IDs of all dead-end branches
        """
        # Initialize pipe id list
        ALL_IDs = []
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
            
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            ALL_IDs.append(self.GET_ID("BRAN_ID",branch_idx))
                    
        return ALL_IDs
    
    ###########################################################################
       
    def GET_ALL_PIPE_IDs(self):
        """This function returns a list of the IDs of all dead-end pipes
        """
        # Initialize pipe id list
        ALL_IDs = []
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
    
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
        
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for pipe_idx in range(BRAN_SIZE[branch_idx]):        
                    ALL_IDs.append(self.GET_ID("PIPE_ID",branch_idx,pipe_idx))
                    
        return ALL_IDs
    
    ###########################################################################
    
    def GET_ALL_NODE_IDs(self):
        """This function returns a list of the IDs of all dead-end nodes
        """
        # Initialize pipe id list
        ALL_IDs = []
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
    
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
        
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for pipe_idx in range(BRAN_SIZE[branch_idx]):        
                    ALL_IDs.append(self.GET_ID("NODE_ID",branch_idx,pipe_idx))
                    
        return ALL_IDs
    
    #%%     
        
    ###########################################################################
    ### define GET ALL Properties functions
    ###########################################################################
    
    def GET_ALL_BRAN_PROPERTIES_EPANET(self):
        """This function returns a list of the properties of all dead-end branches
        'Branch_ID' | 'Branch_Size' | 'Tot_Length (m)'  | Tot_ResT (sec)
        """
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")

        # Get the number of steps
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")   
        
        # Initialize branch ID, size, length, and residence time lists
        Branch_IDs    = []
        BRAN_SIZES    = []
        BRAN_Lengths  = []
        BRAN_ResT     = []
        
        # Get the properties of each branch
        for branch_idx in range(N_BRANCHES):    
            
            Branch_IDs.append(self.GET_ID("BRAN_ID",branch_idx))
            
            BRAN_SIZES.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
            
            # get the length and residence time of pipes in the branch
            Pipe_Lengths = []
            AVG_RES_TIME = []
            
            for pipe_idx in range(BRAN_SIZES[branch_idx]):                

                Pipe_Lengths.append(self.GET_PIPE_PROPERTY("LENGTH",branch_idx,pipe_idx))   
                
                # Get residence time in the pipe
                Res_time = []
                
                for time_step in range(0,N_STEPS):
                    
                    Res_time.append(self.GET_PIPE_RESULT_EPANET("RES_TIME",branch_idx,pipe_idx,time_step))
                
                AVG_RES_TIME.append(np.mean(Res_time))


            
            BRAN_Lengths.append(sum(Pipe_Lengths))
            BRAN_ResT.append(sum(AVG_RES_TIME))
            
        df = pd.DataFrame({
                           'Branch_ID':      Branch_IDs,
                           'Branch_Size':    BRAN_SIZES,
                           'Tot_Length (m)': BRAN_Lengths,
                           'Tot_ResT (sec)': BRAN_ResT,
                           })
            
        return df
    
    ###########################################################################

    def GET_ALL_PIPE_PROPERTIES_EPANET(self):
        """This function returns a dataframe of the properties of all dead-end 
        pipes as simulated by EPANET:
            'Branch_ID' | 'Pipe_ID' | 'Length (m)' | 'Diameter(m)' | 'Avg_Reynolds' | 'Avg_Res_time' | 'Avg_Flow(m3/s)'
        """
        
        # Initialize branch number list
        Branch_ID = []
        
        # Initialize pipe id list
        ALL_IDs = []
        
        # Initialize lists of pipe properties
        Length           = []
        Diameter         = []
        Avg_Reynolds     = []
        Avg_Res_time     = []
        Avg_Flow         = []
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
    
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
        
        # Get the number of steps
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")    
        
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for pipe_idx in range(BRAN_SIZE[branch_idx]):        
                
                Branch_ID.append(self.GET_ID("BRAN_ID",branch_idx))
                ALL_IDs.append(self.GET_ID("PIPE_ID",branch_idx,pipe_idx))
                Length.append(self.GET_PIPE_PROPERTY("LENGTH",branch_idx,pipe_idx))
                Diameter.append(self.GET_PIPE_PROPERTY("DIAMETER",branch_idx,pipe_idx))
                
                # Get Reynolds and Res Time
                Reynolds = []
                Res_time = []
                Flow     = []
                for time_step in range(0,N_STEPS):        
                    
                    Reynolds.append(self.GET_PIPE_RESULT_EPANET("REYNOLDS",branch_idx,pipe_idx,time_step))
                    Res_time.append(self.GET_PIPE_RESULT_EPANET("RES_TIME",branch_idx,pipe_idx,time_step))
                    Flow.append(self.GET_PIPE_RESULT_EPANET("FLOW",branch_idx,pipe_idx,time_step))

                Avg_Reynolds.append(np.mean(Reynolds))
                Avg_Res_time.append(np.mean(Res_time))
                Avg_Flow.append(np.mean(Flow))
        
        df = pd.DataFrame({
                           'Branch_ID':        Branch_ID,
                           'Pipe_ID':          ALL_IDs,
                           'Length (m)':       Length, 
                           'Diameter(m)':      Diameter, 
                           'Avg_Reynolds':     Avg_Reynolds, 
                           'Avg_Res_time':     Avg_Res_time,
                           'Avg_Flow(m3/s)':   Avg_Flow,
                           })
            
        return df
    
    ###########################################################################

    def GET_ALL_NODE_PROPERTIES_EPANET(self):
        """This function returns a dataframe of the properties of all dead-end 
        nodes as simulated by EPANET:
            'Branch_ID' | 'Node_ID' | 'AVG_QUAL' | 'Avg_DEM(m3/s)'
        """
        # Initialize branch number list
        Branch_ID = []
        
        # Initialize node id list
        ALL_IDs = []
        
        # Initialize lists of pipe properties
        Avg_QUAL     = []
        Avg_DEMAND   = []
        
        # Get number of branches
        N_BRANCHES = self.GET_BRAN_COUNT("BRAN_COUNT")
    
        # Get the size of each branch
        BRAN_SIZE = []
        for branch_idx in range(N_BRANCHES):    
            BRAN_SIZE.append(self.GET_BRAN_SIZE("BRAN_SIZE",branch_idx))
            
        # Get the number of steps
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")    
        
        # Get pipe ids of all dead-end pipes    
        for branch_idx in range(N_BRANCHES):
            for node_idx in range(BRAN_SIZE[branch_idx]):        
                Branch_ID.append(self.GET_ID("BRAN_ID",branch_idx))
                ALL_IDs.append(self.GET_ID("NODE_ID",branch_idx,node_idx))

                QUAL   = []
                DEMAND = []
                for time_step in range(0,N_STEPS):        
                    QUAL.append(self.GET_NODE_RESULT_EPANET("QUALITY",branch_idx,node_idx,time_step))
                    DEMAND.append(self.GET_NODE_RESULT_EPANET("DEMAND",branch_idx,node_idx,time_step))

                Avg_QUAL.append(np.mean(QUAL))
                Avg_DEMAND.append(np.mean(DEMAND))
        
        df = pd.DataFrame({
                           'Branch_ID':     Branch_ID,
                           'Node_ID':       ALL_IDs,
                           'AVG_QUAL':      Avg_QUAL,
                           'Avg_DEM(m3/s)': Avg_DEMAND                           
                           })
            
        return df    

    #%%    
        
    ###########################################################################
    ### define WUDESIM GET TIMESERIES functions
    ###########################################################################

    def GET_TIMESERIES_PIPE_WUDESIM(self,pipe_id):
        """This function returns a dataframe of the WUDESIM simulation results 
        for a specific dead-end pipe:
            'TIME_STEP' | 'REYNOLDS' | 'RES_TIME' | 'PECLET'

        Parameters
        ----------
        pipe_id : string
            The ID of the dead-end pipe
        """
        
        # Get branch idx, pipe idx
        [branch_idx,pipe_idx] = self.GET_IDX_PIPE(pipe_id)
        
        # Initialize lists of pipe results
        Timestep    = []
        Reynolds    = []
        Peclet      = []
        Res_time    = []
        
        # Get number of steps
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            Reynolds.append(self.GET_PIPE_RESULT_WUDESIM("REYNOLDS",branch_idx,pipe_idx,time_step))
            Peclet.append(self.GET_PIPE_RESULT_WUDESIM("PECLET",branch_idx,pipe_idx,time_step))        
            Res_time.append(self.GET_PIPE_RESULT_WUDESIM("RES_TIME",branch_idx,pipe_idx,time_step))
        
        df = pd.DataFrame({'TIME_STEP': Timestep,
                           'REYNOLDS': Reynolds, 
                           'RES_TIME': Res_time,
                           'PECLET':   Peclet,
                           })
            
        return df
    
    ###########################################################################
    
    def GET_TIMESERIES_PIPE_EPANET(self,pipe_id):
        """This function returns a dataframe of the EPANET simulation results 
        for a specific dead-end pipe:
            'TIME_STEP' | 'REYNOLDS' | 'RES_TIME' | 'FLOW(m3/s)'

        Parameters
        ----------
        pipe_id : string
            The ID of the dead-end pipe
        """
        
        # Get branch idx, pipe idx
        [branch_idx,pipe_idx] = self.GET_IDX_PIPE(pipe_id)
        
        # Initialize lists of pipe results
        Timestep    = []
        Reynolds    = []
        Res_time    = []
        Flow        = []

        # Get number of steps
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            Reynolds.append(self.GET_PIPE_RESULT_EPANET("REYNOLDS",branch_idx,pipe_idx,time_step))
            Res_time.append(self.GET_PIPE_RESULT_EPANET("RES_TIME",branch_idx,pipe_idx,time_step))
            Flow.append(self.GET_PIPE_RESULT_EPANET("FLOW",branch_idx,pipe_idx,time_step))        

        
        df = pd.DataFrame({'TIME_STEP': Timestep,
                           'REYNOLDS': Reynolds, 
                           'RES_TIME': Res_time,
                           'FLOW(m3/s)': Flow,
                           })
            
        return df
    
    ###########################################################################

    def GET_TIMESERIES_NODE_WUDESIM(self,node_id):
        """This function returns a dataframe of the simulation results for a 
        specific dead-end pipe:
            'TIME_STEP' | 'QUALITY' 
        
        Parameters
        ----------
        node_id : string
            The ID of the dead-end node
        """
        # Get branch idx, node idx
        [branch_idx,node_idx] = self.GET_IDX_NODE(node_id)
        
        # Initialize lists of node results
        Timestep = []
        QUALITY  = []
        
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            QUALITY.append(self.GET_NODE_RESULT_WUDESIM("QUALITY",branch_idx,node_idx,time_step))

        df = pd.DataFrame({'TIME_STEP': Timestep,
                           'QUALITY': QUALITY, 
                           })            
        return df
        
    ###########################################################################

    def GET_TIMESERIES_NODE_EPANET(self,node_id):
        """This function returns a dataframe of the simulation results for a 
        specific dead-end pipe:
            'TIME_STEP' | 'QUALITY' | 'DEMAND(m3/s)' 
        
        Parameters
        ----------
        node_id : string
            The ID of the dead-end node
        """
        # Get branch idx, node idx
        [branch_idx,node_idx] = self.GET_IDX_NODE(node_id)

        # Initialize lists of node results
        Timestep  = []
        QUALITY   = []
        DEMAND    = []
        
        N_STEPS    = self.GET_STEP_COUNT("EPANET_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            QUALITY.append(self.GET_NODE_RESULT_EPANET("QUALITY",branch_idx,node_idx,time_step))
            DEMAND.append(self.GET_NODE_RESULT_EPANET("DEMAND",branch_idx,node_idx,time_step))


        df = pd.DataFrame({'TIME_STEP': Timestep,
                           'QUALITY': QUALITY,
                           'DEMAND(m3/s)': DEMAND,
                           })            
        return df
    
    ###########################################################################

    def GET_TIMESERIES_STOC_FLOWS(self,pipe_id):
        """This function returns a dataframe of the stochastic flows generated by WUDESIM for 
        a specific dead-end pipe
        
        Parameters
        ----------
        pipe_id : string
            The ID of the dead-end pipe
        """

        # Get branch idx, pipe idx
        [branch_idx,pipe_idx] = self.GET_IDX_PIPE(pipe_id)
        
        # Initialize lists of pipe results
        Timestep        = []
        Flow_STOCHASTIC = []
        
        # Get number of steps
        N_STEPS    = self.GET_STEP_COUNT("STOCHASTIC_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            Flow_STOCHASTIC.append(self.GET_STOC_FLOW("FLOW",branch_idx,pipe_idx,time_step))        
        
        df = pd.DataFrame({'TIME_STEP': Timestep,                          
                           'FLOW (m3/s)':Flow_STOCHASTIC})
            
        return df

    
    ###########################################################################

    def GET_TIMESERIES_STOC_DEMANDS(self,node_id):
        """This function returns a dataframe of the stochastic flows generated by WUDESIM for 
        a specific dead-end pipe
        
        Parameters
        ----------
        pipe_id : string
            The ID of the dead-end pipe
        """

        # Get branch idx, pipe idx
        [branch_idx,node_idx] = self.GET_IDX_NODE(node_id)
        
        # Initialize lists of pipe results
        Timestep = []
        DEMAND   = []
        
        # Get number of steps
        N_STEPS    = self.GET_STEP_COUNT("STOCHASTIC_STEP_COUNT")
    
        for time_step in range(0,N_STEPS):        
            Timestep.append(time_step)
            DEMAND.append(self.GET_STOC_FLOW("DEMAND",branch_idx,node_idx,time_step))        
        
        df = pd.DataFrame({'TIME_STEP': Timestep,                          
                           'DEMAND (m3/s)':DEMAND})
            
        return df        
    
    #%%
        
    ###########################################################################
    ### define WUDESIM VISUALIZE functions
    ###########################################################################
            
    def VISUALIZE_LAYOUT_PIPES(self,EPANET_INP,pipe_ids=[],labels=False,ax=None):
        """This function plots the layout of the network highlighting specific 
        pipes
        
        Parameters
        ----------
        EPANET_INP : string
            Name of the EPANET input file
        pipe_ids : list, optional
            IDs of the pipes that will be highlighted, by default []
        labels : bool, optional
            Whether to write the IDs of the pipes on the plot, by default False
        ax : matplotlib axis, optional
            Axis of a matplotlib figure, by default None
        """
        
        if ax==None:
            fig, ax = plt.subplots(figsize=(10, 10),dpi=300)

        wn = wntr.network.WaterNetworkModel(EPANET_INP)    
        wntr.graphics.network.plot_network(wn,link_attribute=pipe_ids,ax=ax,link_labels=labels)
    
    ###########################################################################
            
    def VISUALIZE_LAYOUT_NODES(self,EPANET_INP,node_ids=[],labels=False,ax=None):
        """This function plots the layout of the network highlighting specific 
        nodes
        
        Parameters
        ----------
        EPANET_INP : string
            Name of the EPANET input file
        node_ids : list, optional
            IDs of the nodes that will be highlighted, by default []
        labels : bool, optional
            Whether to write the IDs of the nodes on the plot, by default False
        ax : matplotlib axis, optional
            Axis of a matplotlib figure, by default None
        """
        
        if ax==None:
            fig, ax = plt.subplots(figsize=(10, 10),dpi=300)

        wn = wntr.network.WaterNetworkModel(EPANET_INP)    
        wntr.graphics.network.plot_network(wn,node_attribute=node_ids,ax=ax,node_labels=labels)
        
    ###########################################################################
            
    def VISUALIZE_TIMESERIES_NODE(self,node_id,ax=None):
        """This function plots the timeseries water quality results of both 
        EPANET and WUDESIM for a node
        
        Parameters
        ----------
        pipe_id : string
            ID of the node to be plotted
        ax : matplotlib axis, optional
            Axis of a matplotlib figure, by default None
        """
        
        NODE_RESULTS_EPANET  = self.GET_TIMESERIES_NODE_EPANET(node_id)
        NODE_RESULTS_WUDESIM = self.GET_TIMESERIES_NODE_WUDESIM(node_id)
        
        if ax==None:
            fig, ax = plt.subplots(figsize=(10, 10),dpi=300)
            plt.rcParams.update({'font.size': 22})
            
        ax.plot(NODE_RESULTS_EPANET['TIME_STEP'],NODE_RESULTS_EPANET['QUALITY'],'b')    
        ax.plot(NODE_RESULTS_WUDESIM['TIME_STEP'],NODE_RESULTS_WUDESIM ['QUALITY'],'r')
        ax.legend(['EPANET_QUAL','WUDESIM_QUAL'],bbox_to_anchor=(1.0, 1.0))
        ax.set_title('Timeseries results for node ' + node_id)   
        ax.set_xlabel('Timestep')       
        ax.set_ylabel('Quality')     
        
    ###########################################################################
            
    def VISUALIZE_TIMESERIES_PIPE(self,pipe_id,ax=None):
        """This function plots the timeseries results of both 
        EPANET and WUDESIM  for a pipe
        
        Parameters
        ----------
        pipe_id : string
            ID of the pipe to be plotted
        ax : matplotlib axis, optional
            Axis of a matplotlib figure, by default None
        """
        
        PIPE_RESULTS_EPANET  = self.GET_TIMESERIES_PIPE_EPANET(pipe_id)
        PIPE_RESULTS_WUDESIM = self.GET_TIMESERIES_PIPE_WUDESIM(pipe_id)
        
        if ax==None:
            fig, ax = plt.subplots(figsize=(10, 10),dpi=300)
            plt.rcParams.update({'font.size': 22})
            
        ax.plot(PIPE_RESULTS_EPANET['TIME_STEP'],PIPE_RESULTS_EPANET['REYNOLDS'],'b')    
        ax.plot(PIPE_RESULTS_WUDESIM['TIME_STEP'],PIPE_RESULTS_WUDESIM ['REYNOLDS'],'r')
        ax.legend(['EPANET_REYN','WUDESIM_REYN'],bbox_to_anchor=(1.0, 1.0))
        ax.set_title('Timeseries results for pipe ' + pipe_id)   
        ax.set_xlabel('Timestep')       
        ax.set_ylabel('Reynolds')        

        
        
#%%        
        
        