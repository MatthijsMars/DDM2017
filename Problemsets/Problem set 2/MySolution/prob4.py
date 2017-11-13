import numpy as np 
import cPickle
import matplotlib.pyplot as plt 
import sys
from sklearn.linear_model import LinearRegression as LR 



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
    
    
d = pickle_from_file('data-for-poly-test.pkl')

print d
x = d['x']
y = d['y']
sigma = d['sigma_y']
plt.errorbar(x,y, fmt='o', yerr=sigma)
plt.show()


ML = np.empty(0)


n = 3
p = np.empty((n,len(x)))
for i in range(n):
    p[i,:] = x**i

model = LR(fit_intercept=True)
model.fit(x,y,p)

plt.plot(x,model.predict(x))
lnpdf = 0.
for i in range(len(x)):
    lnpdf += (model.predict(x[i])-y[i])**2/sigma_y[i]**2

