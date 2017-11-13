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

        # redirect url to output
        elif self.path == '/play':
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            #print post_data

            self.send_response(200)
            self.end_headers()
            for r in re.finditer('([^\|]+)\|' ,
                     post_data, re.DOTALL):
                url = r.group(1)
                print "url = " + url + "\n"
            for r in re.finditer('(Cookie\=[^\&]+)' ,
                     post_data, re.DOTALL):
                cookie = r.group(1)
                print "cookie = " + cookie + "\n"
            for r in re.finditer('(Authorization\=[^\s]+)' ,
                     post_data, re.DOTALL):
                auth = r.group(1)
                print "auth = " + auth + "\n"

    def do_HEAD(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)

        # passed a kill signal?
        if self.path == '/kill':
            self.server.ready = False
            return



        # redirect url to output
        elif self.path == '/play':
            cookies = self.headers['Cookie']
            cookie = ''
            url = ''
            auth = ''
            print "COOKIES =" + cookies + "\n"
            for r in re.finditer(' url\=([^\;]+)\;' ,
                     cookies, re.DOTALL):
                url = r.group(1)
                print "url = " + url + "\n"
            for r in re.finditer(' Cookie\=DRIVE_STREAM\%3D([^\;]+)\;' ,
                     cookies, re.DOTALL):
                cookie = r.group(1)
                print "cookie = " + cookie + "\n"
            for r in re.finditer(' Authorization\=([^\;]+)\;' ,
                     cookies, re.DOTALL):
                auth = r.group(1)
                print "auth = " + auth + "\n"


            print 'HEAD ' + url + "\n\n\n\n"
            req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth})
            req.get_method = lambda : 'HEAD'

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403 or e.code == 401:
                    print "ERROR\n"
                    return
                else:
                    return

            self.send_response(200)
            #print str(response.info()) + "\n"
            self.send_header('Content-Type',response.info().getheader('Content-Type'))
            self.send_header('Content-Length',response.info().getheader('Content-Length'))
            self.send_header('Cache-Control',response.info().getheader('Cache-Control'))
            self.send_header('Date',response.info().getheader('Date'))
            self.send_header('Content-type','video/mp4')
            self.send_header('Accept-Ranges','bytes')

            #self.send_header('ETag',response.info().getheader('ETag'))
            #self.send_header('Server',response.info().getheader('Server'))
            self.end_headers()

            ## may want to add more granular control over chunk fetches
            #self.wfile.write(response.read())

            response.close()
            print "DONE"
            self.server.length = response.info().getheader('Content-Length')


    #Handler for the GET requests
    def do_GET(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)


        start = ''
        end = ''
        startOffset = 0
        for r in re.finditer('Range\:\s+bytes\=(\d+)\-' ,
                     headers, re.DOTALL):
          start = int(r.group(1))
          break
        for r in re.finditer('Range\:\s+bytes\=\d+\-(\d+)' ,
                     headers, re.DOTALL):
          end = int(r.group(1))
          break


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
        elif self.path == '/play':
            #self.send_response(200)
            #self.end_headers()
            #xbmcplugin.assignOutputBuffer(self.wfile)
            cookies = self.headers['Cookie']
            cookie = ''
            url = ''
            auth = ''
            print "COOKIES =" + cookies + "\n"
            for r in re.finditer(' url\=([^\;]+)\;' ,
                     cookies, re.DOTALL):
                url = r.group(1)
                print "url = " + url + "\n"
            for r in re.finditer(' Cookie\=DRIVE_STREAM\%3D([^\;]+)\;' ,
                     cookies, re.DOTALL):
                cookie = r.group(1)
                print "cookie = " + cookie + "\n"
            for r in re.finditer(' Authorization\=([^\;]+)\;' ,
                     cookies, re.DOTALL):
                auth = r.group(1)
                print "auth = " + auth + "\n"

            if start == '':
                req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth})
            else:
                req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth, 'Range': 'bytes='+str(start- startOffset)+'-' + str(end)})


            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403 or e.code == 401:
                    print "STILL ERROR\n"
                    return
                else:
                    return
            self.server.length = response.info().getheader('Content-Length')

            if start == '':
                self.send_response(200)
                self.send_header('Content-Length',response.info().getheader('Content-Length'))
            else:
                self.send_response(206)
                self.send_header('Content-Length', str(int(response.info().getheader('Content-Length'))-startOffset))
                #self.send_header('Content-Range','bytes ' + str(start) + '-' +str(end))
                if end == '':
                    self.send_header('Content-Range','bytes ' + str(start) + '-' +str(int(self.server.length)-1) + '/' +str(int(self.server.length)))
                else:
                    self.send_header('Content-Range','bytes ' + str(start) + '-' + str(end) + '/' +str(int(self.server.length)))

                #self.send_header('Content-Range',response.info().getheader('Content-Range'))
                print 'Content-Range!!!' + str(start) + '-' + str(int(self.server.length)-1) + '/' +str(int(self.server.length)) + "\n"

            print str(response.info()) + "\n"
            self.send_header('Content-Type',response.info().getheader('Content-Type'))

            self.send_header('Cache-Control',response.info().getheader('Cache-Control'))
            self.send_header('Date',response.info().getheader('Date'))
            self.send_header('Content-type','video/mp4')
            self.send_header('Accept-Ranges','bytes')

            self.end_headers()

            CHUNK = 16 * 1024
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                self.wfile.write(chunk)

            #response_data = response.read()
            response.close()
            return

        # redirect url to output
        elif re.search(r'/default.py', str(self.path)):
#            self.send_response(200)
#            self.end_headers()

            results = re.search(r'/default\.py\?(.*)$', str(self.path))
            if results:
                query = str(results.group(1))

            mediaEngine = default.contentengine()
            mediaEngine.run(self,query, DBM=self.server.dbm)
            return

        # redirect url to output
        else:
            # no options
            return
