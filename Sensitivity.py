# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 08:10:23 2018

@author: mrich
"""

from LossEventClass import LossEvent
from LossSimClass import LossSim
from LossCurvePlot import plotCurves
from numpy import sort
from numpy.random import uniform
from numpy.random import beta

# Probabilities need to be expressed raw..  Not as percents!
event_01 = LossEvent(".01% Prob", .0001, 25000, 500)
event_02 = LossEvent(".02% Prob", .0002, 25000, 500)
event_03 = LossEvent(".03% Prob", .0003, 25000, 500)
event_1 = LossEvent(".1% Prob", .001, 25000, 500)
event_2 = LossEvent(".2% Prob", .002, 25000, 500)
event_3 = LossEvent(".3% Prob", .003, 25000, 500)
event1 = LossEvent("1.0% Prob", .01, 25000, 500)
event1_uniform = LossEvent("1.0% +/- .5% Prob",lambda foo=1:uniform(.005,.015), 25000, 500)
event1_beta =  LossEvent("1.0% beta",lambda foo=1:beta(1,99), 25000, 500)
event2 = LossEvent("2.0% Prob", .02, 25000, 500)
event3 = LossEvent("3.0% Prob", .03, 25000, 500)

event_5per = LossEvent("5.0% Prob", .05, 25000, 500)
event_5peruniform = LossEvent("5.0% +/- 4% Prob",lambda foo=1:uniform(.01,.09), 25000, 500)
event_5perbeta =  LossEvent("5.0% beta (1 hit in 20)",lambda foo=1:beta(1,19), 25000, 500)

event_4per = LossEvent("4.0% Prob", .04, 25000, 500)
event_4peruniform = LossEvent("4.0% +/- 3% Prob",lambda foo=1:uniform(.01,.07), 25000, 500)


eventLowSpread_1 = LossEvent("100 Lower Bound", .02, 100000, 100)
eventLowSpread_2 = LossEvent("200 Lower Bound", .02, 100000, 200)
eventLowSpread_3 = LossEvent("300 Lower Bound", .02, 100000, 300)

eventMidSpread_1 = LossEvent("1K Lower Bound", .02, 100000, 1000)
eventMidSpread_2 = LossEvent("2K Lower Bound", .02, 100000, 2000)
eventMidSpread_3 = LossEvent("3K Lower Bound", .02, 100000, 3000)

eventHighSpread_1 = LossEvent("10K Lower Bound", .02, 100000, 10000)
eventHighSpread_2 = LossEvent("20K Lower Bound", .02, 100000, 20000)
eventHighSpread_3 = LossEvent("30K Lower Bound", .02, 100000, 30000)

eventUBSpread_1 = LossEvent("25K Upper Bound", .02, 25000, 20000)
eventUBSpread_2 = LossEvent("50K Upper Bound", .02, 50000, 20000)
eventUBSpread_3 = LossEvent("75K Upper Bound", .02, 75000, 20000)

eventUBSpread_4 = LossEvent("250K Upper Bound", .02, 250000, 20000)
eventUBSpread_5 = LossEvent("500K Upper Bound", .02, 500000, 20000)
eventUBSpread_6 = LossEvent("750K Upper Bound", .02, 750000, 20000)

eventUBSpread_7 = LossEvent("2.50M Upper Bound", .02, 2500000, 20000)
eventUBSpread_8 = LossEvent("5.0M Upper Bound", .02, 5000000, 20000)
eventUBSpread_9 = LossEvent("7.5M Upper Bound", .03, 7500000, 20000)
eventUBSpread_9_uniform = LossEvent("7.5M Upper Bound - Uniform", lambda foo=1:uniform(.01,.05), 7500000, 20000)

sim = LossSim()
#sim.attachEvent(event_01)
#sim.attachEvent(event_02)
#sim.attachEvent(event_03)
#sim.attachEvent(event_1)
#sim.attachEvent(event_2)
#sim.attachEvent(event_3)
#sim.attachEvent(event1)
#sim.attachEvent(event1_uniform)
#sim.attachEvent(event1_beta)
#sim.attachEvent(event2)
#sim.attachEvent(event3)

#sim.attachEvent(eventLowSpread_1)
#sim.attachEvent(eventLowSpread_2)
#sim.attachEvent(eventLowSpread_3)
sim.attachEvent(event_5per)
sim.attachEvent(event_5peruniform)
sim.attachEvent(event_4per)
sim.attachEvent(event_4peruniform)


#sim.attachEvent(event_5perbeta)
#sim.attachEvent(eventMidSpread_1)
#sim.attachEvent(eventMidSpread_2)
#sim.attachEvent(eventMidSpread_3)

#sim.attachEvent(eventHighSpread_1)
#sim.attachEvent(eventHighSpread_2)
#sim.attachEvent(eventHighSpread_3)


#sim.attachEvent(eventUBSpread_7)
#sim.attachEvent(eventUBSpread_8)
#sim.attachEvent(eventUBSpread_9)
#sim.attachEvent(eventUBSpread_9_uniform)

sim.run(presentation=True, iterations=100000, aggregate=False)
data, labels = sim.getResults()

results = sim.rankRisks()
