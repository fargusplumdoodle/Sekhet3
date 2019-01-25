#!/usr/bin/python3

import cfh
import Printer as p
import fo
import os

if __name__ == '__main__':

    #  ## VARIABLES
    # this gets used sometimes
    title = 'Google Drive Backup'
    # value that we will plug into rclone to access google drive
    rclone_config = None
    # users home directory, ( this can be anything, but all dirs will be assumed to be in home dir)
    home_dir = None
    # the list of directories found in both the root of the google drive and in the users home dir
    dirs = []


    # ## END VARIABLES

    # ## LOG FILE GOBLDYGOOGK
    log_file = '/home/fargus/.backup.log'
    sp = p.SpoolPrinter(log_file)

    # ## END LOG FILE NONSENSE

    # ## CONFIG FILE CONFIGURATION
    try:
        config_file = '/home/fargus/.backup.conf'
        config_comments = 'I am writing this because every file in my home directory was deleted. I am now sad. Below write the directories you want to magically reappear if they are deleted They MUST be in the root directory of the Google Drive account that you have specified Also include full directories you fool This utility assumes you already have a valid rclone configuration. If you are unsure if you have this  please inform yourself. Because I am tired and sad and at school and its late and I want to finish this and go home. Dont give up hope and wash the dishes moron. ALSO THIS ONLY WORKS WITH DIRECTORIES IN YOUR HOME DIRECTORY'
        config_sections = ['rclone_config', 'home_dir', 'directories']

        # creating config file object
        cfh = cfh.cfh(config_file)

        # check for config file
        if not os.path.isfile(config_file):
            # if there is no config file, create it and exit
            cfh.generate_conf(title, config_comments, config_sections)
            p.print_header(title)
            sp.print_log('No config file found, generating config file')
            p.print_footer()
            exit(-1)

        # loading data from config
        config = cfh.read_conf()

        # getting rclone config, there should only be one element in this list, all else will be ignored
        rclone_config = config['rclone_config'][0]
        # getting home dir, there should only be one element in this list, all else will be ignored
        home_dir = config['home_dir'][0]
        # getting directories
        dirs = config['directories']
    except Exception as e:
        sp.print_log('Error with config: %s' % str(e))
        sp.print_log('Exiting')
        exit(-1)
    # ## END CONFIG FILE CONFIGURATION

    # ## UPLOADING DATA
    # For each directory
    for dir in dirs:
        dir_name = dir
        # Prepending home directory to active directory
        dir = (fo.directoryify(fo.directoryify(home_dir) + dir))

        # Verifying local directory exists, if it doesnt we skip it
        if not os.path.isdir(dir):
            sp.print_log('Error: Local path %s does not exist' % dir)
            sp.print_log('Skipping!')
            continue

        # running rclone command












