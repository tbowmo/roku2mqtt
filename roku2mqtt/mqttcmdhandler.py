""" Key handler for emulated roku, this publishes the keypresses to MQTT """
from paho.mqtt import publish
from emulated_roku import EmulatedRokuCommandHandler

class MQTTCommandHandler(EmulatedRokuCommandHandler):
    """Emulated Roku command handler."""
    #pylint: disable=too-many-arguments
    def __init__(self, mqtthost, mqttport, mqttroot, mqttuser=None, mqttpass=None):
        self.mqtthost = mqtthost
        self.mqttport = mqttport
        self.root = mqttroot
        self.mqttuser = mqttuser
        self.mqttpass = mqttpass

    def publish(self, event, _usn, message):
        topic = f'{self.root}/{event}'
        if (self.mqttuser is not None) and (self.mqttpass is not None):
            auth = auth={'username':self.mqttuser, 'password':self.mqttpass}
            publish.single(
                topic,
                message,
                hostname = self.mqtthost,
                port = self.mqttport,
                auth=auth
                )
        else:
            publish.single(topic, message, hostname = self.mqtthost, port = self.mqttport)

    def on_keydown(self, roku_usn, key):
        self.publish('keydown', roku_usn, key)

    def on_keyup(self, roku_usn, key):
        self.publish('keyup', roku_usn, key)

    def on_keypress(self, roku_usn, key):
        print(roku_usn)
        self.publish('keypress', roku_usn, key)

    def launch(self, roku_usn, app_id):
        self.publish('app', roku_usn, app_id)
