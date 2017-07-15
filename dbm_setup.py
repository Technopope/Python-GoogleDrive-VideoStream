
import sys
import re
import os

import anydbm

try:
    dbmfile = str(sys.argv[1])
    username = str(sys.argv[2])
    method = str(sys.argv[3])

    dbm = anydbm.open(dbmfile,'c')

    dbm['username'] = username
    print "method " + method
    if method == "1":
        passcode = str(sys.argv[4])
        dbm['type'] = '4'

    elif method == "2":

        argSize = len(sys.argv)
        if argSize == 7:
            dbm['clientid'] = str(sys.argv[4])
            dbm['clientsecret'] = str(sys.argv[5])
            dbm['code'] = str(sys.argv[6])

        elif argSize == 6:
            dbm['clientid'] = str(sys.argv[4])
            dbm['clientsecret'] = str(sys.argv[5])

        elif argSize == 5:
            dbm['code'] = str(sys.argv[4])

        dbm['type'] = '3'

    dbm.close()
except:
    print "usage:\n"
    print "1 - using your KODI plugin method - <dbm_file.db> <username> 1 <passcode>"
    print "2 - using your own client ID and secret method"
    print "\t\t step 1, print URL - <dbm_file.db> <username> 2 <client id> <client secret>"
    print "\t\t step 2, enter code - <dbm_file.db> <username> 2 <code>"
    print "\t\t OR enter code directly - <dbm_file.db> <username> 2 <client id> <client secret> <code>"