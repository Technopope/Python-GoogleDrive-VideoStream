from resources.lib import  encryption
#from subprocess import call

import sys
import re
import os

saltFile = str(sys.argv[1])
password = str(sys.argv[2])
source = str(sys.argv[3])
target = str(sys.argv[4])

encrypt = encryption.encryption(saltFile,password)
#encrypt.encryptString(file)
#print encrypt.decryptString(file)


def encrypt_dir(source, target):

  current, dirs, files = os.walk(source).next()

  for file in files:
    encrypt.encryptFile(source + '/' + file, target +'/'+encrypt.encryptString(file))

  for dir in dirs:
    encDIR = encrypt.encryptString(dir)
    os.mkdir(target + '/' + encDIR)
    encrypt_dir(source + '/' + dir, target +'/'+encDIR)


#print encrypt.generateSalt()

encrypt_dir(source, target)
