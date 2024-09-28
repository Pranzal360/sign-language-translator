import speech_recognition as sr
import openai

def audio_file(path):
    r = sr.Recognizer()

    with sr.AudioFile(path) as source:
        audio = r.listen(source)

    try:
        # Recognize the audio using Google Speech Recognition
        text = r.recognize_google(audio)

        # Use Gemini to enhance the text and provide more context
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can adjust the engine as needed
            prompt=f"Enhance the following text: {text}",
            max_tokens=1024,  # Adjust the maximum token length as desired
            temperature=0.5  # Adjust the temperature for creativity-control
        )

        enhanced_text = response.choices[0].text

        print(enhanced_text)
        return enhanced_text

    except sr.UnknownValueError:
        return 'could not understand'

    except sr.RequestError as e:
        return format(e)
    
PATH = "microphone-results.wav"
audio_file(PATH)