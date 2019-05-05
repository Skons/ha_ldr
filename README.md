# ha_ldr
Home assistant python script for an LDR ligth sensor

## Home Assistant LDR
This script allowes for reading an LDR photoresistant sensor on a Raspberry pi.

## Usage

```
usage: ha_ldr.py [-h] [-p PIN] [-m MAX] [-l LOOP] [-u URL] [-s SLEEP]
                 [-f LOGFILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -p PIN, --pin PIN     LDR GPIO data pin
  -m MAX, --max-value MAX
                        Max brightness value reported
  -l LOOP, --max-loop LOOP
                        Max number of loops, 0 for indefinate
  -u URL, --url URL     Url to post the value to, if not provided the output
                        is console
  -s SLEEP, --sleep SLEEP
                        Number of seconds to wait for next brightness
                        retreival
  -f LOGFILE, --log-file LOGFILE
                        Log file location
  -v, --verbose         Show verbose logging
```

This script can be used in 2 ways. You can use it as a command line sensor on a Home Assistant system, or you can use it from a headless RPi to Post the brightness value via the API. By default the script will look for GPIO 17 (contact pin 11), but you can  also use GPIO 4 for instance (which is contact pin 7).

### Command line Sensor
```
sensor:
  - platform: command_line
    name: Brightness
    command: "python3 /path/to/ha_ldr.py -l 1"
    # The lower the number reported, the higher the lumen
    unit_of_measurement: "Units"
```

### Headless RPi
Use curl to call the script, you'll need to enable the legacy_api_password. 
```
* * * * * root python3 /path/to/ha_ldr.py -l 5 -s 10 -u "http://homeassistant:8123/api/states/input_number.brightness?api_password=yourapikey" -v -f "/var/log/ha_ldr.log"
```
This will call the script every minute. The script will post the value every 10 seconds for a duration of 50 seconds (5 loops * 10 seconds wait time).

## Links
* How to LDR on RPi: https://pimylifeup.com/raspberry-pi-light-sensor/
