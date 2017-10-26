import numpy as np
import matplotlib.pyplot as plt
from astropy.io.votable import parse
from astropy.table import Table
from sklearn.neighbors import KernelDensity as KD
from sklearn.model_selection import KFold 
from astroML.plotting import hist
import cPickle

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
    
    

def cv1(x, bws, model='gaussian', plot=False, n_folds=10):
    """
    This calculates the leave-one-out cross validation. If you set 
    plot to True, then it will show a big grid of the test and training
    samples with the KDE chosen at each step. You might need to modify the 
    code if you want a nicer layout :)
    """

    # Get the number of bandwidths to check and the number of objects
    N_bw = len(bws)
    N = len(x)
    cv_1 = np.zeros(N_bw)
    
    # If plotting is requested, set up the plot region
    if plot:
        fig, axes = plt.subplots(N_bw, int(np.ceil(N/n_folds)), figsize=(15, 8))
        xplot = np.linspace(-3, 8, 1000)

    # Loop over each band-width and calculate the probability of the 
    # test set for this band-width
    for i, bw in enumerate(bws):
    
        # I will do N-fold CV here. This divides X into N_folds
        kf = KFold(N)

        # Initiate - lnP will contain the log likelihood of the test sets
        # and i_k is a counter for the folds that is used for plotting and
        # nothing else..
        lnP = 0.0
        i_k = 0
                                 
        # Loop over each fold
        for train, test in kf.split(x):
            x_train = x[train, :]
            x_test = x[test, :]
            
            # Create the kernel density model for this bandwidth and fit
            # to the training set.
            kde = KD(kernel=model, bandwidth=bw).fit(x_train)
                                 
            # score evaluates the log likelihood of a dataset given the fitted KDE.
            log_prob = kde.score(x_test)
            
            if plot:
                # Show the tries
                ax = axes[i][i_k]

                # Note that the test sample is hard to see here.
                hist(x_train, bins=10, ax=ax, color='red')
                hist(x_test, bins=10, ax=ax, color='blue')
                ax.plot(xplot, np.exp(kde.score_samples(xplot[:, np.newaxis])))
                i_k += 1
            

            lnP += log_prob
            
        # Calculate the average likelihood          
        cv_1[i] = lnP/N
        
    return cv_1
    
    
vot = Table().read('pulsar_masses.vot' )

mass = vot['Mass'].quantity

print 'prob m > 1.8:', float((mass > 1.8).sum())/len(mass)

p1 = float(( (mass > 1.36).astype(int) - (mass > 2.26).astype(int) ).sum())/len(mass)
print 'prob m1:', p1
p2 = float(( (mass > 0.86).astype(int) - (mass > 1.36).astype(int) ).sum())/len(mass)
print 'prob m2:', p2
print 'likelihood of binary:', p1 * p2

bws = np.arange(0.01, 1, 0.01)
x = mass[:,np.newaxis]
bw = bws[np.argmax(np.exp(cv1(x, bws)))]
kde = KD(bandwidth = bw).fit(x)

print np.mean(kde.sample(10)), 'solar mass'

