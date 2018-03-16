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
from resources.lib import scheduler


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
    schedule = scheduler.scheduler(logfile=dbm.getSetting('scheduler_logfile', None))

    i=0
    while 1:
        runtime = dbm.getIntSetting(str(i)+'_runtime', None)
        status = dbm.getIntSetting(str(i)+'_status', None)
        if runtime is None:
            i += 1
            break
        elif status == '1':
            schedule.log ("job #" + str(i)+ " is detected as incomplete")
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
                type = dbm.getIntSetting(str(i)+'_type', None)
                schedule.log ('job ' + str(i)+"instance = " + str(instance) +' frequency' + str(frequency) + ' type' + str(type))

                if status is None:
                    schedule.log ("status = " + str(status) + 'job' + str(i))
                elif (type == schedule.SYNC_BOTH or type == schedule.SYNC_CHANGE_ONLY) and status == 0 and frequency is not None and runtime < (currentTime - (frequency*60)) :
                    cmd = dbm.getSetting(str(i)+'_cmd', None)
                    schedule.log ("time to run job #" + str(i) + ' runtime ' + str(runtime) + ' test ' + str(currentTime - (frequency*60))+  'cmd' + str(cmd))

                    if cmd is not None:
                        currentTime = int(time.time())
                        dbm.setSetting(str(i)+'_runtime', str(currentTime))
                        dbm.setSetting(str(i)+'_status', str(1))
                        cmd = re.sub('buildstrmscheduler', 'buildstrm', cmd)
                        cmd = re.sub(' ', '%20', cmd)
                        if cmd.startswith('http'):
                            try:
                                contents = urllib2.urlopen(cmd).read()
                            except:
                                contents  = 'exception'
                        else:
                            try:
                                contents = urllib2.urlopen('http://'+str(cmd)).read()
                            except:
                                contents = 'exception'
                        contents = re.sub('<[^<]+?>', '', contents)
                        schedule.log(contents)

                        currentTime = int(time.time())
                        dbm.setSetting(str(i)+'_runtime', str(currentTime))
                        dbm.setSetting(str(i)+'_status', str(0))
                        dbm.setSetting(str(i)+'_statusDetail', str(datetime.now()) + ' - ' + str(contents))
                #else:
                #    schedule.log ("status = " + str(status))

            i += 1

        time.sleep(60)

else:
    while server.ready:
        server.handle_request()
    server.socket.close()

#except: pass


#default.run()
