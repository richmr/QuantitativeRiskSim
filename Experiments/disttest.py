# -*- coding: utf-8 -*-
"""
Created on Fri Mar 02 13:19:23 2018

@author: mrich
"""

from numpy.random import uniform

def bob():
    return uniform(1,5)

def test(func):
    return func()

f = bob

def newloss(dist=False, flatProb=.15):
    if dist:
        return dist()
    else:
        return flatProb



def sam(val=lambda what=1:uniform(1,5)):
    return val()

def david(val):
    return val()

#for i in range(10):
#    print david(lambda foo:uniform(1,5))
    
print(newloss())
print(newloss(dist=lambda what=1:uniform(1,5)))