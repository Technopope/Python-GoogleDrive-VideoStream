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

import anydbm
import re


# The purpose of this class is to override  xbmcaddon and supply equivalent subroutines when ran without KODI
#

class getAddonInfo(object):

    def ok(self, heading, line1, line2='', line3=''):
        print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        return



class xbmcaddon:
    # CloudService v0.3.0

    ##
    ##
    def __init__(self):

        self.dbmfile = './gdrive.db'
        self.dbm = anydbm.open(self.dbmfile,'r')
        self.language = {}
        file = open('./resources/language/english/strings.xml', "r")
        for line in file:
            result = re.search(r'\<string id\=\"([^\"]+)\"\>([^\<]+)\<', str(line))
            key = ''
            value = ''
            if result:
                key = str(result.group(1))
                value = str(result.group(2))
                self.language[key] = value;



        return

    def getAddonInfo(self, id):
        return ''



    ##
    # return the setting from DBM
    ##
    def getSetting(self,key):
        try:
           return self.dbm[key]
        except:
           return ''


    ##
    # return the setting from DBM
    ##
    def setSetting(self,key,value):
        self.dbm.close()
        self.dbm = anydbm.open(self.dbmfile,'w')
        self.dbm[key] = value
        self.dbm.close()
        self.dbm = anydbm.open(self.dbmfile,'r')
        print "setting key " + key + "\n"
        return


    ##
    # return the language setting
    ##
    def getLocalizedString(self,key):
        return self.language[str(key)]


