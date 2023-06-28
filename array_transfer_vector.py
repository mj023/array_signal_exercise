import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

positions = np.array([[-1.808672048], [-2.390435735], [-0.440114335]
])/100
frequency = 9000

def array_transfer_vector( u, v):
    einheitsvector = np.array([u,v,np.emath.sqrt(1-np.power(u,2)-np.power(v,2))])
    print(einheitsvector)
    a_u = np.exp(1j*2*np.pi*frequency*(einheitsvector @ positions))
    return a_u


x = np.arange(-1,1,0.1)
y = np.arange(-1,1,0.1)
X,Y = np.meshgrid(x, y)

plt.contourf(X, Y, array_transfer_vector(X,Y))





