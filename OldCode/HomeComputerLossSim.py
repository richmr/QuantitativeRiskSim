# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:15:47 2017

@author: MRICH
"""

"""
Computer banking loss and risk model

"""

from LossEventClass import LossEvent
from LossSimClass import LossSim
from LossCurvePlot import plotCurves
from numpy import sort


BankingPhish = LossEvent("Banking Trojan", .05, 25000, 500, 35000)
Ransomware = LossEvent("Ransomware", .10, 3000, 200)
JealousBoyfriend = LossEvent("Creepy Spyware", .02, 2000, 300, 5000)
AmazonSpendingSpree = LossEvent("Amazon Spree", .3, 750, 150)
#InAppPurchases = LossEvent("In App Puchases", .10, 100, 5)
#TransferFail = LossEvent("Savings Transfer", .085, 200, 5)
CatAttack = LossEvent("Clumsy Cat", .05, 3000, 750)

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
