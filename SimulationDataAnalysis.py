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

class SimulationDataAnalysis:
    
    def __init__(self, simulation : Simulation, limit = 1e-6):
        
        self.simulation = simulation
        
        self.limit = limit
        
        self.sizeBinNameA = "SizeBinA"
        self.sizeBinNameB = "SizeBinB"
        
    def renamePSVariableCoordSizeBinA(self, variable ):
        data = self.simulation.getPSDataset()[variable]
        
        oldName = None
        for k in ["aea", "cla", "ica"]:
            if k in data.coords:
                oldName = k
                break
            else:
                continue
        
        if oldName is None:
            sys.exit("renamePSVariableSizeBinBCoord", variable, self, "old coordinate is not suitable for SizeBinA")
        else:
            data = data.rename({oldName:self.sizeBinNameA})      
            
    def renamePSVariableCoordSizeBinB(self, variable ):
        data = self.simulation.getPSDataset()[variable]
        
        oldName = None
        for k in ["aeb", "clb", "icb"]:
            if k in data.coords:
                oldName = k
                break
            else:
                continue
        
        if oldName is None:
            sys.exit("renamePSVariableSizeBinBCoord", variable, self, "old coordinate is not suitable for SizeBinB")
        else:
            data = data.rename({oldName:self.sizeBinNameB})

          
    
    def filterPSVariableAboveCloud(self, variable ):
        ps = self.simulation.getPSDataset()
        ts = self.simulation.getTSDataset()
        
        filteredVariableName = variable + "_filteredByAboveCloud"
        
        ps[filteredVariableName] = ps[variable].where(ps["zt"] > ts["zc"], drop = True).mean(dim = "zt", skipna = True)
        
        return filteredVariableName
    
    def filterPSVariableInCloud(self, variable ):
        ps = self.simulation.getPSDataset()
        
        filteredVariableName = variable + "_filteredByInCloud"
        ps[filteredVariableName] = ps[variable].where( (ps["P_rl"] > self.limit) & (ps["P_ri"] > self.limit), drop = True).mean(dim = "zt", skipna = True)
        
        return filteredVariableName
    
    def filterPSVariableBelowCloud(self, variable ):
        ps = self.simulation.getPSDataset()
        ts = self.simulation.getTSDataset()
        
        filteredVariableName = variable + "_filteredByBelowCloud"
        
        ps[filteredVariableName] = ps[variable].where(ps["P_rl"] < self.limit, drop = True).where(ps["zt"] < ts["zb"], drop = True).mean(dim = "zt", skipna = True) 
        
        return filteredVariableName
        
    def filterPSVariableAtHeight(self, variable, height):
        ps = self.simulation.getPSDataset()
        
        filteredVariableName = variable + "_filteredByAtHeight"
        
        ps[variable] = ps[variable].sel(zt = height, method = 'nearest')
        
        return filteredVariableName
    
        
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
        #TÄSSÄ OLLAAN
        newname = "dryRadiusBinB"
        aero = aero.rename({"aeb":newname})
        cloud = cloud.rename({"clb":newname})
        ice   = ice.rename({"icb":newname})
        
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
            