#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:16:21 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import matplotlib
import numpy
import pathlib
import seaborn
import sys

class Figure:
    
    def __init__(self, figurefolder, name,
                 nrows = 1, ncols =1, sharex=False, sharey=False, style = "seaborn-paper",
                 figsize = None,width = None,
                 wspace=0.3, hspace=0.12, 
                 top = 0.985, left = 0.12, right=0.97, bottom = 0.1
                 ):
        
        self._setContext(style)
        
        self.figurefolder = pathlib.Path(figurefolder)
        self.name = name
        self.absoluteName = self.figurefolder / name
        
        
        aspectRatio = 1.5
        inchInCM = 2.54
        if figsize is None:
            if width is None:
                width = 12/inchInCM
            self.figsize = [width, width*nrows/ncols/aspectRatio]
        else:
            self.figsize = figsize
        
        
        self.fig = matplotlib.pyplot.figure(figsize=self.figsize, constrained_layout=False)
        self.grid = matplotlib.gridspec.GridSpec(nrows, ncols,
                                            wspace=wspace, hspace=hspace, 
                                            top = top, left = left, right = right, bottom = bottom)
        
        self.coords = numpy.arange(ncols*nrows).reshape(nrows,ncols)
        
        self.axesList = []
        
        for yCoord in range(nrows):
            for xCoord in range(ncols):
                self.axesList.append(matplotlib.pyplot.subplot( self.grid[yCoord,xCoord] ))
        
        self.oldContextValues = {}
    
    def getFig(self):
        return self.fig
    
  
    def getAxes(self, ind=0):
        
        # coordIndexes = numpy.where(self.coords==ind)
        
        # yCoord = coordIndexes[0].item()
        # xCoord = coordIndexes[1].item()
        
        return self.axesList[ind] #matplotlib.pyplot.subplot( self.grid[yCoord,xCoord] )
        
    def getFigSize(self):
        return self.figsize
    
    def getOldContextValues(self):
        return self.oldContextValues

    def modifyContext(self, parameter, factorForOldValue = None, newValue = None):
        self.oldContextValues[ parameter ] = matplotlib.rcParams[parameter]
        
        if factorForOldValue is not None:
            matplotlib.rcParams[ parameter ] = Figure._modifyContextFactor(parameter, factorForOldValue)
        elif newValue is not None:
            matplotlib.rcParams[ parameter ] = newValue
            

    def _modifyContextFactor(parameter, factorForOldValue ):
        if isinstance(matplotlib.rcParams[parameter], int):
            newValue = matplotlib.rcParams[parameter] * factorForOldValue
            
        elif isinstance(matplotlib.rcParams[parameter], list):
            newValue = list(numpy.asarray(matplotlib.rcParams[parameter])*factorForOldValue)
            
        return newValue

    def _setContext(self, style = "seaborn-paper", printing = False):
        matplotlib.rcParams.update(matplotlib.rcParamsDefault)
        matplotlib.pyplot.style.use(style)
#        seaborn.set_context("poster")
#        matplotlib.rcParams['figure.figsize'] = list(numpy.asarray(matplotlib.rcParams["figure.figsize"])*2)
#        if printing: print('figure.figsize', matplotlib.rcParams['figure.figsize'])
#    
#        if printing: print('figure.dpi', matplotlib.rcParams['figure.dpi'])
        matplotlib.rcParams['savefig.dpi'] = 900
#        if printing: print('savefig.dpi', matplotlib.rcParams['savefig.dpi'])
#        matplotlib.rcParams['legend.fontsize'] = 14
#        if printing: print('legend.fontsize', matplotlib.rcParams['legend.fontsize'])
#        matplotlib.rcParams['axes.titlesize'] = 42
#        matplotlib.rcParams['axes.labelsize'] = 42
#        matplotlib.rcParams['xtick.labelsize'] = 42 #22
#        matplotlib.rcParams['ytick.labelsize'] = 42 #22
        matplotlib.rcParams['font.weight']= 'bold' #this should be changed
#        if printing: print('axes.titlesize', matplotlib.rcParams['axes.titlesize'])
#        if printing: print('axes.labelsize', matplotlib.rcParams['axes.labelsize'])
#        if printing: print('xtick.labelsize', matplotlib.rcParams['xtick.labelsize'])
#        if printing: print('ytick.labelsize', matplotlib.rcParams['ytick.labelsize'])
#        if printing: print("lines.linewidth", matplotlib.rcParams['lines.linewidth'])
#        matplotlib.rcParams['text.latex.unicode'] = False
#        matplotlib.rcParams['text.usetex'] = False
#        if printing: print("text.latex.unicode", matplotlib.rcParams['text.latex.unicode'])
#        matplotlib.rcParams['text.latex.preamble']=[r'\usepackage{amsmath}']
        matplotlib.rc('text', usetex = False)
    
    def setAdjusting(self, hspace = 0.05, wspace = 0.05, left = None, right = None, top = None, bottom = None):
        self.fig.subplots_adjust( hspace=hspace, wspace = wspace, left = left, right = right, top = top, bottom = bottom)
        
    #, padding = 0.06, bbox_inches = "tight"
    def save(self, file_extension = ".pdf", useTight = True, close = True):
            
        #self.fig.savefig( self.absoluteName.with_suffix( file_extension ), pad_inches = padding, bbox_inches = bbox_inches )
        self.fig.savefig( self.absoluteName.with_suffix( file_extension ))
        
        if close:
            matplotlib.pyplot.close()
