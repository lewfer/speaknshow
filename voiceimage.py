'''
Voice to Image for Raspberry Pi

Recognise speech using Google Speech Recognition and then search Bing for matching images

pip install SpeechRecognition
pip install pyaudio
pip install bing-image-downloader

sudo apt-get install python3-pil
sudo apt install -y python3-pyaudio
sudo apt-get install flac
'''

import speech_recognition as sr
from bing_image_downloader import downloader
import webbrowser
from display_image import *
from time import sleep
import os

# Buttons on Adafruit display
from gpiozero import Button
b1 = Button(27)
b2 = Button(23)
b3 = Button(22)
b4 = Button(17)

# Set up Audio and text recogniser
r = sr.Recognizer()
m = sr.Microphone()
with m as source: r.adjust_for_ambient_noise(source)

IMAGE_SIZE = 600

# Globals to track downloaded images
image_no = 0
search_phrase = ""
files = []
image_path = ""

def doit():
    global search_phrase
    global image_path
    global files
    global image_no

    # Listen for utterances
    displayText("Say something")
    print("\n\n\n\n\n\nSay something!")
    with m as source: audio = r.listen(source)

    # Handle what was said
    print("\n\n\n\n\n\nI heard you...")
    try:
        # Recognize speech using Google Speech Recognition
        search_phrase = r.recognize_google(audio)
        print("You said '{}'".format(search_phrase))
        displayText(search_phrase)

        # Download matching images from Bing
        downloader.download(search_phrase, limit=4,  output_dir='dataset', adult_filter_off=False, force_replace=True, timeout=60, verbose=True)

        # Remember files
        image_path = "./dataset/"+search_phrase
        files = os.listdir(image_path)
        image_no = 0

        # Display first image
        showImage()

    except sr.UnknownValueError:
        displayText("Oops! Didn't catch that")
        print("Didn't catch that")
    except sr.RequestError as e:
        displayText("Issue with Google")
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

# Show image and move number to next image
def showImage():
    global image_path
    global files
    global image_no

    if (len(files)==0):
        return
    if image_no>=len(files):
        image_no = 0

    # Replace image
    try:
        print(image_path+"/"+files[image_no])
        displayImage(image_path+"/"+files[image_no])  
    except:
        displayText("Could not display image")
    finally:     
        image_no+=1

# Set up button handlers
b1.when_pressed = doit
b4.when_pressed = showImage

# Loop forever
while True:
    #print( b1.is_pressed)
    sleep(0.1)