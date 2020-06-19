# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 16:33:55 2018

@author: mrich
"""

from LossEventClassv2 import *
from LossSimClass import LossSim
from LossCurvePlot import plotCurves

from numpy.random import uniform


riskyEvent = decomposedRisk("Risky event", lambda foo=1:uniform(.01,.05))
riskyEvent.attachEvent(costOfLaborValue("Executive labor", LogNormalValue(40, 1, 60), LogNormalValue(200, 100, 300)))
riskyEvent.attachEvent(costOfLaborValue("Line Worker", LogNormalValue(3, 1), ConstantValue(18.50)))
riskyEvent.attachEvent(LogNormalValue(250000, 10000)) # Cost of IT equipment replacement

sim = LossSim()
replot = sim.replot

sim.attachEvent(riskyEvent)

sim.run(presentation=True, iterations=10000, aggregate=False)


