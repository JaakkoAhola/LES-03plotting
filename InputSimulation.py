#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:28:17 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import numpy
import pandas
import pathlib
import sys

from FileSystem import FileSystem
from Simulation import Simulation

class InputSimulation:
    
    def __init__(self,
        idCollection = None, #either list or YAML file
        folderCollection = None, #either list or YAML file
        labelCollection = None, #either list or YAML file
        colorSet = None, #either list or YAML file or dictionary with "label" : "color" format
        folder = None):
        
        self.idCollection     = InputSimulation.__setupCollection(self, folder, idCollection)
        self.folderCollection = InputSimulation.__setupCollection(self,folder, folderCollection)
        self.labelCollection  = InputSimulation.__setupCollection(self,folder, labelCollection)
        self.colorCollection  = InputSimulation.__setupCollection(self,folder, colorSet)
        
        self.simulationDataFrame = InputSimulation.__initSimulationDataFrame(self)
        
    def __setupCollection(self, folder, collectionVar):
        
        if isinstance(collectionVar, str):
            if folder is not None:
                absoluteFileOfPath = FileSystem.getAbsoluteFilename(folder,collectionVar)
            else:
                absoluteFileOfPath = collectionVar
                
            collection = FileSystem.readYAML( absoluteFileOfPath )
            
        elif isinstance(collectionVar, list):
            collection = collectionVar
        elif isinstance(collectionVar, dict):
            collection = InputSimulation.__createSimulationColorCollection( self.labelCollection, collectionVar)
        else:
            collection = None
        
        return collection
    
    def __createSimulationColorCollection( labelCollection, colorCollection ):
        
        simulationColorCollection = [ colorCollection[label]   for ind,label in enumerate(labelCollection) ]
        
        return simulationColorCollection

    
    def __initSimulationDataFrame(self):
        checkType, checkLength = InputSimulation.__checkObj(self)
        
        if checkType and checkLength:
        
            self.simulationDataFrame = pandas.DataFrame( data = numpy.asarray([
                                                                    self.idCollection,
                                                                    self.labelCollection,
                                                                    self.colorCollection,
                                                                    self.folderCollection ]).T,
                                      index = self.idCollection,
                                      columns = ["ID", "LABEL", "COLOR", "FOLDER"] )
        else:
            self.simulationDataFrame = None
        
        return self.simulationDataFrame
    
    def getSimulationCollection(simulationDataFrame): #public
        simulationCollection = {}
        
        if not ( simulationDataFrame.index.name == "ID"):
            try:
                simulationDataFrame.set_index("ID", inplace = True)
            except KeyError:
                sys.exit("ID missing from simulationDataFrame")
        for ind in simulationDataFrame.index:
            simulationCollection[ ind ] = Simulation( simulationDataFrame.loc[ind]["FOLDER"],
                                                                                    simulationDataFrame.loc[ind]["LABEL"],
                                                                                    simulationDataFrame.loc[ind]["COLOR"])
        return simulationCollection

    def getSimulationDataFrame(self):
        return self.simulationDataFrame

    def setSimulationDataFrame(self, simulationDataFrame):
        self.simulationDataFrame = simulationDataFrame
    
    def __checkObj(self):
        checkType, checkLength = InputSimulation.__checkLists([self.idCollection, self.folderCollection, self.labelCollection, self.colorCollection])
        
        if not checkType:
            print("Object variable types are not lists")
        elif not checkLength:
            print("Object list lengths are incorrect")
            
        return checkType, checkLength
    
    def __checkLists(arrayOfLists):
        checkType = True
        checkLength = True
        for k in arrayOfLists:
            checkType = (checkType and isinstance(k, list))
        
        for i in range(1,len(arrayOfLists)):
            checkLength = checkLength and (len(arrayOfLists[i-1]) == len(arrayOfLists[i]) )
        
        return checkType, checkLength
    
    def saveDataFrameAsCSV(self, folder, file = None): #public
        if self.simulationDataFrame is None:
            raise Exception("simulationDataFrame is not set. Set proper object variables and run __initSimulationDataFrame()")
        if file is None:
            absFile = folder
        else:
            absFile = pathlib.Path(folder) / file
        absFile.parent.mkdir( parents=True, exist_ok = True )
        self.simulationDataFrame.to_csv(absFile)
        
        return absFile
    
    def getEmulatorFileList(superRootFolder, emulatorSet = None, listOfCases = None):#public
        
        if emulatorSet is not None:
            absolutepath = pathlib.Path(superRootFolder) / emulatorSet
        else:
            absolutepath = pathlib.Path(superRootFolder)
            
            
        if listOfCases is None:
            fileList =  sorted(absolutepath.glob("emul???/"))
        else:
            fileList = []
            for i in listOfCases:
                case = absolutepath / ( "emul" + "{:03d}".format(i))
                
                if case.is_dir():
                    fileList.append(case)
        return fileList
    
    def getEmulatorIDlist(fileList):#public
        idList =  [None] * len(fileList)
        
        for ind,file in enumerate(fileList):
            emulatorSet = file.parts[-2]
            emulatorSetSplit = emulatorSet.split("_")
            lvl = emulatorSetSplit[-2][-1]
            nightTimeDayTime = emulatorSetSplit[-1][0].upper()
            caseNumber = file.parts[-1][4:]
            
            idList[ind] = lvl + nightTimeDayTime + "_" + caseNumber
            
        return list(idList)
    
    def getEmulatorDesignAsDataFrame(folder, identifierPrefix, file = "design.csv"):#public
        absolutePath = pathlib.Path(folder) / file
        
        designDataframe = pandas.read_csv(absolutePath)
        
        idList = ["{0}_{1:03d}".format(identifierPrefix, i) for i in range(1,designDataframe.shape[0]+1)]
        
        designDataframe["ID"] = idList
        designDataframe.set_index("ID")
        del designDataframe["Unnamed: 0"]
        
        return designDataframe
    
    
        
    
