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

import constants
from resources.lib import default
from resources.libgui import xbmcplugin

class ThreadedWebGUIServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class WebGUIServer(ThreadingMixIn,HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.ready = True
        import addon_parameters
        self.addon = addon_parameters.addon
        self.hide = False
        self.keyvalue = False

    # set DBM
    def setDBM(self, dbm):
        self.dbm = dbm
        #setup encryption password
        import anydbm

        dbm = anydbm.open(dbm,'r')
        try:
            from resources.lib import encryption
            self.encrypt = encryption.encryption(dbm['salt'],dbm['password'])
        except:
            self.encrypt = None

        # login password?
        try:
            self.username = dbm['username']
            self.password = dbm['password']
        except:
            self.username = None
            self.password = None

        try:
            if dbm['hide'] == 'true':
                self.hide = True
            if dbm['keyvalue'] == 'true':
                self.keyvalue = True
        except: pass

        dbm.close()


class webGUI(BaseHTTPRequestHandler):


    #Handler for the GET requests
    def do_POST(self):




        decryptkeyvalue = self.path
        if re.search(r'kv\=', str(self.path)):
            from resources.lib import encryption

            results = re.search(r'kv\=(.*)$', str(self.path))
            if results:
                keyvalue = str(results.group(1))
                decryptkeyvalue = '/' + self.server.encrypt.decryptString(keyvalue).strip()
                print decryptkeyvalue +"."


        # debug - print headers in log
        headers = str(self.headers)
        print(headers)

        # passed a kill signal?
        if decryptkeyvalue == '/kill':
            if self.server.username is not None:
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                #print post_data

                self.send_response(200)
                self.end_headers()
                username = ''
                password = ''
                for r in re.finditer('username\=([^\&]+)' ,
                         post_data, re.DOTALL):
                    username = r.group(1)
                for r in re.finditer('password\=([^\&]+)' ,
                         post_data, re.DOTALL):
                    password = r.group(1)
                if self.server.username == username and self.server.password == password:
                    self.wfile.write("Stopping server...")
                    self.server.ready = False
                    print "Stopping server...\n"
                else:
                    self.wfile.write("Wrong username/password")


            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Stopping server...")
                self.server.ready = False
                print "Stopping server...\n"
            return

        elif decryptkeyvalue == '/list' or decryptkeyvalue == '/':

            if self.server.username is not None:
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                #print post_data

                username = ''
                password = ''
                for r in re.finditer('username\=([^\&]+)' ,
                         post_data, re.DOTALL):
                    username = r.group(1)
                for r in re.finditer('password\=([^\&]+)' ,
                         post_data, re.DOTALL):
                    password = r.group(1)
                if self.server.username == username and self.server.password == password:
                    mediaEngine = default.contentengine()
                    mediaEngine.run(self, DBM=self.server.dbm, addon=self.server.addon)
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write("Wrong username/password")

            else:
                mediaEngine = default.contentengine()
                mediaEngine.run(self, DBM=self.server.dbm, addon=self.server.addon)


        # redirect url to output
        elif re.search(r'/play.py', str(decryptkeyvalue)):

            print "TRYING TO SEEK WITH POSR REQUEST\n\n\n"


    def do_HEAD(self):

        # debug - print headers in log
        headers = str(self.headers)
        print(headers)


        print "HEAD HEAD HEAD\n\n"

        # passed a kill signal?
        if self.path == '/kill':
#            self.server.ready = False
            return



        # redirect url to output
        elif re.search(r'/play.py', str(self.path)):

            print "TRYING TO SEEK WITH HEAD REQUEST\n\n\n"


    #Handler for the GET requests
    def do_GET(self):

        decryptkeyvalue = self.path
        if re.search(r'kv\=', str(self.path)):
            from resources.lib import encryption

            results = re.search(r'kv\=(.*)$', str(self.path))
            if results:
                keyvalue = str(results.group(1))
                decryptkeyvalue = '/' + self.server.encrypt.decryptString(keyvalue).strip()
                print decryptkeyvalue +"."



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
        if decryptkeyvalue == '/kill':
            self.send_response(200)
            self.end_headers()
            if self.server.username is not None:
                self.wfile.write('<html><form action="/kill" method="post">Username: <input type="text" name="username"><br />Password: <input type="password" name="password"><br /><input type="submit" value="Stop Server"></form></html>')
            else:
                self.wfile.write('<html><form action="/kill" method="post"><input type="submit" value="Stop Server"></form></html>')

            #self.server.ready = False
            return

        elif decryptkeyvalue == '/settings':
            self.send_response(200)
            self.end_headers()

            self.setings = {}
            file = open('./resources/settings.xml', "r")
            print "LOAD SETTINGS\n\n\n"
            for line in file:
                result = re.search(r'\<setting id\=\"([^\"]+)\" type\=\"([^\"]+)\" values\=\"([^\"]+)\" default\=\"([^\"]+)\" label\=\"([^\"]+)\" \/\>', str(line))
                if result is None:
                    result = re.search(r'\<setting id\=\"([^\"]+)\" type\=\"([^\"]+)\"( )label\=\"([^\"]+)\" default\=\"([^\"]+)\" \/\>', str(line))

                id = ''
                type = ''
                values = ''
                defaults = ''
                label = ''
                if result:
                    id = str(result.group(1))
                    type = str(result.group(2))
                    values = str(result.group(3))
                    defaults = str(result.group(4))
                    label = str(result.group(5))
                    print "ID = " + id + "\n"

        elif decryptkeyvalue == '/list' or decryptkeyvalue == '/':
            self.send_response(200)
            self.end_headers()
            if self.server.username is not None:
                self.wfile.write('<html><form action="/list" method="post">Username: <input type="text" name="username"><br />Password: <input type="password" name="password"><br /><input type="submit" value="Login"></form></html>')
            else:
                self.wfile.write('<html><form action="/list" method="post"><input type="submit" value="Login"></form></html>')

            #self.server.ready = False
            return

            #self.send_response(200)
            #self.end_headers()
            #xbmcplugin.assignOutputBuffer(self.wfile)

            mediaEngine = default.contentengine()
            mediaEngine.run(self, DBM=self.server.dbm, addon=self.server.addon)
            #self.wfile.write(outputBuffer)
            return

        # redirect url to output
        elif re.search(r'/play', str(decryptkeyvalue)):
#            self.send_response(200)
#            self.end_headers()
            print "PLAYBACK" + "\n\n\n"
            count = 0
            results = re.search(r'/play\?count\=(.*)$', str(decryptkeyvalue))
            if results:
                count = int(results.group(1))
            #self.send_response(200)
            #self.end_headers()
            #xbmcplugin.assignOutputBuffer(self.wfile)
            #cookies = self.headers['Cookie']
            cookie = xbmcplugin.playbackBuffer.playback[count]['cookie']
            url = xbmcplugin.playbackBuffer.playback[count]['url']
            auth = xbmcplugin.playbackBuffer.playback[count]['auth']
            auth = auth.replace("+",' ')



            if start == '':
#                req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth})
                req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth})
            else:
                req = urllib2.Request(url,  None,  { 'Cookie' : 'DRIVE_STREAM='+ cookie, 'Authorization' : auth, 'Range': 'bytes='+str(start- startOffset)+'-' + str(end)})


            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 403 or e.code == 401:
                    print "STILL ERROR"+str(e.code)+"\n"
                    return
                else:
                    return

            if start == '':
                self.send_response(200)
                self.send_header('Content-Length',response.info().getheader('Content-Length'))
            else:
                self.send_response(206)
                self.send_header('Content-Length', str(int(response.info().getheader('Content-Length'))-startOffset))
                #self.send_header('Content-Range','bytes ' + str(start) + '-' +str(end))
                #if end == '':
                #    self.send_header('Content-Range','bytes ' + str(start) + '-' +str(int(self.server.length)-1) + '/' +str(int(self.server.length)))
                #else:
                #    self.send_header('Content-Range','bytes ' + str(start) + '-' + str(end) + '/' +str(int(self.server.length)))

                #self.send_header('Content-Range',response.info().getheader('Content-Range'))

            print str(response.info()) + "\n"
            self.send_header('Content-Type',response.info().getheader('Content-Type'))
            self.send_header('Content-Range', response.info().getheader('Content-Range'))
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
        elif re.search(r'/\?', str(decryptkeyvalue)) or re.search(r'/default.py', str(decryptkeyvalue)):
#            self.send_response(200)
#            self.end_headers()

            results = re.search(r'\?(.*)$', str(decryptkeyvalue))
            if results:
                query = str(results.group(1))

            mediaEngine = default.contentengine()
            mediaEngine.run(self,query, DBM=self.server.dbm, addon=self.server.addon)
            return

        # redirect url to output
        else:
            # no options
            return
