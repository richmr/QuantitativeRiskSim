# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:56:48 2018

@author: mrich
"""

import datetime as dt

def timeWindowBetaCalc(timeframe, eventDates, startday, stopday = False, alpha_prior = 1, beta_prior = 1, dtformat = '%m/%d/%Y'):
    """
    This will return the Alpha and Beta parameters for a beta distribution 
    based on the how many times the sliding time window [timeframe] included a 
    date on the eventDates array.  Starts the analysis at the date: startday and
    ends on stopday
    
    For example: If timeframe = 6 months, and event dates = [1/17, 12/17],
    then the algorithm will produce:
        1/17 - 6/17: HIT
        2/17 - 7/17: MISS
        3/17 - 8/17: MISS
        4/17 - 9/17: MISS
        5/17 - 10/17: MISS
        6/17 - 11/17: MISS
        7/17 - 12/17: HIT
        
        HIT: 2, MISS: 5 -> Alpha = 3, Beta = 6
    
    timeframes are strings specified as: n unit
    where:
        n = is the size of the frame 
        unit is in ['d', 'mo', 'yr']:
            d = "days"
            mo = "months"
            yr = "years"
    
    eventDates is an array of event dates formatted:
        %m/%d/%Y
        alternatively you can specify a format for the date entries in dtformat
        using the 1989 C standard (see https://docs.python.org/2/library/datetime.html)
        
    startday and stopday should be formatted to match the dates in eventDates
    stopday defaults to today
        
    A sample call based on the scenario above looks like:
        new_alpha, new_beta = timeWindowBetaCalc('6 mo', ['1/17', '12/17'], startday='1/17', stopday='12/17', dtformat='%m/%y')
    """
    new_alpha = alpha_prior
    new_beta = beta_prior
        
    # Convert the eventDates array to actual datetime values
    eventDates_dt = [dt.datetime.strptime(adate, dtformat) for adate in eventDates]
    # Order them
    eventDates_dt.sort()
    startday_dt = dt.datetime.strptime(startday, dtformat)
    stopday_dt = 0
    if (not stopday):
        # set to now
        stopday_dt = dt.datetime.today()
    else:
        stopday_dt = dt.datetime.strptime(stopday, dtformat)
    
    # parse time frame
    tframe_dat = timeframe.split()
    window = int(tframe_dat[0])
    sample = 1 # 1 day sample interval
    
    # I'm using a forgiving interpretation of the scale parameter.
    # https://media.giphy.com/media/yKuPJ1fxNUAx2/giphy.gif
    
    # Everything gets rebaselined as days, because date math is annoying
    if (tframe_dat[1][0] == "d"):
        # No change to interval or sample
        window = window
    elif (tframe_dat[1][0] == "m"):
        # Convert months to days..  Using average days/month.
        window = (365/12)*window
        sample = (365/12)
    elif (tframe_dat[1][0] == "y"):
        window = 365*window
        sample = 365
        
    window_dt = dt.timedelta(window)
    sample_dt = dt.timedelta(sample)
    
    # need to push stopday by sample size to ensure we get the range
    stopday_dt += sample_dt
    
    print(("{}".format(window_dt)))
    print(("{}".format(stopday_dt)))
    # begin the hunt
    windowStart_dt = startday_dt
    windowStop_dt = windowStart_dt + window_dt
    wasAHit = False
    while (windowStop_dt <= stopday_dt):
        
        for event_dt in eventDates_dt:
            # these have been date ordered
            if (event_dt > windowStop_dt):
                break
            if ((event_dt >= windowStart_dt) and (event_dt < windowStop_dt)):
                # It hits
                new_alpha += 1
                wasAHit = True
                # Only one hit is necessary in an interval for it to be a hit
                break
        if (not wasAHit):
            # then it's a miss
            new_beta += 1
        # print("{} {} {}".format(windowStart_dt, windowStop_dt, wasAHit))
        wasAHit = False
        windowStart_dt += sample_dt
        windowStop_dt = windowStart_dt + window_dt
    
    return new_alpha, new_beta

def BPCtest():
    new_alpha, new_beta = timeWindowBetaCalc('6 mo', ['1/17', '12/17'], startday='1/17', stopday='12/17', dtformat='%m/%y')
    print(("{}, {}".format(new_alpha, new_beta)))
    
def MailTest():
    eventData = ['8/26/2016', '9/2/2016', '1/13/2017', '3/2/2017', '3/30/2017', 
                 '11/1/2017', '2/17/2018', '3/8/2018', '5/10/2018', '6/11/2018', 
                 '6/21/2018', '6/27/2018']

    new_alpha, new_beta = timeWindowBetaCalc('6 mo', eventData, startday='8/1/2016')
    print(("{}, {}".format(new_alpha, new_beta)))