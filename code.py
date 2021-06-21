import json
from adafruit_magtag.magtag import MagTag
from secrets import secrets
from time import sleep
from gc import collect
import alarm
from alarm.pin import PinAlarm
import time
import board
import re
import displayio
# from adafruit_epd.epd import Adafruit_EPD
# from adafruit_epd.il0373 import Adafruit_IL0373

#print(dir(displayio.EPaperDisplay))
#print(dir(board.EPD_RESET))

k_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
flux_url = "https://services.swpc.noaa.gov/products/10cm-flux-30-day.json"
alerts_url = "https://services.swpc.noaa.gov/products/alerts.json"
a_url = "https://services.swpc.noaa.gov/json/predicted_fredericksburg_a_index.json"
sunspot_url = "http://www.sidc.be/silso/DATA/EISN/EISN_current.txt"
time_url = "http://worldclockapi.com/api/json/utc/now"


def deep_sleep():
    last_line = "Refresh                              Events"
    magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(1, 121),
        is_data=False,
        text=last_line

    )

    alarms.append(alarm.time.TimeAlarm(monotonic_time = time.monotonic() + 14400))
    alarm.exit_and_deep_sleep_until_alarms(*alarms)


def clear_display():
    magtag.graphics.set_background(0xFFFFFF)
    #time.sleep(1.0)
    #magtag.graphics.display.refresh()

line_nu = 0
def disp_event(alltxt, which, text_color=0x000000):
    global line_nu
    clear_display()

    if which < 0:
        which = len(alltxt) -1
    elif which >= len(alltxt):
        which = 0

    #bitmap = displayio.Bitmap(board.DISPLAY.width, board.DISPLAY.height, 2)
    #palette = displayio.Palette(2)
    #palette[0] = 0xffffff
    #palette[1] = 0x000000
    #tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    #group = displayio.Group()
    #group.append(tile_grid)
    print("mt.dis", dir(magtag.graphics.display))
    print("mt.gr", dir(magtag.graphics))

    foo = re.sub("\s+",' ', alltxt[which]['message'])
    foo = re.sub("NOAA Space Weather Scale descriptions can be found at www.swpc.noaa.gov/noaa", '', foo)
    foo = re.sub("Space Weather Message Code", "MSG CDE", foo)
    foo = re.sub("Serial Number", "Ser Nu", foo)
    foo = re.sub("Issue Time", "Tm", foo)
    foo = re.sub("Cancel Serial Number", "C Ser Nu", foo)
    foo = re.sub("Original Issue Time", "Orig Tm", foo)


    #print("SUB",foo, len(foo))

    magtag.add_text(
        text_position=(5, 50),
        is_data=False,
        text_wrap=50,
        text_maxlen=len(foo),
        line_spacing=0.8,
        text_color=text_color

    )
    magtag.set_text(foo + '   ', index = 0, auto_refresh=False)

    last_line = "Exit     Previous          Next"
    magtag.add_text(
        text_position=(1, 121),
        is_data=False,
        text_color=text_color,
        text = last_line
    )
    return which + 1

def show_events():
    alerts_url = "https://services.swpc.noaa.gov/products/alerts.json"
    magtag.url = alerts_url
    alerts_value = json.loads(magtag.fetch())

    which = disp_event(alerts_value, 0)

    while True:
        time.sleep(0.2)
        if magtag.peripherals.button_a_pressed:
            disp_event(alerts_value, which - 1, text_color=0xFFFFFF)
            magtag.set_text(' ', index=0, auto_refresh=False)
            magtag.set_text(' ', index=1)
            magtag._text = []
            show_weather()
            deep_sleep()
            return
        elif magtag.peripherals.button_b_pressed:
            #disp_event(alerts_value, which - 1, text_color=0xFFFFFF)
            which = disp_event(alerts_value, which - 2)
        elif magtag.peripherals.button_c_pressed:
            #disp_event(alerts_value, which - 1 , text_color=0xFFFFFF)
            which = disp_event(alerts_value, which)

def flashit(fillset):
    for ii in range(0,4):
        magtag.peripherals.neopixels.fill(fillset)
        time.sleep(.25)
        magtag.peripherals.neopixels.fill((0,0,0))
        time.sleep(.25)


def show_weather():
    magtag.url = time_url
    time_value = json.loads(magtag.fetch())['currentDateTime']

    magtag.url = k_url
    k_value = json.loads(magtag.fetch())[-1:][0][1]

    magtag.url = flux_url
    flux_value = json.loads(magtag.fetch())[-1:][0][1]

    magtag.url = a_url
    a_value = str(json.loads(magtag.fetch())[0]['afred_1_day'])

    magtag.url = sunspot_url
    sunspot_value = magtag.fetch().split()[-4]

    magtag.add_text(
        text_position=(5, 10),
        is_data=False

    )
    magtag.set_text("UTC:" + str(time_value), index = 0, auto_refresh=False)

    data_str = "K Index:%s  A Index:%s  Flux:%s  Sun Spot:%s" %(k_value, a_value, flux_value, sunspot_value)

    magtag.add_text(
        text_position=(5, 25),
        is_data=False
    )
    magtag.set_text(data_str, index = 1, auto_refresh=False)

    if int(flux_value) > 74 and int(k_value) <=5:
        magtag.add_text(
            text_position=(5, 56),
            is_data=False,
            text_scale=2
            )


        flashit((0,128,0))
        magtag.set_text("W00T! Get on the radio", index=2, auto_refresh=False)
    else:
        magtag.add_text(
            text_position=(20, 56),
            is_data=False,
            text_scale=2
        )

        flashit((128,0,0))
        magtag.set_text("sigh, get work done", index=2, auto_refresh=False)


buttons = [board.BUTTON_A, board.BUTTON_D]
alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

magtag = MagTag()

if magtag.peripherals.battery < 2.9:
    for ii in range(0, 10) :
        magtag.peripherals.play_tone(3000, 1.0)
        sleep(1)
    magtag.add_text(
        text_position=(40, 60),
        is_data=False,
        text_scale=3,
        text = "BATTERY LOW"
    )
    magtag.exit_and_deep_sleep(7200)

if isinstance(alarm.wake_alarm, PinAlarm) and alarm.wake_alarm.pin == board.BUTTON_D:
    show_events()
else:
    show_weather()

deep_sleep()
