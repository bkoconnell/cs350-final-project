#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature & Humidity Sensor Pro 
# (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  
# You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import grovepi
from grovepi import *
import math
# import json
import json
# import grove_rgb_lcd, sleep, and isnan
from time import sleep
from math import isnan

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
# threshold for daylight
threshold = 100
grovepi.pinMode(light_sensor,"INPUT")

# set LED's (red = D2 || blue = D3 || green = D4)
red = 2
blue = 3
green = 4
grovepi.pinMode(red,"OUTPUT")
grovepi.pinMode(blue,"OUTPUT")
grovepi.pinMode(green,"OUTPUT")


# Connect the Grove Temperature & Humidity Sensor Pro
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
sensor = 7  # The Sensor goes on digital port 7.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue_sensor = 0    # The Blue colored sensor.

# initialize 'x_axis' variable to track # of data collect points
x_axis = 1

# set sleep variable to 1800 seconds (30min) (determines frequency of data collect / loop iteration)
freq = 1800

# declare json object
data = []

while True:
    try:
        ''' Light Sensor for daylight hours '''
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        # if daylight, proceed
        if resistance < threshold:
            ''' Weather Station Data Collect & JSON dump '''
            # This example uses the blue colored sensor. 
            # The first parameter is the port, the second parameter is the type of sensor.
            [temp,humidity] = grovepi.dht(sensor, blue_sensor)
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                # convert temp from C to F and round to 1 decimal
                tempF = round((temp * 1.8) + 32, 1)
            
                # round humidity to 1 decimal place
                humidity = round(humidity, 1)
                
                # append iteration #, tempF, and humidity to the json object
                data.append([x_axis, tempF, humidity])

                # send data to json file
                with open('data.json', 'w+') as f:
                    json.dump(data, f)
            
                # increment tracker
                x_axis += 1

                ''' Output Visual Using LEDs '''
                if humidity > 80:
                    digitalWrite(red,0)
                    digitalWrite(blue,1)
                    digitalWrite(green,1)
                    print('blue & green')
                elif tempF > 95:
                    digitalWrite(red,1)
                    digitalWrite(blue,0)
                    digitalWrite(green,0)
                    print('red light')
                elif tempF > 85:
                    digitalWrite(red,0)
                    digitalWrite(blue,1)
                    digitalWrite(green,0)
                    print('blue light')
                elif tempF > 60:
                    digitalWrite(red,0)
                    digitalWrite(blue,0)
                    digitalWrite(green,1)
                    print('green light')
                else:
                    print('Temp is colder than 60')                
                

    except (IOError, TypeError) as e:
        # reset the LEDs
        digitalWrite(red,0)
        digitalWrite(blue,0)
        digitalWrite(green,0)        
        print(str(e))


    except KeyboardInterrupt as e:
        # reset the LEDs
        digitalWrite(red,0)
        digitalWrite(blue,0)
        digitalWrite(green,0)
        print(str(e))
        break
        
    ''' Frequency of Data '''
    # wait some time before re-looping
    # (frequency per loop)
    sleep(freq)
