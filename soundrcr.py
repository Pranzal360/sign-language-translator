import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())

