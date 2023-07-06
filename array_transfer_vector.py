import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat


frequency = 9000
c = 343
wavelength = c/(frequency)
position1 = np.array([-1.808672048, -2.390435735, -0.440114335
])/100

position2 = np.array([3.398238294,	2.163172776,-2.385025347])/100

position3 = np.array([-5.648426012, 6.876657062,3.928439637])/100
positions = [position1,position2,position3]


def array_transfer_vector( u, v, position):
    a_u = np.exp(((1j*(2*np.pi))/wavelength)*(position[0]*u + position[1] * v + position[2] * np.emath.sqrt(1-u**2-v**2)))
    return a_u


x = np.arange(-1,1,0.01)
y = np.arange(-1,1,0.01)
X,Y = np.meshgrid(x, y)
fig, ax = plt.subplots(3)

for i in range(len(positions)):
    Z = array_transfer_vector(X,Y,positions[i])
    cs = ax[i].contourf(X,Y,np.angle(Z))
    circ = pat.Circle((0, 0), 1, transform=ax[i].transData)
    for coll in cs.collections:
        coll.set_clip_path(circ)

fig.colorbar(cs, ax=ax.ravel().tolist())


plt.show()





