"""Example script for using the Emulated Roku api."""

if __name__ == "__main__":
    import socket
    import asyncio
    import logging
    import emulated_roku
    import paho.mqtt.publish as publish
    import os
    
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    servers = []

    DEFAULT_HOST_IP = os.environ['HOST_IP']
    DEFAULT_LISTEN_PORTS = os.environ['HOST_PORT']
    MQTT_HOST = os.environ['MQTT_HOST']
    MQTT_PORT = os.environ['MQTT_PORT']
    MQTT_USERNAME = os.getenv('MQTT_USERNAME',None)
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD',None)
    
    DEFAULT_UPNP_BIND_MULTICAST = True

    class MQTTRokuCommandHandler(emulated_roku.RokuCommandHandler):
        """Emulated Roku command handler."""
        def publish(self, event, usn, message):
            topic = 'roku/'+event
            publish.single(topic, message, hostname = MQTT_HOST, auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD}, port = int(MQTT_PORT))

        def on_keydown(self, roku_usn, key):
            self.publish('keydown', roku_usn, key)
            
        def on_keyup(self, roku_usn, key):
            self.publish('keyup', roku_usn, key)

        def on_keypress(self, roku_usn, key):
            print(roku_usn)
            self.publish('keypress', roku_usn, key)

        def launch(self, roku_usn, app_id):
            self.publish('app', roku_usn, app_id)



    @asyncio.coroutine
    def init(loop):
        handler = MQTTRokuCommandHandler()
        discovery_endpoint, roku_api_endpoint = emulated_roku.make_roku_api(
            loop=loop,
            handler=handler,
            host_ip=DEFAULT_HOST_IP,
            listen_port=DEFAULT_LISTEN_PORTS,
            advertise_ip=DEFAULT_HOST_IP,
            advertise_port=DEFAULT_LISTEN_PORTS,
            bind_multicast=DEFAULT_UPNP_BIND_MULTICAST)  # !Change Host IP!

        discovery_transport, _ = yield from discovery_endpoint
        api_server = yield from roku_api_endpoint

        servers.append(discovery_transport)
        servers.append(api_server)

    loop.run_until_complete(init(loop))

    loop.run_forever()
