import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from Task3_array_transfer_vector import full_array_vector
import scipy.fft
import scipy.optimize as optimize
import sounddevice as sd

### TASK 6

# Calculates the weigth vectors of the beamformer for given u,v coordinates
def calculate_beam_wheights(uv1,uv2,wavelength):
    u1,v1 = uv1
    u2,v2 = uv2
    avec1 = full_array_vector(u1,v1,wavelength)
    avec2 = full_array_vector(u2,v2,wavelength)
    bvec1 = np.asmatrix((np.identity(16)-(avec2 @ np.linalg.pinv(avec2.H @ avec2) @ avec2.H)) @ avec1)
    bvec2 = np.asmatrix((np.identity(16)-(avec1 @ np.linalg.pinv(avec1.H @ avec1)@ avec2.H)) @ avec2)
    cvec1 = bvec1 / np.emath.sqrt(bvec1.H @ bvec1)
    cvec2 = bvec2 / np.emath.sqrt(bvec2.H @ bvec2)
    return cvec1

if __name__ == '__main__':
    if True:
        x = np.arange(-1,1,0.05)
        y = np.arange(-1,1,0.05)
        fig, ax = plt.subplots(1)
        Z = np.zeros((len(x),len(y)),dtype=float)
        for i in range(len(x)):
            for j in range(len(y)):
                print(i,j)
                Z[i,j] = np.abs(calculate_beam_wheights((-0.5,-0.7),(0.7,0.5),9000).H @ full_array_vector(x[i],y[j],9000))
        
        # Convert to Db scale
        maximum = np.max(Z)
        Z = (Z / maximum).T
        with np.nditer(Z, op_flags=['readwrite']) as it:
            for value in it:
                value[...] = 10 * np.log10(value)
        
        # Plot spatial filter
        levels = np.linspace(-40, 0, 40+1)
        cs = ax.contourf(x,y,Z,levels = levels,cmap = 'coolwarm')
        circ = pat.Circle((0, 0), 1, transform=ax.transData)
        for coll in cs.collections:
            coll.set_clip_path(circ)
        cbar = fig.colorbar(cs)
        cbar.set_label('dB')
        ax.set_xlabel('u')
        ax.set_ylabel('v')
        ax.set_title('Spatial Filter u=-0.5 v=-0.7, Null at (0.7,0.5)')
        plt.savefig('Plots/Spatial_Filter.pdf')
        plt.show()
    
    ### TASK 7

    # Load signal
    file_names = ["measurements1","measurements2","measurements3"]
    sampleRate, audioBuffer = scipy.io.wavfile.read("data/" + file_names[2] + ".wav")

    # Transform signal to Frequency domain
    fft_result = np.fft.fft(audioBuffer,8192,axis=0)
    print(fft_result)
    fft_freqs = np.fft.fftfreq(8192)/48000
    # Apply a filter for each Frequency
    for i,freq in enumerate(fft_freqs):
        if freq != 0:
            fft_result = fft_result * np.fft.fft(calculate_beam_wheights((-0.5,-0.7),(0.7,0.5),freq),8192).T
    # Transform back to time domain
    filtered_signal = np.fft.ifft(fft_result,len(audioBuffer), axis = 0)
    scaled = np.float32(np.abs(filtered_signal[:,0] / np.max(np.abs(filtered_signal[:,0]))))
    scipy.io.wavfile.write('test.wav', sampleRate, scaled)



