#!/usr/bin/python3

import cfh
import os
import fo
import Printer as p

############
# Settings #
############

errors = []
warnings = []

dir = '/home/fargus/.SekhnetBackup'
conf_fl = fo.directoryify(dir) + 'backup.conf'
# comments are examples
conf_info = [
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
    #'rclone_conf',
    # isaac
    #'targets',
    # /home/fargus/Documents
    # /home/fargus/Pictures
    # /home/fargus/Downloads
    #'encrypt'
    # /home/fargus/Safe
'''

targets = []
rclone_conf = ''
encrypt_dirs = []

###########
# Methods #
###########

def print_errors(errors):
    for x in errors:
        p.print_error(x)

def print_warnings(warnings):
    for x in warnings:
        p.print_warning(x)
        
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
    p.print_warning('No config File found, generated one')
    p.print_warning('Exiting')
    exit()

# We have now verified that the config file exists along
# with the bin directory which will hold all of our programs
# files

# Loading data
conf_dic = conf.read_conf()

# We are targeting only the first index here, because there should only be one value
try:
    if len(conf_dic['rclone_conf']) > 1:
        warnings.append('Only one rclone conf should be specified, found more than one')
        warnings.append('Ignoring confs after the first one...')
    rclone_conf = conf_dic['rclone_conf'][0]

    targets = conf_dic['targets']
    encrypt_dirs = conf_dic['encrypt']
except IndexError:
    p.print_fatal_error('Invalid Config file, check \'%s\'' % conf_fl)
    exit(1)

###############################
# Verifying all targets exist #
###############################

kick_targets = []
for x in targets:
    if not os.path.exists(x):
        error = 'Path \'%s\' Does not exist ' % x
        errors.append(error)
        kick_targets.append(x)

kick_enc = []
for x in encrypt_dirs:
    if not os.path.exists(x):
        error = 'Path \'%s\' Does not exist ' % x
        errors.append(error)
        kick_enc.append(x)

# Removing non existing directories to prevent future errors
for x in kick_targets:
    targets.remove(x)

for x in kick_enc:
    encrypt_dirs.remove(x)

# Verifying that there are still directories left to work with
if len(encrypt_dirs) == 0:
    warnings.append('No directories specified to be encrypted')

if len(targets) == 0:
    print_errors(errors)
    print_warnings(warnings)
    p.print_fatal_error('No target directories to sync! Exiting...')
    exit(2)

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

# Printing Errors and warnings
print_warnings(warnings)
print_errors(errors)

##
# END #
     ##
