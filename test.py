from resources.lib import cloudservice
from resources.lib import gdrive_api2



import sys
import re
import os

print "hello world"

cloudservice = gdrive_api2.gdrive(None,None,'ninja','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.38 Safari/532.0',None, DBM='/tmp/test.db')
