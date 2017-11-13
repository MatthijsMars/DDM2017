import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import pandas as pd



t = Table().read('xyzw-for-PCA.csv')


x = t['X'].data
y = t['Y'].data
z = t['Z'].data
w = t['W'].data
scl = StandardScaler()
X = np.vstack([x, y, z, w]).T


pca4d = PCA(whiten=False, n_components=4)
Xs = scl.fit_transform(X)
pca4d.fit(Xs)
Xt4d = pca4d.fit_transform(Xs)
x4d = scl.inverse_transform(pca4d.inverse_transform(Xt4d))

print "4d:"
print zip(*pca2d.components_.T)
print pca2d.explained_variance_

data = pd.DataFrame(x4d)
sns.pairplot(data)
plt.savefig('4D.png')

pca2d = PCA(whiten=False, n_components=2)
Xs = scl.fit_transform(X)
pca2d.fit(Xs)
Xt2d = pca2d.fit_transform(Xs)
x2d = scl.inverse_transform(pca2d.inverse_transform(Xt2d))

print "2d scaled:"
print zip(*pca2d.components_.T)
print pca2d.explained_variance_

data = pd.DataFrame(x2d)
sns.pairplot(data)
plt.savefig('2D_scaled.png')

'''
pca4d = PCA(whiten=False, n_components=4)
X = np.vstack([x, y, z, w]).T
pca4d.fit(X)
Xt4d = pca4d.fit_transform(Xs)
x4d = pca4d.inverse_transform(Xt4d)

data = pd.DataFrame(x4d)
sns.pairplot(data)
plt.savefig('3.png')
'''

pca2d = PCA(whiten=False, n_components=2)
pca2d.fit(X)
#print pca2d.expected_values_
Xt2d = pca2d.fit_transform(Xs)
x2d = pca2d.inverse_transform(Xt2d)

print "2d unscaled:"
print zip(*pca2d.components_.T)
print pca2d.explained_variance_

data = pd.DataFrame(x2d)
sns.pairplot(data)
plt.savefig('2D_unscaled.png')

