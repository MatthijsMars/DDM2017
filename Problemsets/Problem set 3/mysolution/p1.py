import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from sklearn.neighbors import KernelDensity as KD
from sklearn.model_selection import KFold 
from astroML.plotting import hist



t = Table().read('joint-bh-mass-table.csv' )

x = t['MBH'].quantity[:,np.newaxis]
xplot = np.arange(-20,101,0.1)[:,np.newaxis]

bws = list(range(1,8))

for i in bws:
    dist = KD(bandwidth = i).fit(x)
    log_dens = dist.score_samples(xplot)
    plt.plot(xplot[:,0],np.exp(log_dens), label = str(i))

plt.legend()    
#plt.show()
plt.clf()



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

bws = np.arange(1,8+0.01,0.01)
cv = cv1(x,bws, model='gaussian', plot=False, n_folds=3)
plt.plot(bws,np.exp(cv))
plt.show()
print bws[np.argmax(np.exp(cv))]
