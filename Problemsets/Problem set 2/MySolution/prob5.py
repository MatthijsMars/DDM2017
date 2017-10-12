import numpy as np
import matplotlib.pyplot as plt
#from astroML.datasets import fetch_sdss_sspp
#from astroML.plotting import hist
#import seaborn as sns
#import pandas as pd
import sys
import cPickle
#from sklearn.linear_model import Ridge, Lasso
from astroML.linear_model import  LinearRegression
import pdb
import emcee
import corner

def pickle_to_file(data, fname):
    """Save a variable simply to a file"""
    try:
        fh = open(fname, 'w')
        cPickle.dump(data, fh)
        fh.close()
    except:
        print "Pickling failed!", sys.exc_info()[0]

def pickle_from_file(fname):
    """Restore a variable saved with pickle_to_file"""
    try:
        fh = open(fname, 'r')
        data = cPickle.load(fh)
        fh.close()
    except:
        print "Loading pickled data failed!", sys.exc_info()[0]
        data = None

    return data
    
    
d = pickle_from_file('points_example1.pkl')

x = d['x']
yobs = d['y']
sigma = d['sigma']


for k in [1,5,9]:
    y = np.empty(len(yobs))
    for i in range(len(x)):
        dist = ( (x-x[i])**2 + (yobs-yobs[i])**2)**0.5
        nb = np.argsort(dist)[1:k+1]
        y[i] = np.mean(yobs[nb])

    plt.plot(x,yobs,'.')
    plt.plot(x,y)
    plt.show()
            
    
    
