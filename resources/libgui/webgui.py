'''
    Copyright (C) 2014-2016 ddurdle

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

from SocketServer import ThreadingMixIn
import threading
import re
import urllib, urllib2
import sys

from resources.lib import default
from resources.libgui import xbmcplugin

class ThreadedWebGUIServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class WebGUIServer(ThreadingMixIn,HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.ready = True
        #self.TVDB = None
        #    self.MOVIEDB = None


    # set DBM
    def setDBM(self, dbm):
        self.dbm = dbm


class webGUI(BaseHTTPRequestHandler):


    #Handler for the GET requests
    def do_POST(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)

        # passed a kill signal?
        if self.path == '/kill':
            self.server.ready = False
            return


    def do_HEAD(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)

        # passed a kill signal?
        if self.path == '/kill':
            self.server.ready = False
            return




    #Handler for the GET requests
    def do_GET(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)


        # passed a kill signal?
        if self.path == '/kill':
            self.server.ready = False
            return


        # redirect url to output
        elif self.path == '/list':
            self.send_response(200)
            self.end_headers()
            #xbmcplugin.assignOutputBuffer(self.wfile)

            mediaEngine = default.contentengine()
            mediaEngine.run(self.wfile, DBM=self.server.dbm)
            #self.wfile.write(outputBuffer)
            return

        # redirect url to output
        elif re.search(r'/default.py', str(self.path)):
            self.send_response(200)
            self.end_headers()

            results = re.search(r'/default\.py\?(.*)$', str(self.path))
            if results:
                query = str(results.group(1))

            mediaEngine = default.contentengine()
            mediaEngine.run(self.wfile,query, DBM=self.server.dbm)
            return

        # redirect url to output
        else:
            # no options
            return
