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
from datetime import datetime
import re
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
        runtime = dbm.getIntSetting(str(i)+'_runtime', None)
        status = dbm.getIntSetting(str(i)+'_status', None)
        if runtime is None:
            i += 1
            break
        elif status == '1':
            print "job #" + str(i)+ " is detected as incomplete\n"
            dbm.setSetting(str(i)+'_status', 1)
        i += 1


    while 1:
        i=0
        currentTime = int(time.time())
        while 1:
            runtime = dbm.getIntSetting(str(i)+'_runtime', None)
            instance = dbm.getSetting(str(i)+'_instance', None)
            if runtime is None and instance is None:
                i += 1
                break
            if instance is not None and instance != '':
                frequency = dbm.getIntSetting(str(i)+'_frequency', None)
                status = dbm.getIntSetting(str(i)+'_status', None)
                print 'job ' + str(i)+"instance = " + str(instance) +'frequency' + str(frequency)+ "\n"
                if status is None:
                    print "status = " + str(status) + 'job' + str(i)+"\n"
                elif status == 0 and frequency is not None and runtime < (currentTime - (frequency*60)) :
                    cmd = dbm.getSetting(str(i)+'_cmd', None)
                    print "time to run job #" + str(i) + ' runtime ' + str(runtime) + ' test ' + str(currentTime - (frequency*60))+  'cmd' + str(cmd) +  "\n"
                    if cmd is not None:
                        currentTime = int(time.time())
                        dbm.setSetting(str(i)+'_runtime', str(currentTime))
                        dbm.setSetting(str(i)+'_status', str(1))
                        if cmd.startswith('http'):
                            contents = urllib2.urlopen(cmd).read()
                        else:
                            contents = urllib2.urlopen('http://'+str(cmd)).read()
                        contents = re.sub('<[^<]+?>', '', contents)
                        currentTime = int(time.time())
                        dbm.setSetting(str(i)+'_runtime', str(currentTime))
                        dbm.setSetting(str(i)+'_status', str(0))
                        dbm.setSetting(str(i)+'_statusDetail', str(datetime.now()) + ' - ' + str(contents))
                else:
                    print "status = " + str(status) + "\n"

            i += 1

        time.sleep(6)
        print "scanning...\n"

else:
    while server.ready:
        server.handle_request()
    server.socket.close()

#except: pass


#default.run()
