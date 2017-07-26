# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:36:46 2017

@author: MRICH
"""

import LossEventClass
import LossCurvePlot
from numpy import savetxt, linspace, array, sort, save, load
from scipy.integrate import simps

class LossSim:
    """
    Performs a basic Monte Carlo simulation of attached loss events
    """
    
    def __init__(self):
        self.LossEvents = []
        self.data = []
        self.labels = []
        self.minImpacts = []

    def attachEvent(self, newEvent):
        """
        Expects events that are at LossEventClass or a subclass
        """
        self.LossEvents.append(newEvent)
        self.minImpacts.append(newEvent.minImpact)
        
    def run(self, iterations = 10000, aggregate = True, plot = True, presentation = False):
        """
        Runs all the events
        
        iterations = number of simulations to run
        aggregrate = calculate aggregrate losses and include in results
        plot = draw a basic plot automatically
        
        data can be retrieved via getResults method or saved via saveResults
        """
        
        print "[-] LossSim.run: Beginning simulation of {} events with {} iterations each".format(len(self.LossEvents), iterations)
        self.data = []
        self.labels = []
        eventnum = 0
        # clear all the attached events first
        for event in self.LossEvents: event.reset()
        
        for event in self.LossEvents:
            thisdata=[]
            eventnum += 1
            for i in range(iterations):
                thisdata.append(event.run())
            self.data.append(thisdata)
            self.labels.append(event.EventName)
            print "[-] LossSim.run: Completed simulation of event \"{}\" (Event {} of {})".format(event.EventName, eventnum, len(self.LossEvents))  
        
        if aggregate:
            self.labels.append("Total risk")
            self.data.append([sum(i) for i in zip(*self.data)])   
        
        if plot:
            minplot = min(self.minImpacts)
            LossCurvePlot.plotCurves(self.data, self.labels, presentation = presentation, minimum_plotted_impact = minplot)
        
    def plot(self, presentation=False):
        """
        Plots the data in the system
        
        Just a convenience method to allow plotting without running the sim again
        """
        LossCurvePlot.plotCurves(self.data, self.labels, presentation = presentation, minimum_plotted_impact = min(self.minImpacts))
        return
            
    def getResults(self):
        return self.data, self.labels
    
    def saveResults(self, filename):
        # saves the data in binary "npy" format
        to_save = array([self.data, self.labels])
        save(filename, to_save)
        print "[-] LossSim.saveResults: Simulation data saved to {}".format(filename)
       
        
    def loadResults(self, filename):
        # loads sim data
        if (filename[-4:] != '.npy'): filename += ".npy"
        loaded_arr = load(filename)
        self.data = loaded_arr[0]
        self.labels = loaded_arr[1]
        print "[-] LossSim.loadResults: Simulation data loaded from {}".format(filename)
        
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

        print "[-] Calculating average event loss on {} events".format(len(tocalc))        
        for i in range(len(tocalc)):
            data_arr = array(tocalc[i])               
            if (method == 1):
                # Will integrate the data under the curve
                p = linspace(0, max(data_arr), steps)
                lec = LossCurvePlot.calcLossExceedance(data_arr, p, forplot = False)
                thisresult = simps(lec, p)
                results.append(thisresult)
                
        return results
        
    def rankRisks(self, method=1, steps=5000):
        """
        This will return the risks in ranked order, least to most
        
        Uses the results and labels that result from a run
        """
        eal = self.calcEAL(self.data, method=method, steps=steps)
        
        dtype = [('label', 'S25'), ('aal', float)]
        results = zip(self.labels, eal)
        a_results = array(results, dtype)
        a_results = sort(a_results, order='aal')
        return a_results
        
        
        
        