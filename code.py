import json
from adafruit_magtag.magtag import MagTag
from secrets import secrets
from time import sleep
from gc import collect
import alarm
import time
import board

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
        text = last_line
    )
    alarms.append(alarm.time.TimeAlarm(monotonic_time = time.monotonic() + 14400))
    alarm.exit_and_deep_sleep_until_alarms(*alarms)


def show_events():
    alerts_url = "https://services.swpc.noaa.gov/products/alerts.json"
    magtag.url = alerts_url
    alerts_value = json.loads(magtag.fetch())[0]
    print(alerts_value)

    magtag.add_text(
        text_position=(5, 5),
        is_data=False,
        text_wrap=50,
        line_spacing=0.75,
        text=alerts_value
    )


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
    sunspot_value = magtag.fetch().split()[4]

    magtag.add_text(
        text_position=(5, 10),
        is_data=False,
        text="UTC:" + str(time_value)
    )

    data_str = "K Index:%s  A Index:%s  Flux:%s  Sun Spot:%s" %(k_value, a_value, flux_value, sunspot_value)

    magtag.add_text(
        text_position=(5, 25),
        is_data=False,
        text=data_str
    )

    if int(flux_value) > 74 and int(k_value) <=5:
        magtag.add_text(
            text_position=(5, 56),
            is_data=False,
            text_scale=2,
            text = "W00T! Get on the radio"
            )
    else:
        magtag.add_text(
            text_position=(20, 56),
            is_data=False,
            text_scale=2,
            text = "sigh, get work done"
        )


buttons = [board.BUTTON_A, board.BUTTON_D]
alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

magtag = MagTag()

if magtag.peripherals.battery < 3.3:
    for ii in range(0, 10) :
        magtag.peripherals.play_tone(3000, 1.0)
        sleep(1)
    magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(40, 60),
        is_data=False,
        text_scale=3,
        text = "BATTERY LOW"
    )
    magtag.exit_and_deep_sleep(7200)

if alarm.wake_alarm and alarm.wake_alarm.pin == board.BUTTON_D:
    show_events()
else:
    show_weather()

deep_sleep()
