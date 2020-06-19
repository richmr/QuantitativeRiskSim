# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 17:34:39 2018

@author: mrich
"""

from LossEventClassv2 import LogNormalValue, costOfLaborValue, ConstantValue, LossEvent2, PowerLawValue

def MPI_HardwareCosts(mincost = 50000, maxcost = 300000, cap = 750000):
    cost = LossEvent2("Hardware Costs")
    cost.attachEvent(LogNormalValue(maxcost, mincost, cap))
    return cost

def MPI_SoftwareRecode(mincost = 4000, maxcost = 25000, cap = 100000):
    cost = LossEvent2("Software Dev")
    cost.attachEvent(LogNormalValue(maxcost, mincost, cap))
    return cost

def MPI_IRRetainer(mincost = 5000, maxcost = 105000, cap = 250000):
    cost = LossEvent2("IR Retainer")
    cost.attachEvent(LogNormalValue(maxcost, mincost, cap))
    return cost

def MPI_NewTechControl(mincost = 25000, maxcost = 500000, cap = 1000000):
    cost = LossEvent2("Tech Control")
    cost.attachEvent(LogNormalValue(maxcost, mincost, cap))
    return cost

def MPI_Communications(mincost = 100, maxcost = 90000, cap = 150000):
    cost = LossEvent2("Participant Communications")
    cost.attachEvent(LogNormalValue(maxcost, mincost, cap))
    return cost

def MPI_HIPAAFines_Modeled():
    cost = LossEvent2("HIPAA Fines (Modeled)")
    cost.attachEvent(PowerLawValue(0.43, 25000, 5535640))
    return cost


