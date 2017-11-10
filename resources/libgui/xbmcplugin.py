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

class addSortMethod(object):

    def ok(self, heading, line1, line2='', line3=''):
        print heading + ":" + line1 + "\n" + line2 + "\n" + line3
        return

class addDirectoryItem(object):

    def __init__(self,plugin_handle, url, listitem, isFolder=None, totalItems=None):
        return

class endOfDirectory(object):

    def __init__(self,plugin_handle):
        return



class xbmcplugin:
    # CloudService v0.3.0


    ##
    ##
    def __init__(self):
        self.Dialog.ok = None
        return


