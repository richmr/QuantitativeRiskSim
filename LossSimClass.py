# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:36:46 2017

@author: MRICH
"""

import LossEventClassv2
import LossCurvePlot
from numpy import savetxt, linspace, array, sort, save, load, count_nonzero, gradient
from scipy.integrate import simps
import tqdm
import pandas as pd

# global replot

class LossSim:
    """
    Performs a basic Monte Carlo simulation of attached loss events
    """
    
    def __init__(self):
        self.LossEvents = []
        self.data = []
        self.labels = []
        self.minImpacts = []
        self.plotCurves = LossCurvePlot.plotCurves
        # Empyt dataframe as placeholder
        self.totalLossDataframe = pd.DataFrame()
        

    def attachEvent(self, newEvent):
        """
        Expects events that are at LossEventClass or a subclass
        """
        self.LossEvents.append(newEvent)
        #self.minImpacts.append(newEvent.minImpact)
        
    def run(self, iterations = 10000, aggregate = True, plot = True, presentation = False):
        """
        Runs all the events
        
        iterations = number of simulations to run
        aggregrate = calculate aggregrate losses and include in results
        plot = draw a basic plot automatically
        
        data can be retrieved via getResults method or saved via saveResults
        """
        
        print("[-] LossSim.run: Beginning simulation of {} events with {} iterations each".format(len(self.LossEvents), iterations))
        self.data = []
        self.labels = []
        eventnum = 0
        totalsims = len(self.LossEvents)*iterations # number of sim iterations
        # clear all the attached events first
        progBar = tqdm.tqdm(total=totalsims, desc="Simulation Progress")
        
        for event in self.LossEvents: event.reset()
        
        for event in self.LossEvents:
            thisdata=[]
            eventnum += 1
            for i in range(iterations):
                thisdata.append(event.run())
                progBar.update()
            # self.minImpacts.append(min(thisdata))
            # Can't do the above line because the min of every case is always zero.  We need the effective "useful" min
            # Try getting the mean and stddev, then find LEC for stddev-3*mean
            # for the record, stddev of a log-normal is kind of useless
            # Hack to get a good minimal plot point from the data:
            # Sort the data array
            # Get the gradient of this array
            # Count the non-zeros
            # look for first non-zero value towards end of array from -nonzero count
            # set minimum value to the value at sorted[-that location]
            # No Bothans were harmed to make this hack
            s_data = sort(thisdata)
            gs_data = gradient(s_data)
            index = count_nonzero(gs_data)
            while (s_data[-index] == 0):
                index -= 1
            # print "[d] LossSim.run: Min impact = {}".format(s_data[-index])
            self.minImpacts.append(s_data[-index])
            
            self.data.append(thisdata)
            self.labels.append(event.EventName)
            #newdesc = "Completed simulation of \"{}\" (Event {} of {})".format(event.EventName, eventnum, len(self.LossEvents))  
            #progBar.set_description(desc=newdesc, refresh=True)
            
        progBar.close()
        if aggregate:
            self.labels.append("Total risk")
            self.data.append([sum(i) for i in zip(*self.data)])
            # Populate the data frame
            # https://stackoverflow.com/questions/25577352/plotting-cdf-of-a-pandas-series-in-python
            # Define your series
            s = pd.Series(self.data[-1], name = 'loss')
            df = pd.DataFrame(s)             
            # Get the frequency, PDF and CDF for each value in the series             
            # Frequency
            stats_df = df \
                        .groupby('loss')['loss'] \
                        .agg('count') \
                        .pipe(pd.DataFrame) \
                        .rename(columns = {'loss': 'frequency'})
             
            # PDF
            stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
             
            # CDF
            stats_df['cdf'] = stats_df['pdf'].cumsum()
            stats_df = stats_df.reset_index()
            self.totalLossDataframe = stats_df
            
        if plot:
            minplot = min(self.minImpacts)
            LossCurvePlot.plotCurves(self.data, self.labels, presentation = presentation, minimum_plotted_impact = minplot)
                        
            print("[-] Use 'replot(minImpact, [presentation=True/False])' if you don't like the x range of the current plot.")
        
    def plot(self, presentation=False):
        """
        Plots the data in the system
        
        Just a convenience method to allow plotting without running the sim again
        """
        LossCurvePlot.plotCurves(self.data, self.labels, presentation = presentation, minimum_plotted_impact = min(self.minImpacts))
        return
    
    def replot(self, minImpact, presentation=False):
        self.minImpacts = [minImpact]
        self.plot(presentation)
            
    def getResults(self):
        return self.data, self.labels
    
    def saveResults(self, filename):
        # saves the data in binary "npy" format
        to_save = array([self.data, self.labels])
        save(filename, to_save)
        print("[-] LossSim.saveResults: Simulation data saved to {}".format(filename))
       
        
    def loadResults(self, filename):
        # loads sim data
        if (filename[-4:] != '.npy'): filename += ".npy"
        loaded_arr = load(filename)
        self.data = loaded_arr[0]
        self.labels = loaded_arr[1]
        print("[-] LossSim.loadResults: Simulation data loaded from {}".format(filename))
        
    def calcEAL(self, tocalc = [], method=1, steps=5000):
        """
        This reduces lec curves to a single value for ordinal ranking
        
        Returns the results in the same order they were presented
        
        The current method used is to integrate the area under the curve
        TODO: I probably should make possible methods a enum structure, but skipping for now
        
        if an array is passed into tocalc, then that data is calculated and the results returned.
        if not, it uses the data found in self.data.  In general, don't call until after "run"
        """
        if (len(tocalc) == 0): tocalc = self.data
        results = []

        print("[-] Calculating average event loss on {} events".format(len(tocalc)))        
        for i in range(len(tocalc)):
            data_arr = array(tocalc[i])               
            if (method == 1):
                # Will integrate the data under the curve
                p = linspace(0, max(data_arr), steps)
                lec = LossCurvePlot.calcLossExceedance(data_arr, p, forplot = False)
                thisresult = simps(lec, p)
                results.append(thisresult)
                
        return results
    
    def getMinAndMaxTotalLoss(self):
        if self.totalLossDataframe.size == 0:
            raise Exception("Can't use dataframe analysis unless run is called with aggregate=True")
        # Ignores 0
        minLoss = self.totalLossDataframe["loss"][1]
        maxLoss = self.totalLossDataframe["loss"].max()
        return minLoss, maxLoss
    
    def getProbabilityOfLossGreaterOrLessThan(self, lossValue):
        if self.totalLossDataframe.size == 0:
            raise Exception("Can't use dataframe analysis unless run is called with aggregate=True")
        cdf_val = self.totalLossDataframe[self.totalLossDataframe["loss"] >= lossValue]["cdf"].min()
        return 1.0-cdf_val
        
    def rankRisks(self, method=1, steps=5000):
        """
        This will return the risks in ranked order, least to most
        
        Uses the results and labels that result from a run
        """
        eal = self.calcEAL(self.data, method=method, steps=steps)
        
        dtype = [('label', 'S25'), ('aal', float)]
        results = list(zip(self.labels, eal))
        a_results = array(results, dtype)
        a_results = sort(a_results, order='aal')
        return a_results
        
        
        
        