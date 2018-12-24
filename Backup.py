#!/usr/bin/python3

import cfh
import os
import fo
from Printer import VerbosityPrinter as vp

############
# Settings #
############

# Initializing Verbosity Printer
vp = vp(name='SekhnetBackup')

dir = '/home/fargus/SekhnetBackup'
conf_fl = fo.directoryify(dir) + 'backup.conf'
# comments are examples
conf_info = [
    'bin',
    # /home/fargus/safe_enc
    'rclone_conf',
    # isaac
    'targets',
    # /home/fargus/Documents
    # /home/fargus/Pictures
    # /home/fargus/Downloads
    'encrypt'
    # /home/fargus/Safe
]
conf_comments = '''
    #Example Settings:
    #'bin',
    # /home/fargus/safe_enc
    #'rclone_conf',
    # isaac
    #'targets',
    # /home/fargus/Documents
    # /home/fargus/Pictures
    # /home/fargus/Downloads
    #'encrypt'
    # /home/fargus/Safe
'''

###################
# Handling config #
###################

# Making directory if it doesnt exist
if not os.path.exists(dir):
    fo.mkdir(dir)

# Creating configuration handler object
conf = cfh.cfh(conf_fl)

# checking config file
if not os.path.exists(conf_fl):
    conf.generate_conf('Sekhnet gDrive Backup', conf_comments, conf_info)
    vp.print('No config File found, generated one')
    vp.print('Exiting')
    exit()



###############################
# Verifying all targets exist #
###############################


#  Compressing:
#  tar -zcvf compressed.tar.gz test/ > /dev/null
#
#  Encrypting:
#  openssl enc -aes-256-cbc -salt -k 1234asdf -in encryptMe.txt -out secure.d
#
#  Decompressing:
#  tar xf decrypted.tar.gz
#
#  Decrypting
#  openssl enc -aes-256-cbc -d -k 1234asdf -in secure.d -out plaintext.txt
#

##
# END #
     ##
