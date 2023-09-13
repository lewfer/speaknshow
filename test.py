'''
Test display
'''

import speech_recognition as sr
from bing_image_downloader import downloader
import webbrowser
from display_image import *
from time import sleep
import os
import network

from subprocess import check_output, run
import os

# Buttons on Adafruit display
from gpiozero import Button
b1 = Button(27)
b2 = Button(23)
b3 = Button(22)
b4 = Button(17)

r = None
m = None

running = True

draw,image,width,height = getDrawSurface()
draw.text((0, 0), "Ready", font=font, fill=(255, 255, 0))  
menuText(draw, width, 3, "Launch")  
menuText(draw, width, 2, "Listen")     
menuText(draw, width, 1, "1. Exit menu")    
disp.image(image)

def showLongString(ex):
    draw,image,width,height = getDrawSurface()
    draw.text((0, 0), ex[:20], font=font, fill=(255, 255, 0))  
    draw.text((0, 30), ex[20:40], font=font, fill=(255, 255, 0))  
    draw.text((0, 60), ex[40:60], font=font, fill=(255, 255, 0))  
    draw.text((0, 90), ex[60:], font=font, fill=(255, 255, 0))    
    disp.image(image)    


def launch():
    global running

    displayText("Say something")

    fout = open("/home/pi/voice_to_image_poc/out.txt", "w")
    ferr = open("/home/pi/voice_to_image_poc/err.txt", "w")
    #run(["python3", "/home/pi/voice_to_image_poc/test_recognise.py"], stderr=ferr, stdout=fout) 
    run(["python3", "/home/pi/voice_to_image_poc/voiceimage.py"], stderr=ferr, stdout=fout) 
    fout.close()
    ferr.close()

    running = False

def button1():
    global running 

    try:
        ssid = network.getSSID()
        print(ssid)
    except Exception as e:
        showLongString(str(e))        
        return

    draw,image,width,height = getDrawSurface()
    draw.text((0, 0), "Ready", font=font, fill=(255, 255, 0))  
    draw.text((0, 30), ssid, font=font, fill=(255, 255, 0))
    menuText(draw, width, 1, "1. Exit menu")    
    disp.image(image)
    
    sleep(10)
    running = False


def doit():
    global search_phrase
    global image_path
    global files
    global image_no

    print("doit")

    try:
        # Set up Audio and text recogniser
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source: r.adjust_for_ambient_noise(source)
    except Exception as e:
        showLongString(str(e))       
        return    
    
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


    except sr.UnknownValueError:
        displayText("Oops! Didn't catch that")
        print("Didn't catch that")
    except sr.RequestError as e:
        displayText("Issue with Google")
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print(str(e))
        showLongString(str(e))   


# Set up button handlers
b3.when_pressed = launch
b2.when_pressed = doit
b1.when_pressed = button1

# Loop forever
while running:
    #print( b1.is_pressed)
    sleep(0.1)

draw,image,width,height = getDrawSurface()
draw.text((0, 0), "Done", font=font, fill=(255, 255, 0))  
disp.image(image)