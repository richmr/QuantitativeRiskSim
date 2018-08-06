# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 09:23:03 2018

@author: mrich
"""

import MPIManpowerPools as mp
import MPI_OtherCosts as oc

print "{}: {}".format(mp.MPI_SecurityTeam().EventName, mp.MPI_SecurityTeam().run())
print "{}: {}".format(mp.MPI_ApplicationsTeam().EventName, mp.MPI_ApplicationsTeam().run())
print "{}: {}".format(mp.MPI_ITLeadership().EventName, mp.MPI_ITLeadership().run())
print "{}: {}".format(mp.MPI_PSC().EventName, mp.MPI_PSC().run())
print "{}: {}".format(mp.MPI_ClaimsDept().EventName, mp.MPI_ClaimsDept().run())
print "{}: {}".format(mp.MPI_MedReview().EventName, mp.MPI_MedReview().run())
print "{}: {}".format(mp.MPI_BRD().EventName, mp.MPI_BRD().run())
print "{}: {}".format(mp.MPI_Compliance().EventName, mp.MPI_Compliance().run())
print "{}: {}".format(mp.MPI_LegalCounsel().EventName, mp.MPI_LegalCounsel().run())
    
#newTech = le.decomposedRisk("New Tech Control", .577)
print "{}: {}".format(oc.MPI_NewTechControl().EventName, oc.MPI_NewTechControl().run())
#newTech)
   
print "{}: {}".format(oc.MPI_SoftwareRecode().EventName, oc.MPI_SoftwareRecode().run())
print "{}: {}".format(oc.MPI_IRRetainer().EventName, oc.MPI_IRRetainer().run())
print "{}: {}".format(oc.MPI_Communications().EventName, oc.MPI_Communications().run())
print "{}: {}".format(oc.MPI_HIPAAFines_Modeled().EventName, oc.MPI_HIPAAFines_Modeled().run())