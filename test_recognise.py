import speech_recognition as sr
from bing_image_downloader import downloader
import webbrowser
from display_image import *
from time import sleep
import os
import network


import pyaudio

print("=========================")
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
print("audio devices", numdevices)
for i in range(0, numdevices):
    #if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))



m = None
r = None

try:
    # Set up Audio and text recogniser
    r = sr.Recognizer()
    m = sr.Microphone(device_index=4)
    with m as source: r.adjust_for_ambient_noise(source)
except Exception as e:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", e)      
  


# Listen for utterances
print("\n\n\n\n\n\nSay something!")
with m as source: audio = r.listen(source)

# Handle what was said
print("\n\n\n\n\n\nI heard you...")
try:
    # Recognize speech using Google Speech Recognition
    search_phrase = r.recognize_google(audio)
    print("You said '{}'".format(search_phrase))

except sr.UnknownValueError:
    print("Didn't catch that")
except sr.RequestError as e:
    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except Exception as e:
    print(str(e)) 