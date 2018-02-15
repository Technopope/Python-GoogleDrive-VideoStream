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
from resources.libgui import xbmcplugin

class Dialog(object):

    def ok(self, heading, line1, line2='', line3=''):
        print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        xbmcplugin.outputBuffer.output = xbmcplugin.outputBuffer.output + '<br/>' + line1
        return
    def select(self, heading, line1, line2='', line3=''):
        #print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        return
    def yesno(self, heading, line1):
        return
    def inputText(self, variable, name, url, parameters):
        hidden = ''
        for r in re.finditer('([^\=]+)\=([^\&]+)(?:\&|$)' ,
                 parameters, re.DOTALL):
            key = r.group(1)
            value = r.group(2)
            hidden = hidden + '<input type="hidden" name="'+str(key)+'" value="'+str(value)+'" />'
        xbmcplugin.outputBuffer.output = xbmcplugin.outputBuffer.output + '<form post="'+str(url)+'" method="GET"><input type="text" name="'+str(variable)+'"/>'+hidden+'<input type="submit" value="'+str(name)+'"/></form><br/>'
        return
    def browse(self, variable0, variable1, name, variable2,variable3,variable4, variable5):
        xbmcplugin.outputBuffer.output = xbmcplugin.outputBuffer.output + str(variable1) + '<input type="text" name="'+str(name)+'"/><br/>'
        return
    def startForm(self, url, parameters):
        hidden = ''
        for r in re.finditer('([^\=]+)\=([^\&]+)(?:\&|$)' ,
                 parameters, re.DOTALL):
            key = r.group(1)
            value = r.group(2)
            hidden = hidden + '<input type="hidden" name="'+str(key)+'" value="'+str(value)+'" />'
        xbmcplugin.outputBuffer.output = xbmcplugin.outputBuffer.output + '<form post="'+str(url)+'" method="GET">'+hidden

    def endForm(self):
        xbmcplugin.outputBuffer.output = xbmcplugin.outputBuffer.output +'<input type="submit" value="submit"/></form><br/>'


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
        self.label = label
        self.path = None
        self.menu = ''
        self.detail = ''

        return

    def setProperty(self,key,value):
        #print "setProperty " + str(key) + ',' + str(value) + "\n"
        return

    def setInfo(self,key=None,value=None,type=None,infoLabels=None):
        #print "setInfo " + str(key) + ',' + str(value) + "\n"
        return

    def setPath(self,path):
        self.path = path
        return


    def addContextMenuItems(self,cm,value):
        #print "setInfo " +str(value) + "\n"
        i=0
        menuItems = ''
        while i < len(cm):
            url = cm[i][1]
            params = re.search(r'\(([^\)]+)\)', str(url))
            if params:
                url = str(params.group(1))

            menuItems += '<a href="'+str(url)+'">'+str(cm[i][0])+'</a><br/>'
            i += 1

#        self.menu =  '<button title="+" onclick="if(document.getElementById(\''+str(self.label)+'\').style.display==\'none\'){document.getElementById(\''+str(self.label)+'\').style.display=\'\'}else{document.getElementById(\''+str(self.label)+'\').style.display=\'none\'}">+</button><div style="display: none" id="'+str(self.label)+'"> <strong>'+str(menuItems)+'</strong></div>'
        self.menu =  '<button title="+" onclick="if(document.getElementById(\''+str(self.label)+'\').style.display==\'none\'){document.getElementById(\''+str(self.label)+'\').style.display=\'\'}else{document.getElementById(\''+str(self.label)+'\').style.display=\'none\'}">+</button><div style="display: none" id="'+str(self.label)+'">'+str(menuItems)+'</div>'
        return


    def addStreamInfo(self,cm,value):
        value = str(value)
        value = value.replace("\'",'')
        params = re.search(r'duration\: (\d+).* height\: (\d+)', str(value))
        duration = ''
        resolution = ''
        if params:
            duration = str(params.group(1))
            resolution = str(params.group(2))
        self.detail = '<sup><b>' + str(resolution) + 'p</b></sup><i>['+ str(int(duration)/60) + 'mins]</i>'
        self.menu =  '<button title="+" onclick="if(document.getElementById(\''+str(self.label)+'\').style.display==\'none\'){document.getElementById(\''+str(self.label)+'\').style.display=\'\'}else{document.getElementById(\''+str(self.label)+'\').style.display=\'none\'}">+</button><div style="display: none" id="'+str(self.label)+'"> <strong>'+str(value)+'</strong></div>'
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


