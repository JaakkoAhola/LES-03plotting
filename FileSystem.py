#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:22:16 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import pathlib
import yaml

class FileSystem:
    def createSubfolder(rootfolderName, subfolderName):
        subfolder = pathlib.Path(rootfolderName) / subfolderName
        subfolder.mkdir( parents=True, exist_ok = True )
        
        return subfolder
    
    def makeFolder(folder):
        """
        Parameters
        ----------
        folder :  : pathlib.Path
            
        
        creates folder and its parents

        Returns
        -------
        None.

        """
        folder.mkdir( parents=True, exist_ok = True )
    
    def readYAML(absoluteFilePath):
        with open(absoluteFilePath, "r") as stream:
            try:
                output = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return output
    
    def writeYAML(absoluteFilePath, data):
        with open(absoluteFilePath, "w") as stream:
            try:
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                print(exc)
            
    
    def getAbsoluteFilename(folder, file):
        return pathlib.Path(folder) / file
