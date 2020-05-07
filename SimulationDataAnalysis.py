#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:38:34 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import time

import numpy
import xarray
from Simulation import Simulation

class SimulationDataAnalysis:
    
    def getTimeseriesOfProportions(axes,
                                   simulation : Simulation,
                                   muuttuja,
                                   mode = "inCloud", cmap = "bright", limit = 1e-6, height = None, packing = None,
                                   timeStartH = 2.05, timeEndH = 48, analysis = False,
                                   fontsize = None, useLegend = True,
                                   figurePrefix = "",
                                   kuvakansio = "/home/aholaj/OneDrive/000_WORK/000_ARTIKKELIT/000-Manuscript-ICE/kuvat/bini/",
                                   kuvakansioPDF = "/home/aholaj/OneDrive/000_WORK/000_ARTIKKELIT/000-Manuscript-ICE/figures_pdf",
                                   filenamePDF = "figure6"):
        
        print(mode, end = " ")
        if height is not None:
            print(height)
        else:
            print()
        
        
        ps = simulation.getPSDataset()
        if ps is None:
            return "FileNotFound"
        
        ts = simulation.getTSDataset()
        if ts is None:
            return "FileNotFound"
        
        timeStartInd = Data.getClosestIndex( ps.time.values, timeStartH*3600 )
        timeEndInd   = Data.getClosestIndex( ps.time.values, timeEndH*3600 )
        ps = ps.isel(time = slice(timeStartInd,timeEndInd))
        
        
        try:
        
            if mode == "inCloud":
               # ps = ps.sel(zt = slice(665,745)).mean(dim = "zt")
                ps = ps.where( (ps.P_rl > limit) & (ps.P_ri > limit), drop = True).mean(dim = "zt", skipna = True) #ps.where(ps.zt > ts.zb).where(ps.zt < ts.zc).mean(dim = "zt")#
            elif mode == "belowCloud":
                #ps = ps.sel(zt = slice(5,410)).mean(dim = "zt")
                ps = ps.where(ps.P_rl < limit, drop = True).where(ps.zt < ts.zb, drop = True).mean(dim = "zt", skipna = True) #.where(ps.P_rl < 1e-6, drop = True)
            elif mode == "aboveCloud":
                ps = ps.where(ps.zt > ts.zc, drop = True).mean(dim = "zt", skipna = True) #.where(ps.P_rl < 1e-6, drop = True)
            elif mode == "height":
                ps = ps.sel(zt = height, method = 'nearest')        
        except KeyError:
            return
        
        ps = ps.assign_coords(time = (ps.time / 3600))
        
                
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
        
        total = aero + cloud + ice
        
        if packing is not None:
            for daatta in aero, cloud, ice, total:
                daatta[:,packing] = numpy.sum(daatta[:,packing:], axis = 1)
        
        binNumber = min( numpy.shape(total.values)[1], packing +1 )
        
        
        matplotlib.rcParams['lines.linewidth'] = 6
        yTicks = [0, 0.5, 1]
        yTickLabels = map(str, yTicks)
            
        matplotlib.pyplot.subplots_adjust(hspace=0.05, wspace = 0.05)
            
        xLabelListShow = numpy.arange(8, 48+1, 8)
        xLabelListShow = numpy.insert(xLabelListShow, 0, 2)
        
        xLabelListMajorLine = numpy.arange(4, 48+1, 4)
        xLabelListMajorLine = numpy.insert(xLabelListMajorLine, 0, 2)
        
        for bini in range(binNumber):
            ax = axes[bini]
            aeroBin = aero[:,bini]
            cloudBin = cloud[:,bini]
            iceBin  = ice[:,bini]
            
            totalBin = total[:,bini]
            
            aeroFrac = aeroBin/totalBin
            cloudFrac = cloudBin/totalBin
            iceFrac = iceBin/totalBin
            
            totalBinRelative  = totalBin / totalBin.values[0]
            
            aeroFrac.plot(ax=ax, color = "#e6194B")
            cloudFrac.plot(ax=ax, color = "#000075")
            iceFrac.plot(ax=ax, color = "#42d4f4")
            totalBinRelative.plot(ax = ax, color = "black")
            
            ax.set_yticks( yTicks )
            ax.set_yticklabels( yTickLabels )
            ax.set_ylim( 0, 1.5)
            ax.set_title("")
            matplotlib.pyplot.setp(ax.get_yticklabels()[1], visible=False)
            
            if packing is not None and bini == (binNumber - 1):
                bininame = str(bini + 1 ) + " - 7"
            else:
                bininame = str(bini +1)
            
            if useLegend:
                legend_handles = [matplotlib.patches.Patch( facecolor = "black",
                            label = " ".join([ "Bin", bininame + ",", "Total", r"$N_0$",  str(int(totalBin.values[0])) + ",", "Min", r"$N$", str(int(numpy.min(totalBin))), "$(kg^{-1})$"  ]))]
                legend = ax.legend(handles = legend_handles, loc = "best", fontsize = fontsize)
                ax.add_artist(legend)
                
                if bini == 0:
                    header_handles = [matplotlib.patches.Patch(facecolor = "#e6194B", label="Aerosol"),
                                            matplotlib.patches.Patch(facecolor = "#000075", label="Cloud"),
                                            matplotlib.patches.Patch(facecolor = "#42d4f4", label="Ice")]
                                                  
                    header_legend = ax.legend(handles = header_handles, loc =(0.3,1.05), ncol = 3, frameon = True, framealpha = 1.0, fontsize = fontsize)
                    
                    ax.add_artist(header_legend)
            ########## END USELEGEND
            
            if bini in [2,3]:
                setXlabel= True
            else:
                setXlabel =False
            
            ax = PlotTweak.setXTicksLabelsAsTime(ax, ps.time.values, xLabelListShow = xLabelListShow, xLabelListMajorLine = xLabelListMajorLine, setXlabel = setXlabel)
            
            if bini in [0,1]:
                ax.set_xticklabels([])
            
        axes[2].set_yticklabels([str(item) for item in yTicks])
        for tick in axes[2].get_yticklabels():
            print(tick)
            tick.set_visible(True)
        
        return axes
def main():
   
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(round((end - start),0)) + " seconds")
