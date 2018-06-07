# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:26:04 2017

@author: MRICH
"""

from numpy.random import rand
from numpy import exp, log
from scipy import stats

class LossEvent2(object):
    """
    Abstracted loss event
    init with the eventname only
    Then attach n other loss events that get run during "run"
    
    """
        
    def __init__(self, userEventName):
        self.EventName = userEventName
        self.runQueue = []       
        self.data = []
        
    def attachEvent(self, newEvent):
        if (not isinstance(newEvent, LossEvent2)):
            raise Exception("LossEvent2: Can only add LossEvent2 objects to the run queue")
        self.runQueue.append(newEvent)
        
    def run(self):
        """
        run, at all times, is expected to return a single value for a trial run
        This abstracted class runs through all of the events in the run queue and sums them.
        """
        total = 0
        for evt in self.runQueue:
            total += evt.run()
        
        return total
    
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
    
class LogNormalValue(LossEvent2):
    
    def __init__(self, maxImpact, minImpact, capMaxImpact = False):
        super(LogNormalValue, self).__init__("Basic LogNormal")
        # Calculate the new distributions to speed up math later.  They don't vary with trial
        # Catch bad values
        if ((maxImpact < 0) or (minImpact < 0)):
            raise Exception("LogNormalValue: impacts must be greater than 0")
        
        if (maxImpact < minImpact):
            raise Exception("LogNormalValue: maxImpact must be greater than minImpact")
            
        if (capMaxImpact):
            if (capMaxImpact < maxImpact):
                raise Exception("LogNormalValue: capMaxImpact should be greater than maxImpact")
                
        self.impactDistroStdDev = (log(maxImpact) - log(minImpact))/3.29
        self.impactDistroMean = (log(maxImpact) + log(minImpact))/2.0
        self.capMaxImpact = capMaxImpact
            
    def run(self):
        """
        Always returns a value determined by the lognormal bounds
        """
        loss = stats.lognorm(self.impactDistroStdDev, scale=exp(self.impactDistroMean)).ppf(rand())
        
        if (self.capMaxImpact):
            if (loss > self.capMaxImpact): loss = self.capMaxImpact
        return loss

class ConstantValue(LossEvent2):
    """
    Simply returns the same value every time, as assigned
    A bit of a hack to work with the simulation framework
    """
    
    def __init__(self, flatValue):
        super(ConstantValue, self).__init__("Constant Value")
        # Calculate the new distributions to speed up math later.  They don't vary with trial
        self.flatValue = flatValue
    
    def run(self):
        return self.flatValue
    
    
class basicLossEvent(LossEvent2):
    """
    This is the same as the original LossEvent Class
    Calculates a loss based on a single lognormal distribution
    The probability of occurence can be a flat value, or a probability distribution (lamba)
    Example lambda call: 
        LossEvent("Event foo", lambda foo=1:uniform(.01,.05), 7500000, 20000)
        The "foo = 1" is needed because lambda expects at least one parameter, this gives it a dummy default value
    """
    def __init__(self, userEventName, probDist, maxImpact, minImpact, capMaxImpact = False):
        super(basicLossEvent, self).__init__(userEventName)
        self.attachEvent(LogNormalValue(maxImpact, minImpact, capMaxImpact))
        if callable(probDist):
            self.probDist = probDist
        else:
            if (probDist < 0):
                raise Exception("basicLossEvent: basic probability of occurrence must be >= 0")
            self.basicProbabilityofOccurrence = probDist
            self.probDist = False
    
    def eventOccurred(self):
        """
        Returns true if the event occurs for this run
        """
        chance = 0
        if (self.probDist):
            chance = self.probDist()
        else:
            chance = self.basicProbabilityofOccurrence
            
        if (rand() <= chance):
            return True
        else:
            return False
        
    def run(self):
        """ 
        This is the method called by the simulation.
        Should only return the impact of the run
        """
        result = 0
        if self.eventOccurred():
           result = super(basicLossEvent, self).run()
        
        self.data.append(result)
        return result
        
class costOfLaborValue(LossEvent2):
    """
    This is designed to produce a loss value associated with labor
    It will calculate the time of the labor (per given distribution)
    and the cost of that labor (per given distribution)
    and multiple them to come up with cost of the labor
    
    Sample init:
        costOfExecTime = costOfLaborValue("Executive labor", LogNormalValue(40, 1, 60), LogNormalValue(200,100,300))
        costOfWorkerTime = costOfLaborValue("Line Worker", LogNormalValue(3,1), constantValue(18.50))
    """
    
    def __init__(self, userEventName, hourValueDist, costValueDist):
        super(costOfLaborValue, self).__init__(userEventName)
        if ((not isinstance(hourValueDist, LossEvent2)) or (not isinstance(costValueDist, LossEvent2))):
            raise Exception("costOfLaborValue: hour and cost distributions must be LossEvent2 objects")
        self.hourValueDist = hourValueDist
        self.costValueDist = costValueDist
        
    def run(self):
        """ 
        Returns time * cost per time
        """
        result = self.hourValueDist.run() * self.costValueDist.run()
        return result
        
class decomposedRisk(LossEvent2):
    """
    Blank risk only initialized with a name and a probability distribution
    Must attach LossEvent2 items
    
    Examples:
        riskyEvent = decomposedRisk("Risky event", lambda foo=1:uniform(.01,.05))
         OR
        riskyEvent = decomposedRisk("Risky event", 0.025)
        riskyEvent.attach(costOfLaborValue("Executive labor", LogNormalValue(40, 1, 60), LogNormalValue(200,100,300)))
        riskyEvent.attach(costOfLaborValue("Line Worker", LogNormalValue(3,1), constantValue(18.50)))
        riskyEvent.attach(LogNormalValue(10000, 250000)) # Cost of IT equipment replacement
        
        then riskyEvent.run() will check to see if the event happens, and return the aggregrate value of all attached events
    """
    def __init__(self, userEventName, probDist):
        super(decomposedRisk, self).__init__(userEventName)
        if callable(probDist):
            self.probDist = probDist
        else:
            if (probDist < 0):
                raise Exception("basicLossEvent: basic probability of occurrence must be >= 0")
            self.basicProbabilityofOccurrence = probDist
            self.probDist = False
    
    def eventOccurred(self):
        """
        Returns true if the event occurs for this run
        """
        chance = 0
        if (self.probDist):
            chance = self.probDist()
        else:
            chance = self.basicProbabilityofOccurrence
            
        if (rand() <= chance):
            return True
        else:
            return False
    
    def run(self):
        result = 0
        if self.eventOccurred():
           result = super(decomposedRisk, self).run()
        
        self.data.append(result)
        return result
        
    
    