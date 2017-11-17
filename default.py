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

from resources.lib import default



from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from resources.libgui import webgui
import urllib, urllib2
from SocketServer import ThreadingMixIn
import threading

try:
    port = str(sys.argv[1])
except:
    port = 9988
try:
    dbmfile = str(sys.argv[2])
except:
    dbmfile = './gdrive.db'

#try:
server = webgui.WebGUIServer(('',  port), webgui.webGUI)
server.setDBM(dbmfile)
print "Google Drive Media Server ready....\n"

while server.ready:
    server.handle_request()
server.socket.close()
#except: pass


#default.run()
