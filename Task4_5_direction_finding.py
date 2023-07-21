import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from Task3_array_transfer_vector import full_array_vector
import scipy.fft
import scipy.optimize as optimize

file_names = ["measurements1","measurements2","measurements3"]
sampleRate, audioBuffer = scipy.io.wavfile.read("data/" + file_names[1] + ".wav")

### TASK 4

# Take one second from the middle of the audio.
audioBuffer_slice = audioBuffer[5*sampleRate:6*sampleRate]
# Do FFT for all 16 Elements
fft_result = np.array([np.fft.rfft(audioBuffer_slice[:,i],8192) for i in range(16)]).T
print(audioBuffer_slice[:,0].shape)
# Calculate Frequencies of the FFT to later calculate the wavelength
fft_freqs = np.abs(np.fft.rfftfreq(8192)*48000)

# NBDF Algorithm: Beamformer, returns negative absolute for optimization
def beamformer(uv,wavelength,R):
    u,v = uv
    a = full_array_vector(u,v,wavelength)
    BF = a.H @ R @ a
    return np.abs(BF)

# Broadband Beamformer: just summing up the BF values for slected Frequency Bins (more bins was to slow)
def broadband_beamformer(uv):
    result = 0
    u,v = uv
    for i in range(1,4097,100):
        print(fft_freqs[i])
        # Remove all Frequency values that are not in the selected bin
        Z_freq = np.zeros((4097, 16),np.complex128)
        Z_freq[i,:] = fft_result[i,:]
        # Convert back to time domain
        Z = np.asmatrix(np.array([np.fft.irfft(Z_freq[:,j].T,8192) for j in range(16)]))
        # Calculate Covariance Matrix
        R = (Z @ Z.H) / 48000
        # Use Beamformer to determine power in uv direction and sum up the result for all frequencies
        result = result + beamformer(uv,343/fft_freqs[i],R)
        #result = result + np.abs(full_array_vector(u,v,fft_freqs[i]).H @ fft_result[i,:])**2
    return result

# Plot the Direction Finding Function for all uv values
if True:   
    fig, ax = plt.subplots(1)
    x = np.arange(-1,1,0.1)
    y = np.arange(-1,1,0.1)
    strength = np.zeros((len(x),len(y)),dtype=float)
    for i in range(len(x)):
        for j in range(len(y)):
            strength[i,j] = broadband_beamformer((x[i],y[j]))
            print(i,j)

    
    cs = ax.contourf(x,y,strength,cmap='coolwarm')

    fig.colorbar(cs)
    plt.savefig('Plots/Broadband_DFF.pdf')
    plt.show()

# TASK 5; The optimization does not work, as there is something wrong with the direction finding function.
# The algorith terminates at (-1,1) which is outside of the unit circle.

# Convert UV to AZ El Angles
def uvtoazel(uv):
    u,v = uv
    return(np.arctan(u/np.sqrt(1-u**2-v**2)),np.arcsin(v))
# Optimization
if not True:
    result = optimize.basinhopping(broadband_beamformer,(0.2,-0.1),minimizer_kwargs={'method':'Nelder-Mead', 'bounds':((-0.8,1),(-0.8,1))})
    print (result)
    print('AZ,EL:' + str(np.degrees(uvtoazel(result.x))))


    

