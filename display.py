#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import subprocess
import re

logging.basicConfig(level=logging.DEBUG)

LOOK_R = '( ⚆_⚆)'
LOOK_L = '(☉_☉ )'
LOOK_R_HAPPY = '( ◕‿◕)'
LOOK_L_HAPPY = '(◕‿◕ )'
SLEEP = '(⇀‿‿↼)'
SLEEP2 = '(≖‿‿≖)'
AWAKE = '(◕‿‿◕)'
BORED = '(-__-)'
INTENSE = '(°▃▃°)'
COOL = '(⌐■_■)'
HAPPY = '(•‿‿•)'
GRATEFUL = '(^‿‿^)'
EXCITED = '(ᵔ◡◡ᵔ)'
MOTIVATED = '(☼‿‿☼)'
DEMOTIVATED = '(≖__≖)'
SMART = '(✜‿‿✜)'
LONELY = '(ب__ب)'
SAD = '(╥☁╥ )'
ANGRY = "(-_-')"
FRIEND = '(♥‿‿♥)'
BROKEN = '(☓‿‿☓)'
DEBUG = '(#__#)'

try:
    p1 = subprocess.Popen("ifconfig wlan0", shell=True, stdout=subprocess.PIPE)
    p1.wait()
    stdo = p1.stdout.read().decode("utf-8")
    Wlan0 = "wlan: " + re.search('inet (.+?) netmask', stdo).group(1)
    logging.info("wlan ip:" + Wlan0)

    p1 = subprocess.Popen("ifconfig usb0", shell=True, stdout=subprocess.PIPE)
    p1.wait()
    stdo = p1.stdout.read().decode("utf-8")
    match = re.search('inet (.+?) netmask', stdo)
    usb0 = "usb: " + match.group(1) if match is not None else None
    if not usb0 is None:
        logging.info("usb ip:" + usb0)

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    # # partial update
    logging.info("show time...")

    time_image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(time_image)

    draw.text((120, 60), 'local time', font = font15, fill = 0)
    draw.text((0, 0), Wlan0, font = font15, fill = 0)

    epd.displayPartBaseImage(epd.getbuffer(time_image))
    epd.init(epd.PART_UPDATE)

    if not usb0 is None:
        draw.text((0, 14), usb0, font = font15, fill = 0)

    while (True):
        draw.rectangle((120, 80, 220, 105), fill = 255)
        draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
