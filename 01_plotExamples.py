#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:50:04 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import matplotlib
import numpy
import pandas
import time

from InputSimulation import InputSimulation
from Figure import Figure
from Plot import Plot
from PlotTweak import PlotTweak

       
def main(simulationDataFrameCSVFile):
    
    simulationDataFrame = pandas.read_csv(simulationDataFrameCSVFile)

    # set simulation data as dictionary
    simulationCollection = InputSimulation.getSimulationCollection( simulationDataFrame )
        
    if False:
        fig1 = Figure("/home/aholaj/Nextcloud/kuvatesti","Prognostic")
        
        cloudTicks = Plot.getTicks(0, 1000, 250)
    
        logaritmicLevels = Plot.getLogaritmicTicks(-17,-9, includeFives = True)
        
        ax, im = Plot.getTimeseriesOfProfile(fig1.getAxes(),
                                    simulationCollection["Prognostic_48h"],
                                    "P_cDUa",
                                    title = "",
                                    yticks = cloudTicks,
                                    timeEndH= 33.05, levels = logaritmicLevels,
                                    useColorBar = False, showXaxisLabels=False, 
                                    showXLabel = False)
        
        fig1.save()
    if False:
        # create figure object
        fig2 = Figure("/home/aholaj/Nextcloud/kuvatesti","LWP")
        # load ts-datasets and change their time coordinates to hours
        for k in ["Prognostic_48h", "ICE4_24h", "Prognostic_2", "Prognostic_Aero", "Prognostic_2_Aero"]:
            simulationCollection[k].getTSDataset()
            simulationCollection[k].setTimeCoordToHours()
        
        # plot timeseries with unit conversion       
        Plot.getTimeseries(fig2.getAxes(),
                           [simulationCollection["Prognostic_48h"], simulationCollection["ICE4_24h"],
                             simulationCollection["Prognostic_Aero"],simulationCollection["Prognostic_2"],
                            simulationCollection["Prognostic_2_Aero"]],
                           "lwp_bar", conversionFactor=1000.)
        end = 32
        # set xticks
        ticks = PlotTweak.setXticks(fig2.getAxes(), end = end, interval = 0.5)
        # set xlabels
        shownLabelsBoolean = PlotTweak.setXLabels(fig2.getAxes(), ticks, end = end, interval = 4)
        # set xtick sizes
        PlotTweak.setXTickSizes(fig2.getAxes(), shownLabelsBoolean, minorFontSize=8)
        # limit x-axes
        PlotTweak.setXLim(fig2.getAxes(), end = end)
        PlotTweak.setYLim(fig2.getAxes(), end = 60)
        # set annotation for figure
        PlotTweak.setAnnotation(fig2.getAxes(), "a) Liquid water path", xPosition=2, yPosition= 30)
        
        Plot.getVerticalLine(fig2.getAxes(), 2)
        # set axes labels
        PlotTweak.setXaxisLabel(fig2.getAxes(),"LWP", "g\ m^{-2}")
        PlotTweak.setYaxisLabel(fig2.getAxes(),"Time", "h")
        PlotTweak.useLegend( fig2.getAxes() )
        PlotTweak.setTightLayot(fig2.getFig())
        
        fig2.save()

    if True:
        # create figure object
        fig2 = Figure("/home/aholaj/Nextcloud/kuvatesti","Nc_ic")
        # load ts-datasets and change their time coordinates to hours
        sensitive = ["ICE0_8h","ICE1_24h","ICE2_24h","ICE3_24h","ICE3_8h","ICE4_24h","ICE5_8h","ICE6_8h", "Prognostic_48h"]
        for k in sensitive:
            simulationCollection[k].getTSDataset()
            simulationCollection[k].setTimeCoordToHours()
        
            # plot timeseries with unit conversion       
            Plot.getTimeseries(fig2.getAxes(),
                           simulationCollection[k],
                           "Nc_ic", conversionFactor=1e-6)
        end = 32
        # set xticks
        ticks = PlotTweak.setXticks(fig2.getAxes(), end = end, interval = 0.5)
        # set xlabels
        shownLabelsBoolean = PlotTweak.setXLabels(fig2.getAxes(), ticks, end = end, interval = 4)
        # set xtick sizes
        PlotTweak.setXTickSizes(fig2.getAxes(), shownLabelsBoolean, minorFontSize=8)
        # limit x-axes
        PlotTweak.setXLim(fig2.getAxes(), end = end)
        #PlotTweak.setYLim(fig2.getAxes(), end = 60)
        # set annotation for figure
        PlotTweak.setAnnotation(fig2.getAxes(), "a) Nc_ic", xPosition=2, yPosition= 155)
        
        Plot.getVerticalLine(fig2.getAxes(), 2)
        # set axes labels
        PlotTweak.setYaxisLabel(fig2.getAxes(),"In-cloud\ CDNC", "mg^{-1}")
        PlotTweak.setXaxisLabel(fig2.getAxes(),"Time", "h")
        PlotTweak.useLegend( fig2.getAxes() )
        PlotTweak.setTightLayot(fig2.getFig())
        
        fig2.save(file_extension=".png")    
    if True:
        # create figure object
        fig3 = Figure("/home/aholaj/Nextcloud/kuvatesti","IWP")
        # load ts-datasets and change their time coordinates to hours
        for k in ["Prognostic_48h", "ICE4_24h", "Prognostic_2", "Prognostic_Aero", "Prognostic_2_Aero"]:
            simulationCollection[k].getTSDataset()
            #simulationCollection[k].setTimeCoordToHours()
        
        # plot timeseries with unit conversion       
        Plot.getTimeseries(fig3.getAxes(),
                           [simulationCollection["Prognostic_48h"], simulationCollection["ICE4_24h"],
                             simulationCollection["Prognostic_Aero"],simulationCollection["Prognostic_2"],
                            simulationCollection["Prognostic_2_Aero"]],
                           "iwp_bar", conversionFactor=1000.)
        end = 32
        # set xticks
        ticks = PlotTweak.setXticks(fig3.getAxes(), end = end, interval = 0.5)
        # set xlabels
        shownLabelsBoolean = PlotTweak.setXLabels(fig3.getAxes(), ticks, end = end, interval = 4)
        # set xtick sizes
        PlotTweak.setXTickSizes(fig3.getAxes(), shownLabelsBoolean, minorFontSize=8)
        # limit x-axes
        PlotTweak.setXLim(fig3.getAxes(), end = end)
        PlotTweak.setYLim(fig3.getAxes(), end = 60)
        # set annotation for figure
        PlotTweak.setAnnotation(fig3.getAxes(), "b) Ice water path", xPosition=2, yPosition= 30)
        
        Plot.getVerticalLine(fig3.getAxes(), 2)
        # set axes labels
        PlotTweak.setXaxisLabel(fig3.getAxes(),"IWP", "g\ m^{-2}")
        PlotTweak.setYaxisLabel(fig3.getAxes(),"Time", "h")
        PlotTweak.useLegend( fig3.getAxes() )
        PlotTweak.setTightLayot(fig3.getFig())
        
        fig3.save()        
    
    if False:
        # create figure object
        fig2 = Figure("/home/aholaj/Nextcloud/kuvatesti","fourWinds", ncols=2, nrows=2, style ="seaborn-paper")
        # load ts-datasets and change their time coordinates to hours
        for k in ["ICE0_8h", "ICE1_8h"]:
            simulationCollection[k].getTSDataset()
            simulationCollection[k].getPSDataset()
            simulationCollection[k].setTimeCoordToHours()
        
        # plot timeseries with unit conversion       
        Plot.getTimeseries(fig2.getAxes()[0,0],
                           simulationCollection["ICE0_8h"],
                           "lwp_bar", conversionFactor=1000.)
        Plot.getVerticalLine(fig2.getAxes()[0,0], 2)
        
        if True:
            PlotTweak.setSuperWrapper(fig2.getAxes()[0,0],
                                  xstart = 0,
                                  xend = 8,
                                  xtickinterval = 0.5,
                                  xlabelinterval = 2,
                                  xticks = None,
                                  xShownLabels = None,
                                  xTickMajorFontSize = 3.5, # matplotlib.rcParams["xtick.major.size"],
                                  yTickMajorFontSize = 3.5, #matplotlib.rcParams["ytick.major.size"],
                                  ystart = 0, 
                                  yend = 60,
                                  ytickinterval = 2,
                                  ylabelinterval = 10,
                                  yticks = None,
                                  yShownLabels = None,
                                  annotationText = None,
                                  annotationXPosition = 2,
                                  annotationYPosition = 30,
                                  xlabel = "Time",
                                  xunit  = "h",
                                  ylabel = "LWP",
                                  yunit  = "g\ m^{-2}",
                                  useBold = True
                                  )
        PlotTweak.hideYTickLabels( fig2.getAxes()[0,0] )
        
        PlotTweak.setAxesOff( fig2.getAxes()[0,1] )
        PlotTweak.setLegendSimulation(fig2.getAxes()[0,1], [simulationCollection["ICE0_8h"], simulationCollection["ICE1_8h"]])
        
        ax, im, levels = Plot.getTimeseriesOfProfile(fig2.getAxes()[1,1],
                         simulationCollection["ICE0_8h"],
                         "P_RH",
                         levels = None,
                         useLogaritmic = False,
                         colors = None)
        PlotTweak.setAxesOff( fig2.getAxes()[1,0] )
        cax = matplotlib.pyplot.axes([0.05, 0.25, 0.3, 0.03])
        Plot.getColorBar(im, cax, levels)
        
        #Plot.getContourLine(fig2.getAxes()[1,1],"ICE0_8h", color =  'black' , value = 100)
        
        fig2.save()    
    
if __name__ == "__main__":
    start = time.time()
    
    simulationDataFrameCSVFile = "/home/aholaj/Nextcloud/kuvatesti/manuscriptSimulationData.csv"
    main( simulationDataFrameCSVFile )
    
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
