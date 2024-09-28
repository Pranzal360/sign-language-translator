import speech_recognition as sr

def audio_file(path):
    r = sr.Recognizer()

    with sr.AudioFile(path) as source:
        audio= r.listen(source)

    try :
        print(r.recognize_google(audio))
        return(r.recognize_google(audio))
        # delete the temp file after use


    except sr.UnknownValueError:
        return('could not understand')

    except sr.RequestError as e:
        return(format(e)) 
    