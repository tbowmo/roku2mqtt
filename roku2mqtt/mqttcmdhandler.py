import paho.mqtt.publish as publish
from emulated_roku import EmulatedRokuCommandHandler

class MQTTCommandHandler(EmulatedRokuCommandHandler):
    """Emulated Roku command handler."""
    def __init__(self, mqtthost, mqttport, mqttroot):
        self.mqtthost = mqtthost
        self.mqttport = mqttport
        self.root = mqttroot
    def publish(self, event, usn, message):
        topic = '{0}/{1}'.format(self.root, event)
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
