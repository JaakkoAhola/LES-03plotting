#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:14:55 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import numpy
import pathlib
import xarray
from Data import Data

class Simulation:
    
    def __init__(self, folder, label, color, linewidth = None, zorder = 1):
        self.folder = pathlib.Path(folder)
        self.label = label
        self.color = color
        self.nc = None
        self.ps = None
        self.ts = None
        self.linewidth = linewidth
        
        self.__ncHours = False
        self.__psHours = False
        self.__tsHours = False
        
        self.zorder = zorder
        
        self.AUXDatasets = {}
        self.__AuxHours = False
        
    def getColor(self):
        return self.color
    
    def getLabel(self):
        return self.label
    
    def getLineWidth(self):
        return self.linewidth
    
    def getZorder(self):
        return self.zorder
    
    def getFolder(self):
        return self.folder
        
    def getNCDataset(self):
        if self.nc is None:
            self.nc = self._getDataset("nc")
                
        return self.nc
    
    def getPSDataset(self):
        if self.ps is None:
            self.ps = self._getDataset("ps")
        
        return self.ps
    
    def getTSDataset(self):
        if self.ts is None:
            self.ts = self._getDataset("ts")
        
        
        return self.ts
    
    def setAUXDataset(self, key, filename):
        
        self.AUXDatasets[key] = xarray.open_dataset( self.folder / filename )
    
    def updateAUXDataset(self, key, dataset):
        self.AUXDatasets[key] = dataset
    
    def getAUXDataset(self, key):
        return self.AUXDatasets[key]
        
    
    def _getDataset(self, ncMode):
    
        if "." not in ncMode:
            ncModeSuffix = "." + ncMode
        
        fileAbs = None
        for ncFile in list(self.folder.glob("*.nc")):
            if ncMode != "":
                if ncModeSuffix in ncFile.suffixes:
                    fileAbs = ncFile
            else:
                if ".ps" not in ncFile.suffixes and ".ts" not in ncFile.suffixes:
                    fileAbs = ncFile
        if fileAbs is not None:
            dataset = xarray.open_dataset(fileAbs)
        else:
            raise FileNotFoundError(ncMode, "file not found from", self.folder)
        
        return dataset
    
    def setNCDataset(self, nc):
        self.nc = nc
    
    def setTSDataset(self, ts):
        self.ts = ts
    
    def setPSDataset(self,ps):
        self.ps = ps
    
    def setZorder(self, zorder):
        self.zorder = zorder
        
    def sliceByTimeNCDataset(self,timeStart, timeEnd):
        
        self.nc = self.__sliceByTimeDataset( self.getNCDataset(), timeStart, timeEnd)
        
    def sliceByTimePSDataset(self,timeStart, timeEnd):
        
        self.ps = self.__sliceByTimeDataset(self.getPSDataset(),timeStart, timeEnd)
        
    def sliceByTimeTSDataset(self,timeStart, timeEnd):
        
        self.ts = self.__sliceByTimeDataset(self.getPSDataset(), timeStart, timeEnd)    
    
    def sliceByTimeAUXDataset(self, timeStart, timeEnd):
        for key in self.AUXDatasets:
            self.AUXDatasets[key] = self.__sliceByTimeDataset(self.AUXDatasets[key], timeStart, timeEnd)
        
    
    def __sliceByTimeDataset(self, dataSet, timeStart, timeEnd):
        timeStartInd = Data.getClosestIndex( dataSet.time.values, timeStart )
        timeEndInd   = Data.getClosestIndex( dataSet.time.values, timeEnd )
        
        return  dataSet.isel(time = slice(timeStartInd,timeEndInd))

    
    # needs revision
    def getEntrainment(self,
                       divergence = 5.e-6):
        ts = self.getTSDataset()
        z = ts.zi1_bar.values
        t = ts.time.values
        dzdt = numpy.diff(z) / numpy.diff(t)
        we = xarray.DataArray( dzdt + divergence*z[1:], dims={"h":ts.time.values[1:]/3600}, coords = {"time":ts.time.values[1:]/3600}, attrs={"longname":"Entrainment velocity", "units":"m/s"})
        return we
    
    ####
    #### need revision
    ####
    def getNormalisedHeight(h, cloudbase, cloudtop):
        x_incloud = [cloudbase,cloudtop]
        y_incloud = [0,1]
        z_incloud = numpy.polyfit(x_incloud,y_incloud,1)
    
        x_belowcloud = [0,cloudbase]
        y_belowcloud = [-1,0]
        z_belowcloud = numpy.polyfit(x_belowcloud,y_belowcloud,1)
        
        if h<cloudbase:
            rr = numpy.poly1d(z_belowcloud)(h)
        else:
            rr = numpy.poly1d(z_incloud)(h)
        return rr

    
    def setUnitToLatexMathMode(dataset):
        dataset.attrs["units"] = r'$' + dataset.attrs["units"] + '$'
        return dataset
    
    def setTimeCoordToHours(self):
        if self.nc is not None and (not self.__ncHours):
            self.nc = self.nc.assign_coords(time = (self.nc.time / 3600))
            self.__ncHours = True
        if self.ps is not None and (not self.__psHours):
            self.ps = self.ps.assign_coords(time = (self.ps.time / 3600))
            self.__psHours = True
        if self.ts is not None and (not self.__tsHours):
            self.ts = self.ts.assign_coords(time = (self.ts.time / 3600))
            self.__tsHours = True
        if bool(self.AUXDatasets) and (not self.__AuxHours):
            for key in self.AUXDatasets:
                self.AUXDatasets[key] = self.AUXDatasets[key].assign_coords(time = (self.AUXDatasets[key].time / 3600))
                self.__AuxHours = True
    
    def setLineWidth(self, linewidth):
        self.linewidth = linewidth
        
    def setColor(self, color):
        self.color = color