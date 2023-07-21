import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

# Save Data in /data folder
file_names = ["measurements1","measurements2","measurements3"]

### TASK 1,2

for file in file_names:
    figure, axis = plt.subplots(16)
    # Read wav file
    sampleRate, audioBuffer = scipy.io.wavfile.read("data/" + file + ".wav")
    duration = len(audioBuffer)/sampleRate
    time = np.arange(0,duration,1/sampleRate)
    ### TASK 1
    for i in range (0,16):
        axis[i].plot(time,audioBuffer[:,i])
        axis[i].set_title("Channel " + str(i+1))
    figure.tight_layout(pad=0.5)
    plt.savefig('Plots/channels_' +file + '.pdf')
    plt.show()
    ### TASK 2
    plt.specgram(audioBuffer[:,0],Fs=sampleRate,cmap= 'jet')
    plt.colorbar()
    plt.savefig('Plots/spectogram_' +file + '.pdf')
    plt.show()
    

