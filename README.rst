MicroWX Station
---------------

This is a simple python project that runs on an ESP8266 with the
micropython firmware.  This project makes use of the NodeMCU 
ESP8266 hardware connected to an OLED I2C display and a DHT11 temperature
and humidity sensor.  After startup it reads the sensor data from the
DHT11 and sends the temperature and humidity to an MQTT broker over WiFI.


What you need
-------------
* NodeMCU v 1.0 
  https://www.amazon.com/gp/product/B010O1G1ES
  You can see the PINOUT here:
  https://iotbytes.wordpress.com/nodemcu-pinout

* OLED I2C board.  I used
  https://www.amazon.com/gp/product/B01HHOAQ5A

* DHT11 sensor
  https://www.amazon.com/gp/product/B01DKC2GQ0


Setup
-----

* Connect up the NodeMCU to the OLED display.  I used GPIO4 for SDA and GPIO5 
  for SCL
* Connect up the NodeMCU to the DHT11.  I used GPIO10

* Setup your favorite MQTT Broker on your local network.  I used Mosquitto
  https://mosquitto.org/

* Install the micropython firmware on your NodeMCU
  https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

* Edit the config.json and enter your Settings for your WiFI network and your
  MQTT broker.

* Use ampy to install config.json and main.py
  ampy -p /dev/cu.SLAB_USBtoUART put config.json
  ampy -p /dev/cu.SLAB_USBtoUART put main.py
