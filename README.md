# roku dummy

Based on work by Marton Perei over at [gitlab](https://gitlab.com/mindig.marton/emulated_roku)

Emulates a roku device on the network, to fool harmony hub into thinking that there is a roku device on the network. It emits keypress events as mqtt topics to a mqtt broker. Which then can be used in automation setup, to control devices which normally are uncontrollable by harmony hub (like chromecasts.)

See also my chromecast control project [here](https://github.com/tbowmo/chromecastcontrol) which binds chromecast and mqtt together.

Change settings as needed in roku.py before starting it up.