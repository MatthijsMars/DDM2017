import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


t = Table().read('x-vs-y-for-PCA.csv')
#print t

x = t['x'].data
y = t['y'].data

U = ((x - np.mean(x))/np.std(x))
V = ((y - np.mean(y))/np.std(y))

C = np.array([np.sum(U**2), np.sum(U*V),np.sum(V*U),np.sum(V**2)]).reshape((2,2))/len(U)
print C

plt.plot(U,V,'.')
#plt.show()
plt.clf()


eigenvalues, eigenvectors =  np.linalg.eig(C)
ev1, ev2 = zip(*eigenvectors)

print ev1, ev2

Ugrid = (np.linspace(min(U),max(U),100)/ev1[0])
plt.plot(ev1[0]*Ugrid *np.std(x) + np.mean(x), ev1[1]*Ugrid *np.std(y) + np.mean(y), 'r-', label='ev1')
plt.plot(ev2[0]*Ugrid *np.std(x) + np.mean(x), ev2[1]*Ugrid *np.std(y) + np.mean(y), 'b-', label='ev2')
plt.legend()
plt.plot(x,y,'.')
plt.show()

pcs = np.empty((2,len(x)))
for i in range(len(x)):
    pcs[:, i] = np.matmul(eigenvectors.T, np.array([U[i], V[i]]).T)

plt.plot(pcs[0,:], pcs[1,:],'.')
plt.axis(ymin=min(pcs[0,:]), ymax=max(pcs[0,:]))
plt.show()

#pcs[1,:] = 0

x2 = pcs[0,:]*ev1[0] * np.std(x) + np.mean(x)
y2 = pcs[0,:]*ev1[1] * np.std(y) + np.mean(y)

#plt.plot(x,y,'.')
plt.plot(x2,y2,'.')
plt.show()

pca = PCA(whiten=False, n_components=2)
X = np.vstack([x, y]).T
scl = StandardScaler()
Xs = scl.fit_transform(X)
pca.fit(Xs)
ev1_1, ev2_1 = zip(*pca.components_.T)
Xt = pca.fit_transform(Xs)
X3 = pca.inverse_transform(np.array([Xt[:,0], np.zeros(len(Xt[:,0]))]).T)
x3 = scl.inverse_transform( X3)
plt.plot(x3[:,0],x3[:,1],'.')
plt.show()



