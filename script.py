import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

# Save Data in /data folder
file_names = ["measurements1","measurements2","measurements3"]


for file in file_names:
    figure, axis = plt.subplots(16, 1)
    #Read wav file
    sampleRate, audioBuffer = scipy.io.wavfile.read("data/" + file + ".wav")
    duration = len(audioBuffer)/sampleRate
    time = np.arange(0,duration,1/sampleRate)
    for i in range (0,16):
        axis[i].plot(time,audioBuffer[:,i])
        axis[i].set_title("Channel" + str(i+1))
    plt.show()
    plt.specgram(audioBuffer[:,0],Fs=sampleRate,cmap= 'jet')
    plt.colorbar()
    plt.show()
    scipy.io.wavfile.write("data/channel1_"+ file + ".wav", sampleRate, audioBuffer[:,0])
    

