'''
    CloudService XBMC Plugin
    Copyright (C) 2013-2014 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''




from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from resources.libgui import webgui
import urllib, urllib2
from SocketServer import ThreadingMixIn
import threading
import sys
import os
import time
from resources.libgui import settingsdbm


# default.py [settings-dbm] [PORT] [SSL-certificate]
try:
    port = int(sys.argv[2])
except:
    port = 9988
try:
    dbmfile = str(sys.argv[1])
except:
    dbmfile = './gdrive.db'

try:
    sslcert = str(sys.argv[3])
except:
    sslcert = None

#try:
server = webgui.WebGUIServer(('',  port), webgui.webGUI)
if sslcert is not None:
    import ssl
    server.socket = ssl.wrap_socket (server.socket, certfile=sslcert, server_side=True)

server.setDBM(dbmfile)
server.setPort(port)

print "Google Drive Media Server ready....\n"

pid = os.fork()
if pid == 0:
    dbm = settingsdbm.settingsdbm(dbmfile)
    i=0
    while 1:
        runtime = dbm.getSetting(str(i)+'_runtime', None)
        frequency = dbm.getSetting(str(i)+'_frequency', None)
        status = dbm.getIntSetting(str(i)+'_status', None)
        if runtime is None:
            break
        elif status == 1:
            print "job #" + str(i)+ " is detected as incomplete\n"
            dbm.setSetting(str(i)+'_status', 1)
        i += 1
    print "scanning...\n"

    while 1:
        time.sleep(60)
        print "scanning...\n"

else:
    while server.ready:
        server.handle_request()
    server.socket.close()

#except: pass


#default.run()
