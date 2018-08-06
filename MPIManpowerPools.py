# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 17:14:08 2018

@author: mrich
"""

"""
Established manpower pool models for MPI risk modeling
"""

import LossEventClassv2 as le

def MPI_SecurityTeam(mintime = 5, maxtime = 80, cap = 160):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(175, 125, 175)
    team = le.costOfLaborValue("Security Team", timeDist, costDist)
    return team

def MPI_ITOps(mintime = 5, maxtime = 20, cap = 60):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(235, 115, 340)
    team = le.costOfLaborValue("IT I&O Team", timeDist, costDist)
    return team

def MPI_ApplicationsTeam(mintime = 5, maxtime = 20, cap = 60):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(240, 115, 390)
    team = le.costOfLaborValue("Applications Development", timeDist, costDist)
    return team

def MPI_ITLeadership(mintime = 1, maxtime = 35, cap = 60):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(235, 85, 235)
    team = le.costOfLaborValue("IT Leadership", timeDist, costDist)
    return team

def MPI_PSC(mintime = 2, maxtime = 30, cap = 80):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(265, 65, 375)
    team = le.costOfLaborValue("PSC", timeDist, costDist)
    return team

def MPI_ClaimsDept(mintime = 2, maxtime = 20, cap = 40):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(265, 65, 375)
    team = le.costOfLaborValue("Claims Department", timeDist, costDist)
    return team

def MPI_MedReview(mintime = 1, maxtime = 4, cap = 8):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(140, 65, 175)
    team = le.costOfLaborValue("Medical Review", timeDist, costDist)
    return team

def MPI_BRD(mintime = 1, maxtime = 4, cap = 8):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(140, 65, 175)
    team = le.costOfLaborValue("Benefits Recovery Dept", timeDist, costDist)
    return team

def MPI_Compliance(mintime = 4, maxtime = 40, cap = 80):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.ConstantValue(75)
    team = le.costOfLaborValue("Compliance", timeDist, costDist)
    return team

def MPI_CSuite(mintime = 2, maxtime = 40, cap = 80):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(195, 85, 210)
    team = le.costOfLaborValue("C-Suite", timeDist, costDist)
    return team

def MPI_LegalCounsel(mintime = 2, maxtime = 40, cap = 80):
    """
    Returns a costOfLaborValue object suitable to attach to a sim or other event
    Time is in hours
    """
    timeDist = le.LogNormalValue(maxtime, mintime, cap)
    costDist = le.LogNormalValue(600, 150, 800)
    team = le.costOfLaborValue("Legal Counsel", timeDist, costDist)
    return team