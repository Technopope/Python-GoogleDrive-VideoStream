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
import anydbm

class settingsdbm:
    # Settings

    ##
    ##
    def __init__(self, dbmfile):

        self.dbmfile = dbmfile
        #setup encryption password

        self.dbm = anydbm.open(dbmfile,'r')
        self.isReadOnly = True


    def reset(self):
        self.dbm.close()
        self.dbm = anydbm.open(self.dbmfile,'r')
        self.isReadOnly = True


    def getSetting(self, key, default=None):
        if not self.isReadOnly:
            self.dbm.close()
            self.dbm = anydbm.open(self.dbmfile,'r')
            self.isReadOnly = True

        if key is '':
            return None
        try:
            return self.dbm[key]
        except:
            return default

    def getBoolSetting(self, key, default=None):
        if not self.isReadOnly:
            self.dbm.close()
            self.dbm = anydbm.open(self.dbmfile,'r')
            self.isReadOnly = True

        if key is '':
            return None
        try:
            value = self.dbm[key]
            if value == 'True' or value == 'true':
                return True
            else:
                return False
        except:
            return default

    def getIntSetting(self, key, default=None):
        if not self.isReadOnly:
            self.dbm.sync()
            self.dbm.close()
            self.dbm = anydbm.open(self.dbmfile,'r')
            self.isReadOnly = True

        if key is '':
            return None
        try:
            return int(self.dbm[key])
        except:
            return default

    def setSetting(self, key, value):
        if self.isReadOnly:
            self.dbm.close()
            self.dbm = anydbm.open(self.dbmfile,'w')
            self.isReadOnly = False

        self.dbm[key] = value
        self.dbm.sync()

        return

