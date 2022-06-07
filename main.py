import ssd1306_driver
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import cv2
import gphotos
from datetime import datetime
import RPi.GPIO as GPIO

display = ssd1306_driver.SSD1306_128_64(rst=24)
display.begin()
display.clear()
display.display()

width = display.width
height = display.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
font_huge = ImageFont.truetype('DejaVuSans-Bold', size=20)
font_lg = ImageFont.truetype('DejaVuSans-Bold', size=12)
font_sm = ImageFont.truetype('DejaVuSans')

def get_text_center_x(text, font):
    t_width, _ = draw.textsize(text, font=font)
    return (width / 2) - (t_width / 2)

def show_img():
    display.image(image)
    display.display()
    draw.rectangle([(0,0),(width,height)], fill=0)


def show_main_screen():
    draw.text((0,0), "progress-tracker", font=font_lg, fill=255)
    draw.multiline_text((0,15), "Press the button to\ntake a photo", font=font_sm, fill=255)

    lasttime = open('last_pic', "r")
    lasttime_text = "Last: {}".format(lasttime.read())
    draw.text((get_text_center_x(lasttime_text, font_sm), 50), lasttime_text, font=font_sm, fill=255)

    show_img()

def shoot():
    for i in range(5, 0, -1):
        draw.text((0,0), "get ready!", font=font_lg, fill=255)
        radius = 15
        draw.ellipse([(width / 2 - radius, height / 2 - radius + 5), (width / 2 + radius, height / 2 + radius + 5)], fill=0, outline=255, width=2)
        draw.text((get_text_center_x(str(i), font_huge), (height/2 - 5)), str(i), fill=255, font=font_huge)
        display.image(image)
        display.display()
        time.sleep(1)

    draw.rectangle([(0,0),(width,height)], fill=255)
    show_img()
    cam = cv2.VideoCapture(0)
    _, photo = cam.read()
    show_img()
    time.sleep(.5)
    cam.release()
    draw.text((0,0), "uploading...", font=font_lg, fill=255)
    draw.multiline_text((0,15), "Sending to Google Photos", font=font_sm, fill=255)
    show_img()

    img_binary = cv2.imencode('.jpg', photo)[1].tobytes()
    photo_uploader = gphotos.GooglePhotos()
    photo_uploader.add_photo(img_binary)

    draw.text((0,0), "uploaded!", font=font_lg, fill=255)
    draw.multiline_text((0,15), "Sent to Google Photos", font=font_sm, fill=255)
    show_img()
    time.sleep(1)

    with open('last_pic', "w") as f:
        now = datetime.now()
        datestring = now.strftime("%m/%d/%Y %-I:%M %p")
        f.write(datestring)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
show_main_screen()
while True:
    #wait for button
    if GPIO.input(4) == GPIO.HIGH:
        shoot()
        show_main_screen()
    time.sleep(.2)