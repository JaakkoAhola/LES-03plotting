#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 13:30:13 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import matplotlib
import numpy
import time

from Data import Data

class PlotTweak:
  
    
    def setXticks(ax, ticks = None, start = 0, end = 8, interval = 0.5, integer = True):
        if ticks is None:
            if integer:
                ticks = Data.getIntergerList( start, end, interval)
            else:
                ticks = Data.getFloatList(start, end, interval)
            
        PlotTweak._setTicks(ax.set_xticks, ticks)
        return ticks
    
    def setYticks(ax, ticks = None, start = 0, end = 1000, interval = 50, integer = True):
        if ticks is None:
            if integer:
                ticks = Data.getIntergerList( start, end, interval)
            else:
                ticks = Data.getFloatList(start, end, interval)
            
        
        PlotTweak._setTicks(ax.set_yticks, ticks)
        
        return ticks
    
    
    def _setTicks(axset, ticks):
        """
        axset  is in [ax.set_xticks, ax.set_yticks, ]
        """
        axset(ticks)
        return ticks
    
    
    def setXLabels(ax, ticks, shownLabels = None, start = 0, end = 8, interval = 2, integer = True):
        shownLabelsBoolean = PlotTweak._setLabels( ax.set_xticklabels, ax.xaxis, ticks, shownLabels, start, end, interval)
        return shownLabelsBoolean
    
    def setYLabels(ax, ticks, shownLabels = None, start = 0, end = 8, interval = 2, integer = True):
        shownLabelsBoolean = PlotTweak._setLabels( ax.set_yticklabels, ax.yaxis, ticks, shownLabels, start, end, interval)
        return shownLabelsBoolean
    
    def _setLabels(axset, ax_axis, ticks, shownLabels = None, start = 0, end = 8, interval = 2, integer = False):
        
        axset(ticks)
        
        if shownLabels is None:
            if integer:
                shownLabels = Data.getIntergerList( start, end, interval )
            else:
                shownLabels = Data.getFloatList(start, end, interval)
        
        shownLabelsBoolean = Data.getMaskedList(ticks, shownLabels)
        
        PlotTweak.hideLabels(ax_axis, shownLabelsBoolean)
        
        return shownLabelsBoolean
        
    
    def hideLabels(ax_axis, shownLabelsBoolean):
        """
        ax_axis is eithery ax.yaxis or colorbar.ax.xaxis or colorbar.ax.yaxis
        """
        k = 0
        for label in ax_axis.get_ticklabels():
            label.set_visible(shownLabelsBoolean[k])
            k = k + 1
    
    def hideXTickLabels(ax):
        PlotTweak._hideAllTickLabels(ax.get_xticklabels)
    def hideYTickLabels(ax):
        PlotTweak._hideAllTickLabels(ax.get_yticklabels)
    def _hideAllTickLabels(axTicksGetter):
        matplotlib.pyplot.setp(axTicksGetter()[:], visible=False)
    
    def setXTickSizes(ax, labelListMajorLineBoolean,
                  majorFontsize = 7,
                  minorFontSize = 4):
        
        PlotTweak._setTickSizes(ax.xaxis, labelListMajorLineBoolean, majorFontsize, minorFontSize)
    
    def setYTickSizes(ax, labelListMajorLineBoolean,
                  majorFontsize = 7,
                  minorFontSize = 4):
        
        PlotTweak._setTickSizes(ax.yaxis, labelListMajorLineBoolean, majorFontsize, minorFontSize)
    
    def _setTickSizes(ax_axis, labelListMajorLineBoolean,
                  majorFontsize,
                  minorFontSize):
        """
        # ax_axis is eithery ax.yaxis or colorbar.ax.xaxis or colorbar.ax.yaxis
        """
        k = 0
        for line in ax_axis.get_ticklines()[0::2]:
            if labelListMajorLineBoolean[k]:
                line.set_markersize( majorFontsize )
            else:
                line.set_markersize(minorFontSize)
            k= k + 1

    def getUnitLabel(label, unit, useBold = True):
        if useBold:
            boldingStart = "\mathbf{"
            boldingEnd  = "}"
        else:
            boldingStart = ""
            boldingEnd   = ""
        
        return r"$" +boldingStart +  "{" + label +  "}{\ } ( " + unit +      ")" + boldingEnd + "$"
    
    def getLatexLabel(label, useBold = True):
        if useBold:
            boldingStart = "\mathbf{"
            boldingEnd  = "}"
        else:
            boldingStart = ""
            boldingEnd   = ""
        
        return r"$" +boldingStart +  "{" + label +  "}{\ }" +  boldingEnd + "$"
    
    def getMathLabel(label):
        
        
        mathlabel = PlotTweak.getMathLabelFromDict(label)
        if "{" in mathlabel:
            mathlabel = PlotTweak.getLatexLabel(mathlabel)
        return mathlabel
    
    def getMathLabelTableFormat(label):
        return "$" + PlotTweak.getMathLabelFromDict(label) + "$"
    
    def getMathLabelFromDict(label):
        dictionary = {"q_inv":"\Delta q_{L}",
                      "tpot_inv":r"\Delta  {\theta}_{L}",
                      "tpot_pbl":r"{\theta}_{L}"                              ,
                      "pblh":"H_{PBL}",
                      "lwp": "LWP",
                      "cdnc": "cdnc",
                      "cos_mu": r"{\cos\mu}",
                      "ks": "N_{Ait}",
                      "as":"N_{acc}",
                      "cs":"N_{coa}",
                      "rdry_AS_eff":"r_{eff}",
                      "w2pos_linearFit": "w_{lin.fit}"}
        return dictionary[label]
    
    def getMathLabelSubscript(label):
        
        try:
            subscript = PlotTweak.getMathLabelFromDict(label).split("_")[1].replace("{","").replace("}", "")
        except IndexError:
            subscript = ""    
            
        return subscript
    
    def getLabelColor(label):
        dictionary = {"q_inv":"#42d4f4",
                      "tpot_inv":"#f58231",
                      "tpot_pbl":"#e6194B",
                      "pblh":"#9A6324",
                      "lwp": "#4363d8",
                      "cdnc": "#3cb44b",
                      "cos_mu": "#ffe119",
                      "ks": "#911eb4",
                      "as":"#f032e6",
                      "cs":"#dcbeff",
                      "rdry_AS_eff":"#fabed4",
                      "w2pos_linearFit": "#469990"}
        
        return dictionary[label]
    
    def getVariableUnit(label):
        aerosolConcentration = "mg^{-1}" #"10^{6}\ kg^{-1}"
        
        dictionary = {"q_inv":"g\ kg^{-1}",
                      "tpot_inv":"K",
                      "tpot_pbl":"K",
                      "pblh":"hPa",
                      "lwp": "g\ m^{-2}",
                      "cdnc": aerosolConcentration,
                      "cos_mu": "",
                      "ks": aerosolConcentration,
                      "as":aerosolConcentration,
                      "cs":aerosolConcentration,
                      "rdry_AS_eff":"nm",
                      "w2pos_linearFit": "",
                      "rainProduction": "mg\ m^2 s^{-1}",
                      "wpos":"m\ s^{-1}"}
        
        return dictionary[label]
    
    def setXaxisLabel(ax, label, unit = None, useBold = True):
        PlotTweak._setLabel(ax.set_xlabel, label, unit, useBold)
    
    def setYaxisLabel(ax, label, unit = None, useBold = True):
        PlotTweak._setLabel(ax.set_ylabel, label, unit, useBold)
    
    def _setLabel(labelPointer, label, unit, useBold):
        if unit is not None:
            label = PlotTweak.getUnitLabel(label, unit, useBold)
            
        labelPointer(label)
    
    def getLogaritmicTicks(tstart, tend, includeFives = False):
#        tstart = -17
#        tend = -9
        logaritmicTicks = numpy.arange(tstart, tend)
        if includeFives:
            fives = numpy.arange(tstart+numpy.log10(5), tend)
            logaritmicTicks = numpy.sort(numpy.concatenate((logaritmicTicks,fives)))
        
        return logaritmicTicks


    def getXPosition(ax, xFrac):
        xmin = ax.get_xlim()[0]
        xmax = ax.get_xlim()[1]
        
        xPos = xFrac*(xmax-xmin) + xmin
        
        return xPos
    
    def getYPosition(ax, yFrac):
        ymin = ax.get_ylim()[0]
        ymax = ax.get_ylim()[1]
        
    
        yPos = yFrac*(ymax-ymin) + ymin
        
        return yPos
    
    def setXLim(ax, start = 0, end = 1):
        ax.set_xlim( start ,end )

    def setYLim(ax, start = 0, end = 1):
        ax.set_ylim( start ,end )        

    def setAnnotation(ax,
                      text,
                      fontsize = 8,
                      xPosition = 0, yPosition = 0,
                      xycoords = 'data',
                      bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="0.5", alpha=0.9)):
        ax.annotate( text, xy=(xPosition, yPosition), size=fontsize, bbox = bbox_props, xycoords = xycoords)

    def setTightLayot(fig):
        fig.tight_layout()
        
    def setAxesOff(ax):
        ax.axis('off')
        
    def getPatches(collectionOfLabelsColors):
        legend_elements = []
        for label, color in collectionOfLabelsColors.items():
            legend_elements.append( matplotlib.patches.Patch( label=label,
                                                              facecolor=color))
        return legend_elements
    
    def useLegend(ax = None, loc = "best"):
        if ax is None:
            matplotlib.pyplot.legend(loc = loc)
        else:
            ax.legend(loc = loc)    
    def setLegendSimulation(ax, simulationList, loc = "center"):
        collectionOfLabelsColors = {}
        for simulation in simulationList:
            collectionOfLabelsColors[ simulation.getLabel() ] =  simulation.getColor()
            
            
        PlotTweak.setLegend(ax, collectionOfLabelsColors, loc )
        
    def setLegend(ax,
                  collectionOfLabelsColors,
                  loc = "center", fontsize = None):
        legend_elements = []
        for label, color in collectionOfLabelsColors.items():
            legend_elements.append( matplotlib.patches.Patch( label=label,
                                                              facecolor=color))

        ax.legend( handles=legend_elements, loc=loc, frameon = True, framealpha = 1.0, fontsize = fontsize )
    
    def setArtist(ax,
                  collectionOfLabelsColors,
                  loc = "center", fontsize = None, ncol = 1, framealpha = 1.0 ):
        legend_elements = []
        for label, color in collectionOfLabelsColors.items():
            legend_elements.append( matplotlib.patches.Patch( label=label,
                                                              facecolor=color))

        artist = ax.legend( handles=legend_elements, loc=loc, frameon = True, framealpha = framealpha, fontsize = fontsize, ncol = ncol )
        
        ax.add_artist(artist)
        
        

def main():
   pass
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
