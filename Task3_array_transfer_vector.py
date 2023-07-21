import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

### TASK 3

frequency = 9000
c = 343
wavelength = c/(frequency)

# Save Element positions
position1 = np.array([-1.808672048, -2.390435735, -0.440114335
])/100
position2 = np.array([3.398238294,	2.163172776,-2.385025347])/100
position3 = np.array([-5.648426012, 6.876657062,3.928439637])/100
position4 = np.array([-1.789396167  ,-9.256527523 ,   -1.255040771
])/100
position5 = np.array([5.75212894	,3.134840863,	4.559771317
])/100
position6 = np.array([-2.467884361,	-4.962513183,	-6.543077688
])/100
position7 = np.array([4.058171026,	-4.927203702,	2.83438586
])/100
position8 = np.array([-4.68404447,	3.996906221,	-6.812903483
])/100
position9 = np.array([-7.206212425,	0.592588855	,-0.005436826
])/100
position10 = np.array([-5.375639283,	-3.333048831,	6.708612872
])/100
position11 = np.array([0.729555422,	8.731451758,	0.717324222
])/100
position12 = np.array([-2.037436989,	2.156257804,	4.846113769
])/100
position13 = np.array([7.092489188,	-4.499725546,	-3.317171139
])/100
position14 = np.array([-7.178604963, -5.793574952,	-1.598153175
])/100
position15 = np.array([-0.674630675,	-7.188444452,	6.603815916
])/100
position16 = np.array([0.333405145,	7.047787104,	-5.119988521
])/100

positions = [position1,position2,position3,position4,position5,position6,position7,position8,position9,position10,position11,position12,position13,position14,position15,position16]

# Calculate a(u) for one Element
def array_transfer_vector( u, v, position, wavelength):
    a_u = np.exp(((1j*(2*np.pi))/wavelength)*(position[0]*u + position[1] * v + position[2] * np.emath.sqrt(1-u**2-v**2)))
    return a_u
# Calculate the full Array Transfer Vector with all Elements
def full_array_vector(u,v,wavelength):
    return np.asmatrix(np.array([array_transfer_vector(u,v,position,wavelength) for position in positions ])).T

if __name__ == '__main__':
    x = np.arange(-1,1,0.01)
    y = np.arange(-1,1,0.01)
    X,Y = np.meshgrid(x, y)
    fig, ax = plt.subplots(4,4)

    # Plot a(u) for all Elements
    for i in range(len(positions)):
        Z = array_transfer_vector(X,Y,positions[i], wavelength)
        cs = ax[i // 4][ i % 4].contourf(X,Y,np.angle(Z))
        circ = pat.Circle((0, 0), 1, transform=ax[i // 4][i % 4].transData)
        for coll in cs.collections:
            coll.set_clip_path(circ)
        ax[i // 4][ i % 4].set_title(i+1)

    fig.tight_layout()
    fig.colorbar(cs, ax=ax.ravel().tolist())
    plt.savefig('Plots/array_tranfer_vector.pdf')
    plt.show()





