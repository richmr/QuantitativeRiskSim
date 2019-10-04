#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 20:24:54 2017

@author: mrrich
"""

"""
This contains methods to plot loss exceedance curves
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from numpy import percentile, linspace, count_nonzero, array, ndarray, nonzero
from scipy import floor, log10

def calcLossExceedance(data, p, forplot = True):
    """
    This will calculate the loss exceedence for a given set of data
    and a loss value p
    
    This expects a single column of data
    
    if forplot is True, will scale probabilities to percents for clean plotting
    Othewise, leaves probability values as < 1
   
    This will accept p as a linspace, or p as a discrete 
    """
#    p = 100-p
#    loss = percentile(data, p)
#    return loss
#    countif = (data>p).sum()
#    perc = countif/float(len(data))
    lenOfData = float(len(data))
#    
#    if ((type(p) == int) or (type(p) == float)):
#        lec = (([data>p]).sum()/lenOfData)
#        if forplot:
#            lec = lec * 100
           
    if forplot:
        lec = [((data>pi).sum()/lenOfData) * 100.0 for pi in p]
    else:
        lec = [((data>pi).sum()/lenOfData) for pi in p]

    return lec

def moneyformat(x, pos):
    """
    Generic money formatter to help plot look nice
    """
    if (x < 1000):  return '$%1.0f' % x
    if (x < 10000): return '$%1.1fK' % (x/1000.0)
    if (x < 1000000): return '$%1.0fK' % (x/1000.0)
    if (x < 1e9): return '$%1.1fM' % (x/1.0e6)
    if (x < 1e12): return '$%1.1fB' % (x/1.0e9)
    return '$%1.1fT' % (x/1.0e12)

def rawformat(x, pos):
    """
    Generic number formatter to help log plot look nice
    """
    if (x < 1000):  return '%1.0f' % x
    if (x < 10000): return '%1.1fK' % (x/1000.0)
    if (x < 1000000): return '%1.0fK' % (x/1000.0)
    if (x < 1e9): return '%1.1fM' % (x/1.0e6)
    if (x < 1e12): return '%1.1fB' % (x/1.0e9)
    return '%1.1fT' % (x/1.0e12)
    
def percentformat(x, pos):
    """
    Generic percent formatter, just adds a percent sign
    """
    if (x==0): return "0%"
    if (x<0.1): return ('%4.3f' % (x)) + "%" 
    if (x<1): return ('%3.2f' % (x)) + "%" 
    if (x<5): return ('%2.1f' % (x)) + "%" 
    return ('%1.0f' % x) + "%"
    
moneyformatter = FuncFormatter(moneyformat)
percentformatter = FuncFormatter(percentformat)
rawformatter = FuncFormatter(rawformat)
    
def plotCurves(data_set, labels = [], presentation = False, x_label = "Impact ($)", y_label = "Probability of Impact", steps=5000,
               impactformatter = moneyformatter, minimum_plotted_impact = 1):
    """
    Plots loss exceedence curves,
    
    data_set is a list of columns of equal numbers of simulations for all the loss events
        (Even 1 column should be in a list)
    labels = labels for the legend, a list in the same order as the data_set
    steps is the number of steps to calculate, more steps = smoother plot
    presentation = True if you want a nice, high-res plot to work with (False results in default)
    impactformatter = custom formatter for x-axis in FuncFormatter  
    """
    #  Set up colors
    # Color "rotation" code from: http://matplotlib.org/1.3.1/examples/pylab_examples/line_styles.html
    colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    
   
    #fig = plt.figure(figsize=(9,6)) 
    
    fig, ax = plt.subplots(figsize=(9,6))
    
#    if presentation:
#        fig.figure(figsize=(15,10))
    
    if (len(labels)):
        if (len(labels) < len(data_set)):
            raise Exception("LossCurvePlot.plotCurves: Not enough labels for all columns in your data set")
            
    """
    p = linspace(0,100,steps)
    maxX = 0
    maxY = 0
    for i in range(len(data_set)):
        data = data_set[i]
        color = colors[i % len(colors)]
        maxX = max([maxX, max(data)])
        maxY = max([maxY, (count_nonzero(data)/float(len(data))*100)])
        if labels:
            plt.plot(calcLossExceedance(data, p), p, color=color, label=labels[i])
        else:
            plt.plot(calcLossExceedance(data, p), p, color=color)
    """
    maxX = 0
    maxY = 0
    minX = 10**floor(log10(minimum_plotted_impact))
    print("[-] LossCurvePlot.plotCurves: Plotting {} event curves".format(len(data_set)))
    for i in range(len(data_set)):
        data_arr = array(data_set[i])
        print("[-] LossCurvePlot.plotCurves: Calculating {} of {} loss exceedance curves".format(i+1, len(data_set)))
        p = linspace(0, max(data_arr), steps)
        lec = calcLossExceedance(data_arr, p)
        color = colors[i % len(colors)]
        maxX = max([maxX, max(data_arr)])
        maxY = max([maxY, (count_nonzero(data_arr)/float(len(data_arr))*100)])
        if len(labels):
            lines = plt.plot(p, lec, color=color, label=labels[i])
            plt.setp(lines, linewidth=2)
            # this is to show area under the curve, just for demo
            # plt.fill_between(p, lec)
        else:
            lines = plt.plot(p, lec, color=color)
            plt.setp(lines, linewidth=2)
    
    plt.xscale('log')
    
    # This is to show area under the curve 
    ax.xaxis.set_major_formatter(impactformatter)
    ax.yaxis.set_major_formatter(percentformatter)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True, which='both')
    plt.axis([minX,maxX,0,maxY+.1*maxY])
    if len(labels):
        plt.legend()
    plt.show()
    return 
    

    