#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:20:28 2020

@author: Jaakko Ahola, Finnish Meteorological Institute
@licence: MIT licence Copyright
"""
import datetime
import itertools
import math
import numpy
import operator
import pandas



from collections import defaultdict


class Data:
    def getAllConditions( condition : dict ):
        allConditions = None
        for ind, key in enumerate(list(condition)):
            if ind == 0:
                allConditions = condition[key]
            else:
                allConditions = allConditions & condition[key]
        
        return allConditions
    
    def getORConditions( condition : dict ):
        allConditions = None
        for ind, key in enumerate(list(condition)):
            if ind == 0:
                allConditions = condition[key]
            else:
                allConditions = allConditions | condition[key]
        
        return allConditions
    
    def getNANDConditions( condition : dict ):
        allConditions = None
        for ind, key in enumerate(list(condition)):
            if ind == 0:
                allConditions = ~ condition[key]
            else:
                allConditions = allConditions & ( ~ condition[key])
        
        return allConditions
    
    def getNLengthSubsetConditions( condition : dict, n :int):
        allSubsets = Data.getNLengthSubsetsOfList(list(condition), n)
        
        orSubsetConditions = None
        
        for ind, subset in enumerate(allSubsets):
            subsetDictionary = Data.subdict(condition, subset)
            
            subsetCondition = Data.getAllConditions(subsetDictionary)
            
            if ind == 0:
                orSubsetConditions  = subsetCondition
            else:
                orSubsetConditions = orSubsetConditions | subsetCondition
            
        return orSubsetConditions
            
            
        
    
    def listAll2ChoicesFromList(lista : list, n : int):
        choices = []
        
        for ind1, key1 in enumerate(lista[:-1]):
            for ind2, key2 in enumerate(lista[ind1+1:]):
                choices.append([key1, key2])
        return choices
    
    def getNLengthSubsetsOfList(arr : list, k : int):
        subsets = []
        # Function to find all subsets of given set. 
        # Any repeated subset is considered only  
        # once in the output 
        _list = [] 
        n = len(arr)
        # Run counter i from 000..0 to 111..1 
        for i in range(2**n): 
            subset = []
    
            # consider each element in the set 
            for j in range(n): 
    
                # Check if jth bit in the i is set.  
                # If the bit is set, we consider  
                # jth element from set 
                if (i & (1 << j)) != 0: 
                    subset.append(arr[j])
    
            # if subset is encountered for the first time 
            # If we use set<string>, we can directly insert 
            if subset not in _list and len(subset) > 0: 
                _list.append(subset) 
        # print(_list)
        # consider every subset 
        for subset in _list: 
            if len(subset) == k:
                subsets.append(subset)
        return subsets
    
    def subdict(dictionary, keys):
        vals = []
        if len(keys) >= 1:
            vals = operator.itemgetter(*keys)(dictionary)
        if len(keys) == 1:
            vals = [vals]
        return dict(zip(keys, vals))
        
    def getEpsilon():
        return numpy.finfo(float).eps

    def getClosestIndex(dataarray, searchValue):
        return numpy.argmin(numpy.abs(searchValue- dataarray))
    
    def getColorBin(colorArray, bini, data):
        if any(bindim in data.dims for bindim in ['aeb', 'cla', 'clb', 'ica', 'icb']):
            bini = bini + 3
        else:
            bini = bini
        return colorArray[bini]

    def getBinLimits(valueList):
        valueList = sorted(valueList)
        
        minimum = valueList[0] - (valueList[1] - valueList[0] )
        
        maximum = valueList[-1] + (valueList[-1]-valueList[-2])
        
        
        binLimits = [minimum]

        for ind in range(1,len(valueList)):
            
            binLimits.append( (valueList[ind] + valueList[ind-1])/2 )
            
        binLimits.append(maximum)
        
        return binLimits
    
    def getBinLimitsWithPackingStartingWithLastOnes(valueList, packing):
        
        binLimits = Data.getBinLimits(valueList)
        
        binLimitsPacked = binLimits[:packing]
        
        binLimitsPacked.append(binLimits[-1])
        
        
        return binLimitsPacked
        

    def getIntegerExponentsAsBoolean(dataarray):
        helpArray = numpy.zeros(numpy.shape(dataarray))
        for ind,value in enumerate(dataarray):
            if round(math.modf(value)[0],1) != 0.0:
                helpArray[ind] = 0
            else:
                helpArray[ind] = 1
        
        returnableBoolean = (helpArray > 0.5)
        
        return returnableBoolean   
    
    def getLogScale(dataarray : numpy.array, minimiPotenssi = None, maksimiPotenssi = None):
        
        if minimiPotenssi is None:
            minimiPotenssi = max( math.floor( numpy.log10(numpy.min(dataarray[numpy.where(dataarray > numpy.finfo(float).eps)])) ), math.ceil(numpy.log10(numpy.finfo(float).eps)))
        maksimiPotenssi = math.ceil( numpy.log10(numpy.max(dataarray)) )
        rangePotenssi = list(numpy.arange(minimiPotenssi, maksimiPotenssi +1))
        potenssidict = defaultdict(list)
        
        for num in rangePotenssi:
            if num < 0:
                potenssidict['neg'].append(num)
            else: # This will also append zero to the positive list, you can change the behavior by modifying the conditions 
                potenssidict['pos'].append(num)
        
        if len(potenssidict['neg'])>0:
            negLevels = 1/numpy.power(10, -1*numpy.asarray(potenssidict['neg']))
        else:
            negLevels = numpy.asarray([])
            
        if len(potenssidict['pos'])>0:
            posLevels = numpy.power(10, numpy.asarray(potenssidict['pos']))
        else:
            posLevels = numpy.asarray([])
        
        levels = numpy.concatenate((negLevels,posLevels))
        
        return levels, rangePotenssi, minimiPotenssi, maksimiPotenssi

    # returns a maskedList where bigList values are masked with a boolean value
    # True if element from bigList closest to an element from shortList
    # e.g. bigList = [0,1,2,3,4], shortList = [2,4]
    # returns [False, False, True, False, True]
    def getMaskedList(bigList : list, shortList, initial = False):
        bigList = numpy.asarray(bigList)
        maskedList = [initial]*numpy.shape(bigList)[0]
        
        indexes = [ numpy.argmin(numpy.abs(elem - bigList)) for elem in shortList ]
        
        for i in indexes:
            maskedList[i] = (not initial)
        
        return maskedList
    def getIntergerList(start, end, interval):
        integerList = [ int(elem) for elem in numpy.arange(start, end + interval*0.1, interval) ]
        return integerList
    
    def getFloatList(start, end, interval):
            
        floatList = [ float(elem) for elem in numpy.arange(start, end + interval*0.1, interval) ]
            
        return floatList

    def getRelativeChange(dataarray, denominator = None, limiter = 0, relative = True, lahtoarvo = None):
    
        if denominator is None:
            denominator = dataarray.values
        
        if lahtoarvo is None:
            i = 0
            lahtoarvo = denominator[i]
            
            while lahtoarvo < limiter:
               i += 1
               lahtoarvo = denominator[i]
        dataarray = dataarray/lahtoarvo
    
        return dataarray, lahtoarvo
    
    def isCloseToEpsilon(dataarray : numpy.array, limit = numpy.finfo(float).eps ):
        zero =  False
        if (numpy.abs(numpy.min(dataarray) - numpy.max(dataarray)) < limit ):
            zero = True
    
        return zero
    
    def sortDictionary(dictionary : dict):
        sortedDict = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
        return sortedDict
    
    def getHighAndLowTail(dictionary : dict,
                fraction : float):
        
        return { **Data.getLowTail(dictionary, fraction), **Data.getHighTail(dictionary, fraction) }
    
    def getLowTail(dictionary : dict,
                fraction : float):
        
        tailDict = {}
        keyList = list(dictionary)[:int(len(dictionary)*fraction)]
        
        for key in keyList:
            tailDict[key] = dictionary[key]
        
        return tailDict
    
    def getHighTail(dictionary : dict,
                fraction : float):
        
        tailDict = {}
        keyList = list(dictionary)[-int(len(dictionary)*fraction):]
        
        for key in keyList:
            tailDict[key] = dictionary[key]
        
        return tailDict
    
    def emptyDictionaryWithKeys(keylist : list, value = {}):
        return dict.fromkeys(keylist, value)
    
    def toString(variable):
        returnable = ""
        if variable is not None:
            returnable = str(variable)
        
        return returnable
    def date(format="%Y-%m-%d"):
        return datetime.datetime.utcnow().strftime(format)
    
    def mergeDataFrameWithParam(dataFrame, paramDict, paramName):
        for ind, case in enumerate(list(dataFrame)):
            paramDataFrame  = pandas.DataFrame({"ID":list(paramDict[case]),
                                  paramName : list(paramDict[case].values())})
            del dataFrame[case]["ID"]
            dataFrame[case] =  pandas.merge( dataFrame[case],
                                                            paramDataFrame, on ="ID" )
        
        return dataFrame
    
    def outliersFromDataFrame(dataframe : pandas.DataFrame , variable : str, outlierFrac : float):
        
        low = dataframe[variable].quantile( outlierFrac )
        high  = dataframe[variable].quantile(1.-outlierFrac)
        
        if high < low:
            apu = low
            low = high
            high = apu
            
        
        
        return dataframe[( dataframe[variable] < low ) | (dataframe[variable] > high  )]
    
    
    def midQuantileFromDataFrame(dataframe : pandas.DataFrame , variable : str, outlierFrac : float): #variable  < 0.5
        
        low = dataframe[variable].quantile( outlierFrac )
        high  = dataframe[variable].quantile(1.-outlierFrac)
        
        if high < low:
            apu = low
            low = high
            high = apu
    
        
        return dataframe[( dataframe[variable] >  low ) & ( dataframe[variable] < high  )]
    
    def cycleBoolean(numberOfElements, startBoolean = True):
        cyclableValues = itertools.cycle([ startBoolean, not startBoolean])
        
        cycledList = []
        for i in range(numberOfElements):
            cycledList.append(next(cyclableValues))
            
        return cycledList
        
    def roundUp(number, scale):
        return int(round((number + scale)/scale,0)*scale)
    
    def roundDown(number, scale):
        return int(round((number - scale)/scale,0)*scale)
    
    def timeDuration(durationSeconds) -> str:
        durationStr = ""
        secondsUnitConversion = numpy.asarray([24,60,60])
        
        days = divmod(durationSeconds, numpy.prod(secondsUnitConversion))
        hours = divmod(days[1], numpy.prod(secondsUnitConversion[1:]))
        minutes = divmod(hours[1], numpy.prod(secondsUnitConversion[2:]))
        seconds = minutes[1]
        
        days = days[0]
        hours = hours[0]
        minutes = minutes[0]
        
        daysUsed = days >= 1
        hoursUsed = hours >= 1
        minutesUsed = minutes >= 1
        
        if daysUsed:
            
            durationStr += f"{days:.0f} days"
        
        if hoursUsed: 
            intermezzo = " " if daysUsed else ""
            durationStr += f"{intermezzo}{hours:.0f} hours"
        
        if minutesUsed:
            intermezzo = " " if (daysUsed or hoursUsed) else ""
                
            durationStr += f"{intermezzo}{minutes:.0f} minutes"
        
        intermezzo = " " if (hoursUsed or minutesUsed) else ""
        durationStr += f"{intermezzo}{seconds:.1f} seconds"
        
        return durationStr
        
        