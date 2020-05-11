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
        
        self.filteredPackedVariableName = self.filteredVariableName + "_bins"
        
        self.sizeBinNameGroupedByBins = self.sizeBinName + "_bins"
        
        ps[self.filteredPackedVariableName] =  ps[self.filteredVariableName].groupby_bins( self.sizeBinName, bins).sum()
    
        
    def renamePSCoordSizeBinA(self):
        data = self.simulation.getPSDataset()
        
        oldName = None
        for k in ["aea", "cla", "ica"]:
            if k in data[self.variableName].coords:
                oldName = k
                break
            else:
                continue
        
        if oldName is not None:
            self.sizeBinName = "SizeBinA"
            self.simulation.setPSDataset( data.rename( {oldName:self.sizeBinName}) )
        else:
            sys.exit("renamePSVariableSizeBinBCoord", self, "old coordinate is not suitable for SizeBinA")
            
    def renamePSCoordSizeBinB(self):
        data = self.simulation.getPSDataset()
        
        oldName = None
        for k in ["aeb", "clb", "icb"]:
            if k in data[self.variableName].coords:
                oldName = k
                break
            else:
                continue
        
        if oldName is not None:
            self.sizeBinName = "SizeBinB"
            self.simulation.setPSDataset( data.rename( {oldName:self.sizeBinName}) )
        else:
            sys.exit("renamePSVariableSizeBinBCoord", self, "old coordinate is not suitable for SizeBinB")
            
    
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
    
        
        
    def getTimeseriesOfProportions( simulation : Simulation,
                                   mode = "inCloud", limit = 1e-6, height = None, packing = None):
                
        ps = simulation.getPSDataset()
        if ps is None:
            return "FileNotFound"
        
        ts = simulation.getTSDataset()
        if ts is None:
            return "FileNotFound"
        
        try:
            if mode == "inCloud":
                ps = ps.where( (ps.P_rl > limit) & (ps.P_ri > limit), drop = True).mean(dim = "zt", skipna = True)
            elif mode == "belowCloud":
                ps = ps.where(ps.P_rl < limit, drop = True).where(ps.zt < ts.zb, drop = True).mean(dim = "zt", skipna = True) 
            elif mode == "aboveCloud":
                ps = ps.where(ps.zt > ts.zc, drop = True).mean(dim = "zt", skipna = True)
            elif mode == "height":
                ps = ps.sel(zt = height, method = 'nearest')        
        except KeyError:
            return
        
        try:
            aero  = ps["P_Nabb"]
            cloud = ps["P_Ncbb"]
            ice   = ps["P_Nibb"]
        except KeyError:
            return
        
        newname = "dryRadiusBinB"
        aero = aero.rename({"aeb":newname})
        cloud = cloud.rename({"clb":newname})
        ice   = ice.rename({"icb":newname})
        
        #TÄSSÄ OLLAAN REFACTORINGISSA
        total = aero + cloud + ice
        
        if packing is not None:
            for daatta in aero, cloud, ice, total:
                daatta[:,packing] = numpy.sum(daatta[:,packing:], axis = 1)
        
        binNumber = min( numpy.shape(total.values)[1], packing +1 )
        
        for bini in range(binNumber):
            aeroBin = aero[:,bini]
            cloudBin = cloud[:,bini]
            iceBin  = ice[:,bini]
            
            totalBin = total[:,bini]
            
            aeroFrac = aeroBin/totalBin
            cloudFrac = cloudBin/totalBin
            iceFrac = iceBin/totalBin
            
            totalBinRelative  = totalBin / totalBin.values[0]
            
            
            if packing is not None and bini == (binNumber - 1):
                bininame = str(bini + 1 ) + " - 7"
            else:
                bininame = str(bini +1)
            