'''
Speak'n'Show

Voice to Image device for Raspberry Pi

Recognise speech using Google Speech Recognition and then search Bing for matching images

pip install SpeechRecognition
pip install pyaudio
pip install bing-image-downloader

sudo apt-get install python3-pil
sudo apt install -y python3-pyaudio
sudo apt-get install flac
'''

# Google speech recognition
import speech_recognition as sr

# Bing image downloader
from bing_image_downloader import downloader

from time import sleep
import os
import network

from display_image import *


r = None
m = None

IMAGE_SIZE = 600

# Globals to track downloaded images
image_no = 0
search_phrase = ""
files = []
image_path = ""

# Helper functions
# ----------------------------------------------------------------


# Menu handlers
# ----------------------------------------------------------------
def settings():
    print("settings")
    showMenu(settingsMenu)
    pass

def startup():
    global r, m

    try:
        # Set up Audio and text recogniser
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source: r.adjust_for_ambient_noise(source)
    except Exception as e:
        showLongString(str(e))       
        return        
    
    showMenu(mainMenu)
    
def listen():
    print("listen")
    global search_phrase
    global image_path
    global files
    global image_no

    print("doit")

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

        b4.when_pressed = showImage
        b3.when_pressed = None
        b2.when_pressed = None
        b1.when_pressed = setMainMenu

    except sr.UnknownValueError:
        displayText("Oops! Didn't catch that")
        print("Didn't catch that")
    except sr.RequestError as e:
        displayText("Issue with Google")
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print(str(e))
        showLongString(str(e))   

# Show image and move number to next image
def showImage():
    print("showImage")
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

def configWifi():
    pass

def setMainMenu():
    showMenu(mainMenu)


# Main program
# ----------------------------------------------------------------

splashMenu = [(None,None),
            (None,None),
            (None,None),
            ("Startup", startup)]

mainMenu = [(None,None),
            (None,None),
            ("Settings", settings),
            ("Listen", listen)]

settingsMenu = [(None,None),
                (None,None),
                ("Configure Wifi", configWifi),
                ("Exit menu", setMainMenu)]

showMenu(splashMenu, ["Ready"])

# Loop forever
while True:
    #print( b1.is_pressed)
    sleep(0.1)