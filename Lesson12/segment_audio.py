from pydub import AudioSegment
import os

if not os.path.exists("car"):
    os.makedirs("car")    

count=1
for i in range(1,1000,15):
    t1 = i * 1000 #Works in milliseconds
    t2 = (i+15) * 1000
    newAudio = AudioSegment.from_wav("car.wav")
    newAudio = newAudio[t1:t2]
    newAudio.export('car/'+str(count)+'.wav', format="wav") #Exports to a wav file in the current path.
    print(count)
    count+=1