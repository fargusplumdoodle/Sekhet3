#!/usr/bin/python3

import Printer as p
import fo
import os
from subprocess import Popen, PIPE
import threading

class Rclone_Wrapper(threading.Thread):
    def __init__(self, log_file='/home/fargus/.backup.log', config_file='/home/fargus/.backup.conf'):
        # calling super constructor
        super(Rclone_Wrapper, self).__init__()
        #  ## VARIABLES
        # this gets used sometimes
        self.title = 'Google Drive Backup'
        # value that we will plug into rclone to access google drive
        self.rclone_config = None
        # users home directory, ( this can be anything, but all dirs will be assumed to be in home dir)
        self.home_dir = None
        # the list of directories found in both the root of the google drive and in the users home dir
        self.dirs = []

        # log file shananagins
        self.log_file = log_file
        self.sp = p.SpoolPrinter(self.log_file)
        # ## END VARIABLES


        # ## CONFIG FILE CONFIGURATION
        try:
            config_file = config_file
            # config_comments = 'I am writing this because every file in my home directory was deleted. I am now sad. Below write the directories you want to magically reappear if they are deleted They MUST be in the root directory of the Google Drive account that you have specified Also include full directories you fool This utility assumes you already have a valid rclone configuration. If you are unsure if you have this  please inform yourself. Because I am tired and sad and at school and its late and I want to finish this and go home. Dont give up hope and wash the dishes moron. ALSO THIS ONL'
            config_comments = 'This program syncs each of the directories within a given directory with your google drive. \n remote_host: rclone config\nhome_dir: your shared folder\ndirectories: all of the directories in your shared folder that you want to sync\n\nFargus Plumdoodle 2019'
            config_sections = ['remote_host', 'home_dir', 'directories']

            # creating config file object
            import cfh
            cfh = cfh.cfh(config_file)

            # check for config file
            if not os.path.isfile(config_file):
                # if there is no config file, create it and exit
                cfh.generate_conf(self.title, config_comments, config_sections)
                p.print_header(self.title)
                self.sp.print_log('No config file found, generating config file')
                p.print_footer()
                exit(-1)

            # loading data from config
            config = cfh.read_conf()

            # getting rclone config, there should only be one element in this list, all else will be ignored
            self.rclone_config = config['remote_host'][0]
            # getting home dir, there should only be one element in this list, all else will be ignored
            self.home_dir = config['home_dir'][0]
            # getting directories
            self.dirs = config['directories']
        except Exception as e:
            self.sp.print_log('Error with config: %s' % str(e))
            self.sp.print_log('Exiting')
            exit(-1)
        # ## END CONFIG FILE CONFIGURATION

    def run(self):
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('# STARTING %s at %s #' % (self.title, p.print_now()))
        # ## TRANSFERRING DATA
        # For each directory
        for dir in self.dirs:
            dir_name = dir
            self.sp.print_log('# STARTING %s at %s #' % (dir_name, p.print_now()))
            # Prepending home directory to active directory
            dir = (fo.directoryify(fo.directoryify(self.home_dir) + dir))

            # upload variable
            upload = True
            download = True

            # Verifying local directory exists, if it doesnt we skip it
            if not os.path.isdir(dir):
                self.sp.print_log('WARNING: Local path %s does not exist' % dir)
                self.sp.print_log('Skipping Uploading!')
                upload = False

            # verifying remote dir exists
            verify_command = str('rclone lsd %s:/' % self.rclone_config).split(' ')
            process = Popen(verify_command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if dir_name not in stdout.decode('utf-8'):
                self.sp.print_log('WARNING: remote path /%s does not exist' % dir_name)
                self.sp.print_log('Skipping Downloading!')
                download = False

            # UPLOADING DATA!!!!!
            if upload:
                self.sp.print_log('INITIATING UPLOAD: %s!' % dir_name)
                # generating bash command as list of arguments
                upload_command = str('rclone copy -v %s %s:%s' % (dir, self.rclone_config, dir_name)).split(' ')

                # Go stack overflow I choose you!
                try:
                    process = Popen(upload_command, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                except Exception as e:
                    # if there was a python issue with running the command
                    self.sp.print_log('ERROR EXECUTING UPLOAD: %s ' % str(e))
                    exit(-1)
                # logging data from rclone
                self.sp.print_log('Upload stdout:')
                self.sp.println(stdout.decode('utf-8'))
                self.sp.print_log('Upload stderr:')
                self.sp.println(stderr.decode('utf-8'))

            # DOWNLOADING DATA!!!!!
            if download:
                self.sp.print_log('INITIATING DOWNLOAD: %s!' % dir_name)
                # generating bash command as list of arguments
                upload_command = str('rclone copy -v %s:%s %s' % (self.rclone_config, dir_name, dir)).split(' ')

                # Go stack overflow I choose you!
                try:
                    process = Popen(upload_command, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                except Exception as e:
                    # if there was a python issue with running the command
                    self.sp.print_log('ERROR EXECUTING DOWNLOAD: %s ' % str(e))
                    exit(-1)
                # logging data from rclone
                self.sp.print_log('Download stdout:')
                self.sp.println(stdout.decode('utf-8'))
                self.sp.print_log('Download stderr:')
                self.sp.println(stderr.decode('utf-8'))
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('')
        self.sp.print_log('')
        self.sp.print_log('')
#!/usr/bin/python3


class Rsync_Wrapper(threading.Thread):
    def __init__(self, log_file='/home/fargus/.backup_rsync.log', config_file='/home/fargus/.backup_rsync.conf'):
        # calling super constructor
        super(Rsync_Wrapper, self).__init__()
        #  ## VARIABLES
        # this gets used sometimes
        self.title = 'Rsync Backup'
        # users home directory, ( this can be anything, but all dirs will be assumed to be in home dir)
        self.home_dir = None
        #  remote directory that all of the subfolders are stored in example: /mnt/user
        self.remote_home = None
        # the list of directories found in both the root of the google drive and in the users home dir
        self.dirs = []

        # log file shananagins
        self.log_file = log_file
        self.sp = p.SpoolPrinter(self.log_file)
        # ## END VARIABLES


        # ## CONFIG FILE CONFIGURATION
        try:
            config_file = config_file
            config_comments = 'I am writing this because every file in my home directory was deleted. I am now sad. Below write the directories you want to magically reappear if they are deleted They MUST be in the root directory of the Google Drive account that you have specified Also include full directories you fool This utility assumes you already have a valid rclone configuration. If you are unsure if you have this  please inform yourself. Because I am tired and sad and at school and its late and I want to finish this and go home. Dont give up hope and wash the dishes moron. ALSO THIS ONLY WORKS WITH DIRECTORIES IN YOUR HOME DIRECTORY'
            config_sections = ['remote_host', 'home_dir', 'directories', 'remote_home']

            # creating config file object
            import cfh
            cfh = cfh.cfh(config_file)

            # check for config file
            if not os.path.isfile(config_file):
                # if there is no config file, create it and exit
                p.print_header(self.title)
                self.sp.print_log('No config file found, generating config file')
                cfh.generate_conf(self.title, config_comments, config_sections)
                p.print_footer()
                exit(-1)

            # loading data from config
            config = cfh.read_conf()

            # getting rclone config, there should only be one element in this list, all else will be ignored
            self.remote_host = config['remote_host'][0]
            # remote home direcotry
            self.remote_home = config['remote_home'][0]
            # getting home dir, there should only be one element in this list, all else will be ignored
            self.home_dir = config['home_dir'][0]
            # getting directories
            self.dirs = config['directories']
        except Exception as e:
            self.sp.print_log('Error with config: %s' % str(e))
            self.sp.print_log('Exiting')
            exit(-1)
        # ## END CONFIG FILE CONFIGURATION

    def run(self):
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('# STARTING %s at %s #' % (self.title, p.print_now()))
        # ## TRANSFERRING DATA
        # For each directory
        for dir in self.dirs:
            dir_name = dir
            self.sp.print_log('# STARTING %s at %s #' % (dir_name, p.print_now()))
            # Prepending home directory to active directory
            dir = (fo.directoryify(fo.directoryify(self.home_dir) + dir))
            remote_dir = (fo.directoryify(fo.directoryify(self.remote_home) + dir_name))

            # upload variable
            upload = True
            download = True

            # Verifying local directory exists, if it doesnt we skip it
            if not os.path.isdir(dir):
                self.sp.print_log('WARNING: Local path %s does not exist' % dir)
                self.sp.print_log('Skipping Uploading!')
                upload = False

            #FIXME: we cannot verify that remote directory exists
            # verifying remote dir exists
            verify_command = str("ssh %s 'if [ -d '%s' ]; then echo fart; fi'" % (self.remote_host, remote_dir))
            print(verify_command)
            process = Popen(verify_command.split(' '), stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print(stdout, stderr)
            if 'fart' not in stdout.decode('utf-8'):
                self.sp.print_log('WARNING: remote path /%s does not exist' % dir_name)
                self.sp.print_log('Skipping Downloading!')
                download = False
            else:
                print('all good')
            continue

            # UPLOADING DATA!!!!!
            if upload:
                self.sp.print_log('INITIATING UPLOAD: %s!' % dir_name)
                # generating bash command as list of arguments
                upload_command = str('rclone copy -v %s %s:%s' % (dir, self.remote_host, dir_name)).split(' ')

                # Go stack overflow I choose you!
                try:
                    process = Popen(upload_command, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                except Exception as e:
                    # if there was a python issue with running the command
                    self.sp.print_log('ERROR EXECUTING UPLOAD: %s ' % str(e))
                    exit(-1)
                # logging data from rclone
                self.sp.print_log('Upload stdout:')
                self.sp.println(stdout.decode('utf-8'))
                self.sp.print_log('Upload stderr:')
                self.sp.println(stderr.decode('utf-8'))

            # DOWNLOADING DATA!!!!!
            if download:
                self.sp.print_log('INITIATING DOWNLOAD: %s!' % dir_name)
                # generating bash command as list of arguments
                upload_command = str('rclone copy -v %s:%s %s' % (self.remote_host, dir_name, dir)).split(' ')

                # Go stack overflow I choose you!
                try:
                    process = Popen(upload_command, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                except Exception as e:
                    # if there was a python issue with running the command
                    self.sp.print_log('ERROR EXECUTING DOWNLOAD: %s ' % str(e))
                    exit(-1)
                # logging data from rclone
                self.sp.print_log('Download stdout:')
                self.sp.println(stdout.decode('utf-8'))
                self.sp.print_log('Download stderr:')
                self.sp.println(stderr.decode('utf-8'))
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('#######################################################################')
        self.sp.print_log('')
        self.sp.print_log('')
        self.sp.print_log('')
