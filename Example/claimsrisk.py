# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 16:19:00 2018

@author: mrich
"""

"""
This model is for a claims data breach resulting in 500 or more records lost
"""

from LossEventClassv2 import decomposedRisk
import scipy.stats as st
import MPIManpowerPools as mp
import MPI_OtherCosts as oc
from LossSimClass import LossSim

def ClaimsData_ConfidentialityBreach():
    """ 
    Returns the LossEvent object that can be added to the sim
    
    Risk probability distribution is from ~2 years of data regarding claims data breaches
    """
    claimsCBreach = decomposedRisk("Claims data confidentiality breach", lambda foo=1:st.beta.rvs(1,20))
    
    # Manpower costs, cost of opportunity with the exception of LegalCounsel which is a real expense
    claimsCBreach.attachEvent(mp.MPI_SecurityTeam())
    claimsCBreach.attachEvent(mp.MPI_ITOps())
    claimsCBreach.attachEvent(mp.MPI_ApplicationsTeam())
    claimsCBreach.attachEvent(mp.MPI_ITLeadership())
    claimsCBreach.attachEvent(mp.MPI_PSC())
    claimsCBreach.attachEvent(mp.MPI_ClaimsDept())
    claimsCBreach.attachEvent(mp.MPI_MedReview())
    claimsCBreach.attachEvent(mp.MPI_BRD())
    claimsCBreach.attachEvent(mp.MPI_Compliance())
    claimsCBreach.attachEvent(mp.MPI_LegalCounsel())
    
    # Other costs.  These tend to be real expenses
    # According to a SANS breach report only 57.7% of respondents bought a new tech control
    newTech = decomposedRisk("New Tech Control", .577)
    newTech.attachEvent(oc.MPI_NewTechControl())
    claimsCBreach.attachEvent(newTech)
    
    claimsCBreach.attachEvent(oc.MPI_SoftwareRecode())
    claimsCBreach.attachEvent(oc.MPI_IRRetainer())
    claimsCBreach.attachEvent(oc.MPI_Communications())
    claimsCBreach.attachEvent(oc.MPI_HIPAAFines_Modeled())
    
    return claimsCBreach
    
def TestRisk():
    sim = LossSim()
    sim.attachEvent(ClaimsData_ConfidentialityBreach())
    sim.run(iterations = 10000, aggregate = False, plot = True, presentation = True)
    return sim



    