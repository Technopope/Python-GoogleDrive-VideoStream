# Python-GoogleDrive-VideoStream

This package replaces GoogleDrive-VideoStream (which was written in PHP).

This plugin is a direct port of Google Drive plugin for KODI.  The purpose of this plugin is to service content delivered in Google Drive plugin for KODI through any HTML5 client.

Use cases:
- export-and-import of STRM files for playback in Emby-Server
- playback of media through Safari and Chrome on iOS (iphone, ipod touch, ipad)
- playback of media through Firefox and Chrome on Android devices (tv players, phone, tablets)
- playback of media through any web browser on Windows, Mac OS, Linux
- playback of media through media player (such as VLC, KODI) that supports HTTPS streams

Current status - alpha testing.

Current status of items:
- photos (planning stage)
- music (may work, not tested)
- [enroll account] -- you must import settings.xml from a working Google Drive plugin for KODI (support without import of settings coming soon)
- configuring your plugin settings -- you must import settings.xml from a working Google Drive plugin for KODI (support without import of settings coming soon)
- language prompts currently show language codes instead of text (development underway)
- support for encfs (planned)
- support for pycrypto (development underway)
- create STRM files (development underway)
- select stream quality (development underway) -- currently uses your default setting
- SRT / CC (planning stage)
- cache and offline playback (planning stage)


Windows and Mac OS ready to playback without installing Python, coming soon.  Right now Linux based source package is available (python required, available on all Linux systems)

At this stage, you cannot enroll an account with this application or modify user settings.  You MUST import these from a KODI install.  I am only supporting alpha testing with users who have used the Google Drive plugin for KODI previously.


The DBM file contain's the user's settings and enrollment information for Google Drive.  To import your KODI settings, run:

python dbm_import.py <dbmfile> <kodi plugin settings.xml>

such as:

python dbm_import.py ./gdrive.db /home/durdle/.kodi/userdata/addon_data/plugin.video.gdrive-testing/settings.xml

To edit any single setting, you can use the KODI plugin to modify the setting or modify the parameter (if you know what you are doing) by running:

python dbm_setup.py <dbmfile> <key> <value>

To see a list of all settings:

python dbm_display.py <dbmfile>



To start the media server, run:

python default.py

The default dbmfile is ./gdrive.db and the default port to run on is 9988.  You can override these by running:

python default.py <port> <dbmfile>

You can use the setting.xml from either gdrive or gdrive-testing plugin for KODI.
