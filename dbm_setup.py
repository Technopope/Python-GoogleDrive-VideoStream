
import sys
import re
import os

import anydbm

try:
    dbmfile = str(sys.argv[1])
    key = str(sys.argv[2])
    value = str(sys.argv[3])

    dbm = anydbm.open(dbmfile,'c')

    dbm[key] = value
    print "added " + key + ',' + value + "\n"
    dbm.close()
except:
    print "add a key-value pair to the setup dbm - usage:\n"
    print "python dbm_setup.py <dbm_file.db> <key> <value>\n"
