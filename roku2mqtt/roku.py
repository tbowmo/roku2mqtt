"""Example script for using the Emulated Roku api."""
import socket
import logging
import logging.config
import os
from roku2mqtt.mqttcmdhandler import MQTTCommandHandler
import signal
import sys
from os import path
import json

__version__ = __VERSION__ = "0.1.0"

def parse_args(argv = None):
    import argparse
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    parser = argparse.ArgumentParser(prog='roku2mqtt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Roku emulator\n\nEmulates a roku box, and publishes keystrokes on mqtt,\nthis is particular usefull in conjunction with a\nharmony hub based remote control', 
        epilog='find the project at: https://github.com/tbowmo/roku2mqtt'
        )
    parser.add_argument('-p', '--mqttport', action="store", default=1883, type=int, help="Port number for mqtt broker")
    parser.add_argument('-r', '--mqttroot', action="store", default="roku", help="Root topic for mqtt publish")
    parser.add_argument('-H', '--mqtthost', action="store", default="127.0.0.1", help="Hostname / ip address for mqtt broker")
    parser.add_argument('-l', '--logfile', action="store", default=None, help="Log to filename")
    parser.add_argument('-d', '--debug', action="store_const", dest="log", const=logging.DEBUG, help="loglevel debug")
    parser.add_argument('-v', '--verbose', action="store_const", dest="log", const=logging.INFO, help="loglevel info")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__VERSION__))
    parser.add_argument('-P', '--listen', action='store', default="{0}:8080".format(ip), help="IP address and port for roku api, in the form of 127.0.0.1:8080")
    parser.add_argument('-u', '--usn', action='store', default="roku2mqtt", help="Roku usn")
    parser.add_argument('--mqttuser', action='store', default=None, help='User for mqtt connection')
    parser.add_argument('--mqttpass', action='store', default=None, help='Password for mqtt connection')
    return parser.parse_args(argv)

def setup_logging(
        file = None, 
        level=logging.WARNING
    ):
    if (path.isfile('./logsetup.json')):
        with open('./logsetup.json', 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    elif (file != None):
        logging.basicConfig(level=level,
                            filename=file,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')
    else:
        logging.basicConfig(level=level,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')


def main():
    import asyncio
    import emulated_roku

    args = parse_args()

    setup_logging(args.logfile, args.log)

    ip, separator, port = args.listen.rpartition(':')
    assert separator

    def signal_handler(sig, frame):
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    async def init(loop):
        roku_api = emulated_roku.EmulatedRokuServer(
            loop, MQTTCommandHandler(
                args.mqtthost,
                args.mqttport,
                args.mqttroot
            ),
            roku_usn = args.usn, 
            host_ip = ip, 
            listen_port = int(port)
        )
        await roku_api.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))

    loop.run_forever()
