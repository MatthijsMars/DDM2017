import numpy as np
import matplotlib.pyplot as plt
#from astroML.datasets import fetch_sdss_sspp
#from astroML.plotting import hist
#import seaborn as sns
#import pandas as pd
import sys
import pickle as cPickle
#from sklearn.linear_model import Ridge, Lasso
from astroML.linear_model import  LinearRegression
import pdb
import emcee
import corner

def pickle_to_file(data, fname):
    """Save a variable simply to a file"""
    try:
        fh = open(fname, 'wb')
        cPickle.dump(data, fh)
        fh.close()
    except:
        print( "Pickling failed!", sys.exc_info()[0])

def pickle_from_file(fname):
    """Restore a variable saved with pickle_to_file"""
    try:
        fh = open(fname, 'rb')
        data = cPickle.load(fh)
        fh.close()
    except:
        print ("Loading pickled data failed!", sys.exc_info()[0])
        data = None

    return data
    
    
d = pickle_from_file('points_example1.pkl')

x = d['x']
yobs = d['y']
sigma = d['sigma']

M = x[:, None]
model = LinearRegression(fit_intercept=True)
res = model.fit(M, yobs, sigma)
model.predict(M)
print (res.coef_)


def lnprob(theta, x,yobs,sigma):
    a, b = theta 
    model = b * x + a 
    inv_sigma2 = 1.0/(sigma**2) 
    return -0.5*(np.sum((yobs-model)**2*inv_sigma2))

p_init = res.coef_
ndim, nwalkers = 2, 100
pos = [p_init + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(x,yobs,sigma))
sampler.run_mcmc(pos, 500)


labels = ['a', 'b'] 
chain = sampler.chain 
for i_dim in range(2): 
    plt.subplot(2,1,i_dim+1) 
    plt.ylabel(labels[i_dim]) 
    for i in range(100): 
        plt.plot(chain[i,:,i_dim],color='black', alpha=0.5)
plt.show()

samples = sampler.chain[:, 50:, :].reshape((-1, 2))
fig = corner.corner(samples, labels=["$a$", "$b$"])
plt.show()



