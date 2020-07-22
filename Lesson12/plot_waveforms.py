from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from os import walk
import os
if not os.path.exists("bikePlots"):
    os.makedirs("bikePlots")
bike_wavs = []
for (_,_,filenames) in walk('bike'):
    bike_wavs.extend(filenames)
    break
for bike_wav in bike_wavs:
    # read audio samples
    input_data = read("bike/" + bike_wav)
    audio = input_data[1]
    # plot the first 1024 samples
    plt.plot(audio)
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    # set the title
    # plt.title("Sample Wav")
    # display the plot
    plt.savefig("bikePlots/" + bike_wav.split('.')[0] + '.png')
    # plt.show()
    plt.close('all')