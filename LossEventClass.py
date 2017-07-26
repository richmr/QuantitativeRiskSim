# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:26:04 2017

@author: MRICH
"""

from numpy.random import rand
from numpy import exp, log
from scipy import stats

class LossEvent:
    """
    This is a basic Monte Carlo event, based on Hubbard's work
    Probability of occurrance is 15%
    Impact is a log-normal distribution with a min and max bound, can be capped
    Impacts need to be nonzero and positive
    """
        
    def __init__(self, userEventName, initProb = .15, initMaxImpact = 10000, initMinImpact = 5000, initCapMaxImpact = False):
        self.EventName = userEventName
        self.Description = "Not set"
        self.impactDistroMean = 0
        self.impactDistroStdDev = 0
        self.setProbabilityofOccurrence(initProb)
        self.setImpactBounds(initMaxImpact, initMinImpact, initCapMaxImpact)
        self.data = []
        
        
    def setProbabilityofOccurrence(self, newProb):
        if (newProb < 0):
            raise Exception("LossEvent: basicProbability of occurrence must be >= 0")
        self.basicProbabilityofOccurrence = newProb
    
    def setImpactBounds(self, newMaxImpact, newMinImpact, newCapMaxImpact = False):
        if (newMaxImpact <= 0) or (newMinImpact <= 0):
            raise Exception("LossEvent: impacts must be greater than zero")
        if (newMaxImpact <= newMinImpact):
            raise Exception("LossEvent: max impact must be greater than the min impact")
        self.maxImpact = newMaxImpact
        self.minImpact = newMinImpact
        self.capMaxImpact = newCapMaxImpact
        
        # Calculate the new distributions to speed up math later.  They don't vary with trial
        self.impactDistroStdDev = (log(self.maxImpact) - log(self.minImpact))/3.29
        self.impactDistroMean = (log(self.maxImpact) + log(self.minImpact))/2.0
        
        
    def eventOccurred(self):
        """
        Returns true if the event occurs for this run
        """
        if (rand() <= self.basicProbabilityofOccurrence):
            return True
        else:
            return False
        
    def eventLoss(self):
        """
        Returns the value of the loss for this trial
        """
        loss = stats.lognorm(self.impactDistroStdDev, scale=exp(self.impactDistroMean)).ppf(rand())
        
        if (self.capMaxImpact):
            if (loss > self.capMaxImpact): loss = self.capMaxImpact
        return loss        
    
        
    def run(self):
        """ 
        This is the method called by the simulation.
        Should only return the impact of the run
        """
        result = 0
        if self.eventOccurred():
            result = self.eventLoss()
        
        self.data.append(result)
        return result
        
    def reset(self):
        """
        Just resets the data in the event
        """
        self.data=[]

    def getResults(self):
        """
        returns the data for this event
        """
        return self.data 
        

    
    