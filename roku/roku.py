"""Example script for using the Emulated Roku api."""
import socket
import logging
import os
from roku.mqttcmdhandler import MQTTCommandHandler

__version__ = __VERSION__ = "0.1.0"

def parse_args(argv = None):
    import argparse
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    parser = argparse.ArgumentParser(description='Roku emulator')
    parser.add_argument('-p', '--port', action="store", default=1883, type=int, help="MQTT port on host")
    parser.add_argument('-r', '--root', action="store", default="roku", help="MQTT root topic")
    parser.add_argument('-H', '--host', action="store", default="127.0.0.1", help="MQTT Host")
    parser.add_argument('-d', '--debug', action="store_const", dest="log", const=logging.DEBUG, help="loglevel debug")
    parser.add_argument('-v', '--verbose', action="store_const", dest="log", const=logging.INFO, help="loglevel info")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__VERSION__))
    parser.add_argument('-C', '--cleanup', action="store_true", dest="cleanup", help="Cleanup mqtt topic on exit")
    parser.add_argument('-P', '--listen', action='store', default="{0}:8060".format(ip), help="Listen port")
    
    return parser.parse_args(argv)

def main():
    import asyncio
    import emulated_roku


    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    servers = []
    ip, separator, port = args.listen.rpartition(':')
    assert separator
    DEFAULT_HOST_IP = ip
    DEFAULT_LISTEN_PORTS = port
    MQTT_HOST = args.host
    MQTT_PORT = args.port
    
    DEFAULT_UPNP_BIND_MULTICAST = True

    async def init(loop):
        roku_api = emulated_roku.EmulatedRokuServer(
            loop, MQTTCommandHandler(
                args.host,
                args.port,
                args.root
            ),
            "roku_mqtt", ip, 8060
        )
        await roku_api.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))

    loop.run_forever()
