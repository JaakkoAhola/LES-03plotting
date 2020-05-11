#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:38:34 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import time

import numpy
import sys
import xarray
from Simulation import Simulation
from Data import Data

class SimulationDataAnalysis:
    
    def __init__(self, simulation : Simulation, variableName):
        
        self.simulation = simulation
        
        self.variableName = variableName
        
        self.filteredVariableName = None
        
        self.filteredPackedVariableName = None
        
        self.sizeBinName = None

        self.sizeBinNameGroupedByBins = None

    def getFilteredVariableName(self):
        return self.filteredVariableName
    
    def getFilteredPackedVariableName(self):
        return self.filteredPackedVariableName
    
    def getSizeBinNameGroupedByBins(self):
        return self.sizeBinNameGroupedByBins
    
    
    def getFilteredCoordName(self):
        return self.sizeBinName
    
    def packFilteredPSVariablewithSizeBinCoords(self, packing):
        ps = self.simulation.getPSDataset()
        
        bins =  Data.getBinLimitsWithPackingStartingWithLastOnes( ps[self.sizeBinName].values, packing)
        
        self.filteredPackedVariableName = self.filteredVariableName + "_packed"
        
        self.sizeBinNameGroupedByBins = self.sizeBinName + "_bins"
        
        ps[self.filteredPackedVariableName] =  ps[self.filteredVariableName].groupby_bins( self.sizeBinName, bins).sum()
    
        
    def renamePSCoordSizeBinA(self):
        self.__renamePSCoordSizeBin(["aea", "cla", "ica"], "SizeBinA" )
    
    def renamePSCoordSizeBinB(self):
        self.__renamePSCoordSizeBin(["aeb", "clb", "icb"], "SizeBinB" )
        
    def __renamePSCoordSizeBin(self, coordList, newName):
        ps = self.simulation.getPSDataset()
        data = ps[self.filteredVariableName]
        
        oldName = None
        for k in coordList:
            if k in data.coords:
                oldName = k
                break
            else:
                continue
        
        if oldName is not None:
            self.sizeBinName = newName
            ps[self.filteredVariableName] = data.rename( {oldName:self.sizeBinName})
        else:
            sys.exit("renamePSVariableSizeBinBCoord", self, "old coordinate is not suitable for", self.sizeBinName)
            
    
    def __getFilteredStatus(self):
        if self.filteredVariableName is None:
            return False
        else:
            return True
          
    
    def filterPSVariableAboveCloud(self ):
        
        if self.__getFilteredStatus():
            print("Already filtered the desired variable")
            return
        else:
            self.filteredVariableName = self.variableName + "_filteredByAboveCloud"
        
        ps = self.simulation.getPSDataset()
        ts = self.simulation.getTSDataset()
        
        ps[self.filteredVariableName] = ps[self.variableName].where(ps["zt"] > ts["zc"], drop = True).mean(dim = "zt", skipna = True)
        
    
    def filterPSVariableInCloud(self, limit = 1e-6 ):
        
        if self.__getFilteredStatus():
            print("Already filtered the desired variable")
            return
        else:
            self.filteredVariableName = self.variableName +"_filteredByInCloud"
        
        ps = self.simulation.getPSDataset()
        
        ps[self.filteredVariableName] = ps[self.variableName].where( (ps["P_rl"] > limit) & (ps["P_ri"] > limit), drop = True).mean(dim = "zt", skipna = True)
        
    
    def filterPSVariableBelowCloud(self, limit = 1e-6 ):
        
        if self.__getFilteredStatus():
            print("Already filtered the desired variable")
            return
        else:
            self.filteredVariableName = self.variableName + "_filteredByBelowCloud"
        
        
        ps = self.simulation.getPSDataset()
        ts = self.simulation.getTSDataset()
        
        ps[self.filteredVariableName] = ps[self.variableName].where(ps["P_rl"] < limit, drop = True).where(ps["zt"] < ts["zb"], drop = True).mean(dim = "zt", skipna = True) 
        
    def filterPSVariableAtHeight(self, height):
        
        if self.__getFilteredStatus():
            print("Already filtered the desired variable")
            return
        else:
            self.filteredVariableName = self.variableName + "_filteredByAtHeight"
        
        ps = self.simulation.getPSDataset()
        
        ps[self.filteredVariableName] = ps[self.variableName].sel(zt = height, method = 'nearest')
    
                
            
            