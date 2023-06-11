"""Roku 2 mqtt binding. Emulating a roku, that emits keypresses (pause, play etc) to mqtt"""
import socket
import logging
import logging.config
import signal
import sys
from os import path
import json
import asyncio
import argparse
import emulated_roku
from roku2mqtt.mqttcmdhandler import MQTTCommandHandler

__version__ = __VERSION__ = "0.1.0"

def parse_args(argv = None):
    #pylint: disable=line-too-long
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    parser = argparse.ArgumentParser(prog='roku2mqtt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Roku emulator\n\nEmulates a roku box, and publishes keystrokes on mqtt,\nthis is particular usefull in conjunction with a\nharmony hub based remote control',
        epilog=f'I have detected this machines ip as: {ip_address}'
        )
    parser.add_argument('-r', '--mqttroot', action="store", default="roku", help="Root topic for mqtt publish")
    parser.add_argument('-H', '--mqtthost', action="store", default="127.0.0.1", help="Hostname / ip address for mqtt broker")
    parser.add_argument('--mqttport', action="store", default=1883, type=int, help="Port number for mqtt broker")
    parser.add_argument('--mqttuser', action='store', default=None, help='User for mqtt connection')
    parser.add_argument('--mqttpass', action='store', default=None, help='Password for mqtt connection')
    parser.add_argument('-l', '--logfile', action="store", default=None, help="Log to filename")
    parser.add_argument('-d', '--debug', action="store_const", dest="log", const=logging.DEBUG, help="loglevel debug")
    parser.add_argument('-v', '--verbose', action="store_const", dest="log", const=logging.INFO, help="loglevel info")
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__VERSION__}')
    parser.add_argument('--listen', action='store', default=f"{ip_address}:8080", help=f"IP address and port for roku api, in the form of {ip_address}:8080")
    parser.add_argument('--usn', action='store', default="roku2mqtt", help="Roku usn")
    return parser.parse_args(argv)

def setup_logging(
        file = None,
        level=logging.WARNING
    ):
    if path.isfile('./logsetup.json'):
        with open('./logsetup.json', 'rt', encoding='utf-8') as log_setup:
            config = json.load(log_setup)
        logging.config.dictConfig(config)
    elif file is not None:
        logging.basicConfig(level=level,
                            filename=file,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')
    else:
        logging.basicConfig(level=level,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')


def main():

    args = parse_args()

    setup_logging(args.logfile, args.log)

    ip_address, separator, port = args.listen.rpartition(':')
    assert separator

    def signal_handler(_sig, _frame):
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
            host_ip = ip_address,
            listen_port = int(port)
        )
        await roku_api.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))

    loop.run_forever()
