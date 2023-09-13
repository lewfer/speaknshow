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

# Software version number
version = "1"

lastError = "No error"

# Speech recognition recogniser and microphone
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
def showLongMessageForAWhile(message):
    showLongString(message, "...waiting 5 seconds...")   
    sleep(5)

# Show the main menu
def showMainMenu():
    global lastError

    ssid,lastError = network.getSSID()
    #if err==None:
    showMenu(mainMenu, ["Ready", ssid])
    #else:
    #    showLongString(err)       

# Show the show menu
def showSplashMenu():
    showMenu(splashMenu, ["Speak'n'Show", "V"+version])

# Show the settings menu
def showSettingsMenu():
    print("settings")
    showMenu(settingsMenu)



# Menu handlers
# ----------------------------------------------------------------

# Check the network and start the recogniser
def startup():
    global r, m, lastError

    displayText("Checking network")

    if not network.checkNetwork():
        displayText("No network detected")
        sleep(3)
        showSplashMenu()
        return

    try:
        # Set up Audio and text recogniser
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source: r.adjust_for_ambient_noise(source)

        # Show main menu
        showMainMenu()
    except Exception as e:
        lastError = str(e)
        showLongMessageForAWhile(lastError)  
        showSplashMenu()
        return        
    

# Listen for utterances    
def listen():
    print("listen")
    global search_phrase
    global image_path
    global files
    global image_no
    global lastError

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
        b1.when_pressed = showMainMenu

    except sr.UnknownValueError:
        print("Didn't catch that")
        showLongMessageForAWhile("Oops! Didn't catch that")
        showMainMenu()
    except sr.RequestError as e:
        print("Couldn't request results from Google Speech Recognition service; {0}".format(e))
        showLongMessageForAWhile("Issue with Google")
        showMainMenu()
    except Exception as e:
        lastError = str(e)
        print("Some error", lastError)
        showLongMessageForAWhile(lastError)
        showMainMenu()

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

# Configure wifi from wifi.txt file on USB drive
def configWifi():
    displayText("Please wait...getting config")
    settings = network.getSettings()
    print(settings)

    if type(settings) is str:
        # An error message was returned
        showLongMessageForAWhile(settings)
    else:
        # The ssid and password were returned
        displayTextList(["Setting Wifi to", settings[0], settings[1], "Please wait..."])
        #displayText("Setting " + settings[0] + " " + settings[1])
        network.setWifi(settings[0], settings[1])
        sleep(10)
        displayText("Done")
        sleep(1)

    showMainMenu()

# Show the last error
def showLastError():
    global lastError

    clearMenu()
    showLongMessageForAWhile(lastError)   
    showMainMenu()


def updateSoftware():
    global lastError
    result,lastError = network.updateSoftwareFromGuthub()
    showLongMessageForAWhile(result)   
    showMainMenu()

# Main program
# ----------------------------------------------------------------

splashMenu = [("Startup", startup),
              (None,None),
              (None,None),
              (None,None)
             ]

mainMenu = [(None,None),
            (None,None),
            ("Settings", showSettingsMenu),
            ("Listen", listen)]

settingsMenu = [("Last error", showLastError),
                ("Update software", updateSoftware),
                ("Configure Wifi", configWifi),
                ("Exit menu", showMainMenu)]

showSplashMenu()

# Loop forever
while True:
    #print( b1.is_pressed)
    sleep(0.1)