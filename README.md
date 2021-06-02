# MagTag Space weather display
A fairly simple Magtag app that grabs Space Weather from NOAA.
![Good Weather](https://github.com/mpechner/sunweather/blob/bac27f5e9f7cc1100982c971dc1584c8c336a01d/goodweather.jpg)
## ToDo
* get some graphic or display space weather alerts.
* flash neo pixels Green for good weather, red for bad.
* Fix events so all nicely formated for display.
* Scroll events use buttons: A text fwd (loop) B next message C previous message D refresh  
* program so it will try both my home wifi and my phone as a hotspot.
## Library requirements
* adafruit_bitmap_font
* adafruit_display_text
* adafruit_fakerequests
* adafruit_io
* adafruit_magtag
* adafruit_requests
* neopixel
* simpleio
## Secrets.py
Do not check in secrets.py.  Just place at the top level of the project with code.py.
```python
secrets = {
   "ssid":"SSID",
    "password":"passwd"
}
```
## Data Sources

Data source to investigate  https://services.swpc.noaa.gov/

K index use: https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json

Flux: https://services.swpc.noaa.gov/products/10cm-flux-30-day.json

Alerts: https://services.swpc.noaa.gov/products/alerts.json

A Index; https://services.swpc.noaa.gov/json/predicted_fredericksburg_a_index.json

sunspot number: http://www.sidc.be/silso/DATA/EISN/EISN_current.txt

## Interpreting the data
Reading https://www.qrparci.org/resource/FDIM81.pdf to gain a bit more knowledge.

* K index 
  * 0-9 published every 3 hours with a 24 window
  * Magnetometers on the earth measure the condition of our magnetic field. The amount of movement (or, “wiggling”) is averaged and reported by NOAA
* A index 
  * 0-20 is a good number
  * 0-400 representing the overall planetary geomagnetic conditions for the UTC day

K index
* 0 0–2 Very Quiet S1–S2 None
* 1 3–5 Quiet S1–S2 None
* 2 6–9 Quiet S1–S2 Very low
* 3 12–19 Unsettled S2–S3 Very low
* 4 22–32 Active S2–S3 Low
* 5 39–56 MINOR storm S4–S6 High
* 6 67–94 MAJOR storm S6–S9 Very high
* 7 111–154 SEVERE storm S9+ Very high
* 8 179–236 SEVERE STORM Blackout Extreme
* 9 300–400 EXTREME storm Blackout Extreme


