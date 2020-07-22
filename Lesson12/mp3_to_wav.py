from pydub import AudioSegment
sound = AudioSegment.from_mp3("car.mp3")
sound.export("car.wav", format="wav")
sound = AudioSegment.from_mp3("bike.mp3")
sound.export("bike.wav", format="wav")