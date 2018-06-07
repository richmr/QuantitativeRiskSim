# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 13:49:11 2018

@author: mrich
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:15:47 2017

@author: MRICH
"""

"""
Computer banking loss and risk model

"""

from LossEventClassv2 import basicLossEvent
from LossSimClass import LossSim
from LossCurvePlot import plotCurves
from numpy import sort


BankingPhish = basicLossEvent("Banking Trojan", .05, 25000, 500, 35000)
Ransomware = basicLossEvent("Ransomware", .10, 3000, 200)
JealousBoyfriend = basicLossEvent("Creepy Spyware", .02, 2000, 300, 5000)
AmazonSpendingSpree = basicLossEvent("Amazon Spree", .3, 750, 150)
#InAppPurchases = LossEvent("In App Puchases", .10, 100, 5)
#TransferFail = LossEvent("Savings Transfer", .085, 200, 5)
CatAttack = basicLossEvent("Clumsy Cat", .05, 3000, 750)

sim = LossSim()
replot = sim.replot
sim.attachEvent(BankingPhish)
sim.attachEvent(Ransomware)
sim.attachEvent(JealousBoyfriend)
sim.attachEvent(AmazonSpendingSpree)
#sim.attachEvent(InAppPurchases)
#sim.attachEvent(TransferFail)
sim.attachEvent(CatAttack)

sim.run(presentation=True, iterations=10000)
data, labels = sim.getResults()

results = sim.rankRisks()
