import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import pandas as pd

t = Table().read('vizier_votable.vot')

logRe = t['logRe'].data
mu = t['__mu_e'].data
logsigma = t['logsigma'].data

pred = 1.24*logsigma + -0.82/-2.5 * mu

'''
C = np.inf
for i in np.linspace(-10,-6, 100):
    cost =  np.sum((pred + i - logRe )**2)
    if cost < C:
        const = i 
        C = cost
'''
const = -8.34343434343
pred += const

dif = pred-logRe
plt.plot(dif-np.mean(dif),'.')
plt.show()

data = pd.DataFrame(np.vstack([mu,logsigma,logRe]).T)
sns.pairplot(data)
plt.savefig('data.png')

data = pd.DataFrame(np.vstack([mu,logsigma,pred]).T)
sns.pairplot(data)
plt.savefig('pred.png')

pca = PCA(whiten=False, n_components=3)
X = np.vstack([mu,logsigma,logRe]).T
#scl = StandardScaler()
#Xs = scl.fit_transform(X)
pca.fit(X)
ev1,ev2,ev3 = zip(*pca.components_.T)
print ev1/ev1[2]
print ev2/ev2[2]
print ev1, ev2, ev3
print pca.explained_variance_


pca = PCA(whiten=False, n_components=1)
pca.fit(X)
scl = StandardScaler()
Xs = scl.fit_transform(X)
Xt =  scl.inverse_transform(pca.inverse_transform(pca.fit_transform(Xs)))

data = pd.DataFrame(Xt)
sns.pairplot(data)
plt.savefig('pca.png')

print "d_mu", np.mean(np.ediff1d(Xt[:,2])/np.ediff1d(Xt[:,0]))
print "d_logI", np.mean(np.ediff1d(Xt[:,2])/np.ediff1d(Xt[:,0])) * -2.5
print "d_logsigma", np.mean(np.ediff1d(Xt[:,2])/np.ediff1d(Xt[:,1]))

plt.clf()
dif = Xt[:,2]-logRe
plt.plot(dif-np.mean(dif),'.')
plt.show()

# smaller spread: logRe =