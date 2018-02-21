# Python-GoogleDrive-VideoStream

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0d2f3f5f294c4e0db6112cfb4c2ba3d8)](https://www.codacy.com/app/ddurdle/Python-GoogleDrive-VideoStream?utm_source=github.com&utm_medium=referral&utm_content=ddurdle/Python-GoogleDrive-VideoStream&utm_campaign=badger)

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
- support for encfs (planned)
- SRT / CC (planning stage)
- cache and offline playback (planning stage)


Windows and Mac OS ready to playback without installing Python, coming soon.  Right now Linux based source package is available (python required, available on all Linux systems)

At this stage, you cannot enroll an account with this application or modify user settings.  You MUST import these from a KODI install.  I am only supporting alpha testing with users who have used the Google Drive plugin for KODI previously.





To start the media server, run:

python default.py

The default dbmfile is ./gdrive.db and the default port to run on is 9988.  You can override these by running:

python default.py <dbmfile> <port>

To use SSL using a SSL certificate (.pem file) you provide, change the port parameter (if required) and provide a third argument of the .pem file

python default.py <dbmfile> <port> <ssl certfile>

example:

python default.py ./gdrive.db 443 ./mycert.pem


You can use the setting.xml from either gdrive or gdrive-testing plugin for KODI.  You can import this using setup.py.  This is not required as you can setup the instance using the settings pane within the web interface.
