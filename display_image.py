# Code for Adafruit 2.8" display

# Imports
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341

# Buttons on Adafruit display
from gpiozero import Button
b1 = Button(27)
b2 = Button(23)
b3 = Button(22)
b4 = Button(17)

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Load a TTF Font
FONTSIZE = 24
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create display object
disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
def getDrawSurface():
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    return (draw,image,width,height)

# Display text centred on screen
def displayText(text):
    draw,image,width,height = getDrawSurface()

    # Draw Some Text
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (width // 2 - font_width // 2, height // 2 - font_height // 2),
        text,
        font=font,
        fill=(255, 255, 0),
    )

    # Display image.
    disp.image(image)

# Display a list of text on the screen
def displayTextList(textList):
    draw,image,width,height = getDrawSurface()

    pos = 0
    for text in textList:
        drawTextAt(draw, 0, pos, text)
        pos += 30
           
    disp.image(image)

# Draw text at a given position
def drawTextAt(draw, x, y, text):
    (font_width, font_height) = font.getsize(text)
    draw.text((x, y), text, font=font, fill=(255, 255, 0))

# Draw a menu item next to the button at position pos
def menuText(draw, width, pos, text):
    (font_width, font_height) = font.getsize(text)
    draw.text((width-font_width, 210-((pos-1)*60)), text, font=font, fill=(255, 255, 0))

# Display image on screen
def displayImage(image_name):
    
    draw,image,width,height = getDrawSurface()

    image = Image.open(image_name)

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

# Show the menu (which is a list of menu items) and any additional text
def showMenu(menu, additionalText=None):
    draw,image,width,height = getDrawSurface()
   
    # Show menu text
    if menu[0][0] != None:
        menuText(draw, width, 4, menu[0][0]+" >")      
    if menu[1][0] != None:
        menuText(draw, width, 3, menu[1][0]+" >")       
    if menu[2][0] != None:
        menuText(draw, width, 2, menu[2][0]+" >")         
    if menu[3][0] != None:
        menuText(draw, width, 1, menu[3][0]+" >")

    if additionalText != None:
        pos = 0
        for text in additionalText:
            drawTextAt(draw, 0, pos, text)
            pos += 30

    # Set up button handlers
    b4.when_pressed = menu[0][1]
    b3.when_pressed = menu[1][1]
    b2.when_pressed = menu[2][1]
    b1.when_pressed = menu[3][1]
                                  
    disp.image(image)

# Split string into list of chunks of given size
def splitn(string, size):
    result = []

    while len(string)>0:
        if len(string)>size:
            result.append(string[:size])
            string = string[size:]
        else:
            result.append(string)
            string = ""
    return result

# Show a long string split up 
def showLongString(ex, lastLine=None):
    if ex==None:
        splitup = ["Nothing to show"]
    else:
        splitup = splitn(ex, 25)

    if lastLine!=None:
        splitup.append(lastLine)
    displayTextList(splitup)

# Clear the button handlers
def clearMenu():
    # Set up button handlers
    b4.when_pressed = None
    b3.when_pressed = None
    b2.when_pressed = None
    b1.when_pressed = None