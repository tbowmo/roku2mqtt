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

`python -m roku2mqtt <options>`

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
usage: roku2mqtt [-h] [-r MQTTROOT] [-H MQTTHOST] [--mqttport MQTTPORT]
                 [--mqttuser MQTTUSER] [--mqttpass MQTTPASS] [-l LOGFILE] [-d]
                 [-v] [-V] [--listen LISTEN] [--usn USN]

Roku emulator

Emulates a roku box, and publishes keystrokes on mqtt,
this is particular usefull in conjunction with a
harmony hub based remote control

optional arguments:
  -h, --help            show this help message and exit
  -r MQTTROOT, --mqttroot MQTTROOT
                        Root topic for mqtt publish
  -H MQTTHOST, --mqtthost MQTTHOST
                        Hostname / ip address for mqtt broker
  --mqttport MQTTPORT   Port number for mqtt broker
  --mqttuser MQTTUSER   User for mqtt connection
  --mqttpass MQTTPASS   Password for mqtt connection
  -l LOGFILE, --logfile LOGFILE
                        Log to filename
  -d, --debug           loglevel debug
  -v, --verbose         loglevel info
  -V, --version         show program's version number and exit
  --listen LISTEN       IP address and port for roku api, in the form of
                        192.168.3.113:8080
  --usn USN             Roku usn

I have detected this machines ip as: 192.168.3.113
```
