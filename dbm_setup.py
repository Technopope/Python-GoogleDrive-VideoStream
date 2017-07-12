
import sys
import re
import os

import anydbm

try:
    dbmfile = str(sys.argv[1])
    username = str(sys.argv[2])
    code = str(sys.argv[3])

    dbm = anydbm.open(dbmfile,'c')

    dbm['username'] = username
    dbm['code'] = code

    dbm.close()
except:
    print "usage: dbm_file.db username code"