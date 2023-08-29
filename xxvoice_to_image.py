'''
Recognise speech and then search for images

pip install SpeechRecognition
pip install pyaudio
pip install bing-image-downloader
'''

import speech_recognition as sr
from bing_image_downloader import downloader
import webbrowser

import tkinter as tk
from PIL import Image, ImageTk, ImageOps


# Set up Audio and text recogniser
r = sr.Recognizer()
m = sr.Microphone()

with m as source: r.adjust_for_ambient_noise(source)

image_no = 1
search_phrase = ""

IMAGE_SIZE = 600

def on_button_click():
    global search_phrase

    print("Button clicked!")
    print("Say something!")
    with m as source: audio = r.listen(source)
    print("I heard you...")
    try:
        # recognize speech using Google Speech Recognition
        search_phrase = r.recognize_google(audio)
        print("You said '{}'".format(search_phrase))
        downloader.download(search_phrase, limit=4,  output_dir='dataset', adult_filter_off=False, force_replace=True, timeout=60, verbose=False)

        # Replace image
        # try:
        #     image_path = "./dataset/{}/{}".format(search_phrase,"Image_1.jpg")
        #     image = Image.open(image_path)
        # except FileNotFoundError: 
        #     image_path = "./dataset/{}/{}".format(search_phrase,"Image_1.png")
        #     image = Image.open(image_path)
          
        image = openImage(1)  
        #image = image.resize((300, 300))  # Resize the image to fit the window (adjust the size as needed)
        image = ImageOps.contain(image, (IMAGE_SIZE,IMAGE_SIZE))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

def openImage(image_no):
    try:
        image_path = "./dataset/{}/{}".format(search_phrase,"Image_{}.jpg".format(image_no))
        image = Image.open(image_path)
        return image
    except FileNotFoundError: 
        pass
    try:
        image_path = "./dataset/{}/{}".format(search_phrase,"Image_{}.png".format(image_no))
        image = Image.open(image_path) 
        return image
    except FileNotFoundError: 
        pass
    try:
        image_path = "./dataset/{}/{}".format(search_phrase,"Image_{}.gif".format(image_no))
        image = Image.open(image_path) 
        return image
    except FileNotFoundError: 
        pass

def on_next_button_click():
    global image_no

    image_no+=1
    if image_no > 4:
        image_no = 1

    # Replace image
    # try:
    #     image_path = "./dataset/{}/{}".format(search_phrase,"Image_{}.jpg".format(image_no))
    #     image = Image.open(image_path)
    # except FileNotFoundError: 
    #     image_path = "./dataset/{}/{}".format(search_phrase,"Image_{}.png".format(image_no))
    #     image = Image.open(image_path)   
    image = openImage(image_no)     
    #image = image.resize((300, 300))  # Resize the image to fit the window (adjust the size as needed)
    image = ImageOps.contain(image, (IMAGE_SIZE,IMAGE_SIZE))
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo    



# Create the main window
root = tk.Tk()
root.title("Button and Image Example")

# Load the image
image_path = "banner.png"
image = Image.open(image_path)
#image = image.resize((300, 300))  # Resize the image to fit the window (adjust the size as needed)
image = ImageOps.contain(image, (IMAGE_SIZE,IMAGE_SIZE))
photo = ImageTk.PhotoImage(image)

# Create the image label and add the image to it
image_label = tk.Label(root, image=photo)
image_label.pack()

# Create the button
button = tk.Button(root, text="Click Me!", command=on_button_click)
button.pack()

# Create the button
button_next = tk.Button(root, text="Next", command=on_next_button_click)
button_next.pack()


# Start the Tkinter main loop
root.mainloop()



"""
try:
    print("Please wait...")
    with m as source: r.adjust_for_ambient_noise(source)
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("I heard you...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            print("You said '{}'".format(value))
            downloader.download(value, limit=4,  output_dir='dataset', adult_filter_off=False, force_replace=False, timeout=60, verbose=True)
            webbrowser.open("./{}/{}".format(value,"Image_1"))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass    


"""