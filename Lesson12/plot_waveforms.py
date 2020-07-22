from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from os import walk
import os
if not os.path.exists("carPlots"):
    os.makedirs("carPlots")
car_wavs = []
for (_,_,filenames) in walk('car'):
    car_wavs.extend(filenames)
    break
for car_wav in car_wavs:
    # read audio samples
    input_data = read("car/" + car_wav)
    audio = input_data[1]
    # plot the first 1024 samples
    plt.plot(audio)
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    # set the title
    # plt.title("Sample Wav")
    # display the plot
    plt.savefig("carPlots/" + car_wav.split('.')[0] + '.png')
    # plt.show()
    plt.close('all')