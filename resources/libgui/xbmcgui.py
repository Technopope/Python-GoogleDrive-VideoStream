'''
    Copyright (C) 2014-2017 ddurdle

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


#
# The purpose of this class is to override  xbmcgui and supply equivalent subroutines when ran without KODI
#

import re

class Dialog(object):

    def ok(self, heading, line1, line2='', line3=''):
        print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        return
    def select(self, heading, line1, line2='', line3=''):
        #print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        return


class WindowXMLDialog(object):

    def ok(self, heading, line1, line2='', line3=''):
        return

class ListItem(object):


    ##
    ##
    def __init__(self, label,label2=None,iconImage=None,thumbnailImage=None,path=None):
        print label + "\n";
        if thumbnailImage is not None and thumbnailImage != "":
            self.thumbnailImage = thumbnailImage
        else:
            self.thumbnailImage = None
        print "thumbnail" + thumbnailImage + "\n"
        self.label = label
        self.path = None
        self.menu = ''

        return

    def setProperty(self,key,value):
        print "setProperty " + str(key) + ',' + str(value) + "\n"
        return

    def setInfo(self,key=None,value=None,type=None,infoLabels=None):
        print "setInfo " + str(key) + ',' + str(value) + "\n"
        return

    def setPath(self,path):
        self.path = path
        return


    def addContextMenuItems(self,cm,value):
        return


    def addStreamInfo(self,cm,value):
        print "xx\n"
        value = str(value)
        value = value.replace("\'",'')
        print "streaminfo " + str(value) + "\n"
        params = re.search(r'duration\: (\d+).* height\: (\d+)', str(value))
        duration = ''
        resolution = ''
        if params:
            duration = str(params.group(1))
            resolution = str(params.group(2))
        self.detail = '<sup><b>' + str(resolution) + 'p</b></sup><i>['+ str(int(duration)/60) + 'mins]</i>'
        #self.menu =  '<button title="+" onclick="if(document.getElementById(\''+str(self.label)+'\').style.display==\'none\'){document.getElementById(\''+str(self.label)+'\').style.display=\'\'}else{document.getElementById(\''+str(self.label)+'\').style.display=\'none\'}">+</button><div style="display: none" id="'+str(self.label)+'"> <strong>'+str(value)+'</strong></div>'
        return

    def __str__(self):
        return self.label

class xbmcgui:
    # CloudService v0.3.0


    ##
    ##
    def __init__(self):
        self.Dialog.ok = None
        return


    ##
    # Get the token of name with value provided.
    # returns: str
    ##
    def getToken(self,name):
        if name in self.auth:
            return self.auth[name]
        else:
            return ''

    ##
    # Get the count of authorization tokens
    # returns: int
    ##
    def getTokenCount(self):
        return len(self.auth)

    ##
    # Save the latest authorization tokens
    ##
    def saveTokens(self,instanceName,addon):
        for token in self.auth:
            addon.setSetting(instanceName + '_'+token, self.auth[token])

    ##
    # load the latest authorization tokens
    ##
    def loadToken(self,instanceName,addon, token):
        try:
            tokenValue = addon.getSetting(instanceName + '_'+token)
            if tokenValue != '':
              self.auth[token] = tokenValue
              return True
            else:
              return False
        except:
            return False

    ##
    # load the latest authorization tokens
    ##
    def isToken(self,instanceName, addon, token):
        try:
            if self.auth[token] != '':
              return True
            else:
              return False
        except:
            return False
