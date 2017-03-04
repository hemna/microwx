import dht
from machine import Pin, I2C
import network
import ssd1306
from umqtt.simple import MQTTClient
import ujson as json
import time

# global to make writing to the OLED easy
display = None


class Config(object):
    cfg_json = {}

    def __init__(self):

        try:
            with open("config.json") as f:
                self.cfg_json = json.loads(f.read())

            self.client_id = 'esp8266_%s' % self.cfg_json['ID']

        except:
            print("Couldn't read config.json.")
            raise

    def __getattr__(self, key):
        return self.cfg_json[key]


class MQTT(object):
    broker_ip = None
    topic = None
    id = None

    def __init__(self, broker_ip, topic, id):
        self.broker_ip = broker_ip
        self.topic = topic
        self.id = id

        self.client = MQTTClient(self.id, self.broker_ip)
        self.client.connect()

    def send(self, msg):
        """Publish a message to the mqtt broker."""
        self.client.publish('%(topic)s/%(id)s' % {'topic': self.topic,
                                                  'id': self.id},
                            json.dumps(msg))


def display_msg(msg, msg2=None, msg3=None, msg4=None):
    """Show a simple 1 line message."""
    global display

    display.fill(0)
    display.text(msg, 1, 0, 1)
    if msg2:
        display.text(msg2, 1, 20, 1)
    if msg3:
        display.text(msg3, 1, 40, 1)
    if msg4:
        display.text(msg4, 1, 60, 1)

    display.show()


def setup_network(cfg):
    """Make sure we are connected to WiFI."""
    display_msg("Init Network...", msg2="Looking for WiFI",
                msg3=cfg.cfg_json['WIFI_SSID'])

    # wait 2 seconds to see if the network comes up
    time.sleep(2)

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    if ap_if.active():
        ap_if.active(False)

    if not sta_if.isconnected():
        display_msg("Connecting to WiFI..")
        sta_if.active(True)
        sta_if.connect(cfg.cfg_json['WIFI_SSID'], cfg.cfg_json['WIFI_PASSWORD'])
        while not sta_if.isconnected():
            display_msg("Connecting to WiFI...")
        display_msg("Connected to ", msg2=cfg.cfg_json['WIFI_SSID'])
    else:
        display_msg("Connected to ", msg2=cfg.cfg_json['WIFI_SSID'])


def setup():
    global display

    cfg = Config()
    i2c = I2C(sda=Pin(cfg.SDA_PIN), scl=Pin(cfg.SCL_PIN))
    display = ssd1306.SSD1306_I2C(128, 64, i2c,
                                  cfg.I2C_ADDRESS)
    display_msg("Booting...")
    time.sleep(1)
    dht_sensor = dht.DHT11(Pin(cfg.DHT_PIN))

    setup_network(cfg)
    time.sleep(1)

    mqtt = MQTT(cfg.MQTT_BROKER, cfg.MQTT_TOPIC, cfg.ID)
    return (cfg, dht_sensor, mqtt)


def measure_and_show(dht_sensor, index):
    dht_sensor.measure()
    C = dht_sensor.temperature()
    temperature_f = 9.0/5.0 * C + 32
    msg_temp = "Temp: %.2f F" % temperature_f
    humidity = dht_sensor.humidity()
    msg_hum = "Humidity: %s %%" % humidity
    display_msg(str(index), msg2=msg_temp, msg3=msg_hum)
    return temperature_f, humidity


def main():
    cfg, dht_sensor, mqtt = setup()
    display_msg("Start Wx Station")
    time.sleep(1)

    i = 1
    while (True):
        temperature, humidity = measure_and_show(dht_sensor, i)
        info = {'temperature': "%.2f" % temperature,
                'humidity': humidity}
        mqtt.send(info)
        time.sleep(1)
        i += 1

if __name__ == "__main__":
    main()
