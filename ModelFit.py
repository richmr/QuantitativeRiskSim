# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:44:19 2018

@author: tmthydvnprt
This function is adapted from the discussion at:
https://stackoverflow.com/questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-scipy-python

Though I've made it easy to use, I did NOT write this awesome code - mrich
"""

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler



#plt.hist(finesdata)
#%matplotlib inline
import warnings
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib


matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy,
        # st.frechet_r,st.frechet_l,
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Propbability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    print(f"{arg}, {loc}, {scale}")

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    print(f"{start}")
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)
    print(f"{end}")

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    print(f"{x[:3]}")
    y = dist.pdf(x, *arg, loc=loc, scale=scale)
    pdf = pd.Series(y*size, x)

    return pdf

def distro_hist(dist, params, trials, bins=200):
    trial_results = dist(*params).rvs(trials)
    y, x = np.histogram(trial_results, bins=bins)
    return y,x, trial_results
   
    

def do_fit(data, chartTitle = "Data", xlabel = '$'):
    """
    data = array of data
    chartTitle = Top line to be displayed on the generated charts
    xlabel = Label for x axis
    """
 
    data = pd.Series(data)
    
       
    # Find best fit distribution
    best_fit_name, best_fir_paramms = best_fit_distribution(data, 200)
    best_dist = getattr(st, best_fit_name)
    
    
    # "giggle" check the fit
    trial_results = pd.Series(best_dist(*best_fir_paramms).rvs(len(data)))
    
    # Display
    plt.figure(figsize=(12,8))
    ax = data.plot(kind='hist', bins=50, alpha=0.5, label='Data', legend=True) # normed=True, deprecated?
    trial_results.plot(kind='hist', bins=50, alpha=0.5, label="Model Trials", legend=True, ax=ax)
    
    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fir_paramms)])
    dist_str = '{}({})'.format(best_fit_name, param_str)
    
    ax.set_title(chartTitle + '\nBest fit distribution \n' + dist_str)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Frequency')
    
    # Print the dist string for easy cut and paste
    print("Best fit: scipy.stats.{}".format(dist_str))

# Experiments
def test1():
    dist = st.johnsonsb(a=1.60, b=0.49, loc=7474.12, scale=17452673.57)
    dist_plain = st.johnsonsb
    params = [1.60, 0.49, 474.12, 17452673.57]
    pdf = make_pdf(dist_plain, params, size=int(1e6))
    return dist, pdf

def test2():
    dist = st.johnsonsb(a=1.60, b=0.49, loc=7474.12, scale=17452673.57)
    dist_plain = st.johnsonsb
    params = [1.60, 0.49, 474.12, 17452673.57]
    y,x,tr = distro_hist(dist_plain, params, 64)
    return x,y,tr
    
    
#dist, pdf = test1()
#x,y,tr = test2()
#pdf.plot()
    