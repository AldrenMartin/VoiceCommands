
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import datetime
import os.path


def speak(text): 
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the temporary audio file after playing


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        
        try: 
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print ("Exception: " + str(e))
            
    return said

text = get_audio()


speak("Hello World")

if "hello" in text:
    speak("hello, how may I assist you.")



if "what is your name" in text:
    speak ("I am here to assist you")

   