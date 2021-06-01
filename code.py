import json
from adafruit_magtag.magtag import MagTag
from secrets import secrets

magtag = MagTag()

k_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
flux_url = "https://services.swpc.noaa.gov/products/10cm-flux-30-day.json"
alerts_url = "https://services.swpc.noaa.gov/products/alerts.json"
a_url = "https://services.swpc.noaa.gov/json/predicted_fredericksburg_a_index.json"
sunspot_url = "http://www.sidc.be/silso/DATA/EISN/EISN_current.txt"

magtag.url = k_url
k_value = json.loads(magtag.fetch())[-1:][0][1]
print(k_value)

magtag.url = flux_url
flux_value = json.loads(magtag.fetch())[-1:][0][1]
print(flux_value)

# magtag.url = alerts_url
# alerts_value = json.loads(magtag.fetch())
# print(alerts_value)

magtag.url = a_url
a_value = json.loads(magtag.fetch())[0]['afred_1_day']
print(a_value)

magtag.url = sunspot_url
sunspot_value = magtag.fetch().split()[4]
print(sunspot_value)

magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
    text_position=(5, 15),
    is_data=False,
    text = "K Index:" + str(k_value)
)
magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
    text_position=(70, 15),
    is_data=False,
    text = "A Index:" + str(a_value)
)

magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
    text_position=(140, 15),
    is_data=False,
    text = "Flux:" + str(flux_value)

)

magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
    text_position=(200, 15),
    is_data=False,
    text = "Sunspot:" + sunspot_value

)

print("flux ", type(flux_value))
print("k ", type(k_value))

if int(flux_value) > 74 and int(k_value) <=5:
    magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(5, 115),
        is_data=False,
        text_scale=2,
        text = "W00T! Get on the radio"
        )
else:
    magtag.add_text(# text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(20, 110),
        is_data=False,
        text_scale=2,
        text = "sigh, get work done"
        )
magtag.exit_and_deep_sleep(14400)
