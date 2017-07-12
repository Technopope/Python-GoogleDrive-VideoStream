
import sys
import re
import os

import anydbm

try:
    dbmfile = str(sys.argv[1])
    dbm = anydbm.open(dbmfile,'c')

    for k, v in dbm.iteritems():
        print k + "\t" + v

    dbm.close()
except:
    print "usage: dbm_file.db"
