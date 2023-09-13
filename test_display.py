'''
Test display
'''


from display_image import *
from time import sleep

# Buttons on Adafruit display
from gpiozero import Button
b1 = Button(27)
b2 = Button(23)
b3 = Button(22)
b4 = Button(17)

running = True

draw,image,width,height = getDrawSurface()
draw.text((0, 0), "Ready", font=font, fill=(255, 255, 0))  
menuText(draw, width, 1, "1. Exit menu")    
disp.image(image)

def button1():
    global running 
    running = False


# Set up button handlers
b1.when_pressed = button1

# Loop forever
while running:
    #print( b1.is_pressed)
    sleep(0.1)

draw,image,width,height = getDrawSurface()
draw.text((0, 0), "Done", font=font, fill=(255, 255, 0))  
disp.image(image)