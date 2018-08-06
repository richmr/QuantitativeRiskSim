#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 21:09:11 2018

@author: mrich
"""

from numpy import random
from LossEventClassv2 import LossEvent2
from LossSimClass import LossSim


def tumblerRun(goal, dist=lambda foo=1:random.randint(0,10), minVal = 0, maxVal = 9):
    # returns the number of times the tumbler must be scrambled to return to the goal
    numtries = 0
    scramvalue = goal + 1
    while (scramvalue != goal):
        numtries += 1
        scram = dist()
        scramvalue = (goal + scram) % maxVal
    
    return numtries

class tumblerClass(LossEvent2):
    
    def __init__(self, goal, dist=lambda foo=1:random.randint(0,10), minVal = 0, maxVal = 9):
        super(tumblerClass, self).__init__("Tumbler Test")
        self.goal = goal
            
    def run(self):
        """
        returns a tumblerRun
        """
        return tumblerRun(self.goal)
    

tumbSim = LossSim()
tumb1 = tumblerClass(4)
replot = tumbSim.replot

tumbSim.attachEvent(tumb1)

tumbSim.run(presentation=True, iterations=10000, aggregate=False)

import matplotlib.pyplot as plt
data, labels = tumbSim.getResults()
plt.hist(data[0], range(1,max(data[0])))
