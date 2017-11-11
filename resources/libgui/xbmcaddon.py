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
    #
        return

    ##
    # return the setting from DBM
    ##
    def getSetting(self,key):
        print "getting key " + key + "\n"
        return self.dbm[key]

    ##
    # return the setting from DBM
    ##
    def getLocalizedString(self,key):
        print str(key)
        return str(key)


