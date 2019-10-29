Roku2Mqtt
===

Python program to emulate a roku device, which sends keypresses on mqtt

These keypresses can then be used in mqtt flows, to control other things.

Installation
===

Starting python script with virtual-environment
-----------------------------------------------

First ensure that you have at least python3.6 and venv installed, then create a new virtual environment for your python script:

```shell
$ python3 -m venv ~/roku_dummy
$ source ~/roku_dummy/bin/activate
cd ~/roku_dummy
$ pip install --no-cache-dir -r requirements.txt
```

You are now ready to start the script with

`python -m roku <options>`

Starting with systemd
---
Start by following the description above with virtual-environment

Then create a file named roku.service in /etc/systemd/system, with the following content (update paths and hosts as desired)
```
[Unit]
Description=Roku
Wants=network.target
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/pi/roku_dummy
ExecStart=/home/pi/roku_dummy/bin/python -m roku -H 192.168.1.64

[Install]
WantedBy=multi-user.target
```

Then in a terminal, execute the following two commands to enable your new service
```shell
# systemctl enable roku.service
# systemctl start roku.service
```

---
If you wish to run inside a docker container, you can build your own image with `docker build . --tag roku_dummy` and then run it with `docker run roku_dummy <options>` 

Command line options
-------------
Configure through command line options, as shown below
```
usage: roku2mqtt.py [-h] [-p PORT] [-r ROOT] [-H HOST] [-d] [-v] [-V] [-C]
                   [-P LISTEN]

Roku mqtt emulator

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  MQTT port on host
  -r ROOT, --root ROOT  MQTT root topic
  -H HOST, --host HOST  MQTT Host
  -d, --debug           loglevel debug
  -v, --verbose         loglevel info
  -V, --version         show program's version number and exit
  -C, --cleanup         Cleanup mqtt topic on exit
  -P LISTEN, --listen LISTEN
                        Listen port
```
