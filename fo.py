#!/usr/bin/python

import os, hashlib, shutil

'''

File Operator

This class is to hopefully make the moving of files easier in future projects


####### NOTE #############
####### NOTE #############
####### NOTE #############
####### NOTE #############
####### NOTE #############

    This is mostly legacy, written in Python2.7

    I have created Sekhnet3 to rebuild/modernize Sekhnet, using python3

####### NOTE #############
####### NOTE #############
####### NOTE #############
####### NOTE #############


'''

def get_file_info(file_list, relativePath=None, compute_md5=True):
    """Takes a list of file paths and returns a dictionary full of dictionaries with the keys as
        The file names and the values are based on file attributes. This is more efficient
        than searching the list every time.

        :returns

        NOTE: This works with directories but will not be able to compute md5 sum"""
    return_dic = {}
    for fl in file_list:

        fl_name = getFileNameStr(fl)

        # creating nested dictionary for file
        return_dic[fl_name] = {}

        # Having the name here is redundant
        return_dic[fl_name]['name'] = fl_name
        return_dic[fl_name]['path'] = fl
        return_dic[fl_name]['size'] = os.path.getsize(fl)

        # mtime = time last modified
        # ctime = time created
        return_dic[fl_name]['mtime'] = os.path.getmtime(fl)
        return_dic[fl_name]['ctime'] = os.path.getctime(fl)

        # Getting file hash if file is less than 128 MB
        if return_dic[fl_name]['size'] < 128 * 1000 * 1000 and compute_md5 and not os.path.isdir(fl):
            return_dic[fl_name]['md5'] = md5(fl)
        else:
            return_dic[fl_name]['md5'] = None

        if '.' in return_dic[fl_name]['name']:
            return_dic[fl_name]['ext'] = return_dic[fl_name]['name'].split('.')[-1]
        else:
            return_dic[fl_name]['ext'] = None

        if type(relativePath) == str:
            return_dic[fl_name]['relative_path'] = remove_root(relativePath, return_dic[fl_name]['path'])

    return return_dic


class FO(object):
    def __init__(self):
        # This is a list of file lists in a dictionary
        self.ls = {}

    #       self.s = sekhnet.sekhnet()

    def add(self, listName, item):
        # Checking if name already exists
        if listName not in self.ls:
            self.ls[listName] = []

        self.ls[listName].append(item)


def verify_md5sums_of_two_directories(dir0, dir1):
    """This will take the first directory, and verify all of the md5 sums
        are the same as the files in the second directory"""
    errors = []
    dir0_all_files = recurse_get_files(dir0, includeHidden=True)
    all_file_info = get_file_info(dir0_all_files, compute_md5=True)
    list_of_targets_for_dir1 = []

    for x in all_file_info:
        y = directoryify(dir1) + remove_root(dir0, all_file_info[x]['path'])
        if not verify_file_exists(y):
            errors.append('Unable to find in target directory : ' + y)
            continue
        list_of_targets_for_dir1.append(y)

    target_file_info = get_file_info(list_of_targets_for_dir1, compute_md5=True)

    for x in all_file_info:
        if x not in target_file_info:
            errors.append('not found:' + x)
            continue

        if all_file_info[x]['md5'] != target_file_info[x]['md5']:
            errors.append('Incorrect MD5:' + x)

    if len(errors) == 0:
        print ('HELL YEA ALL OF THE MD5 SUMS ARE IDENTICAL! YOU ARE GOOD MY DUDE')
    else:
        print('There were some errors:')
        for x in errors:
            print (x)
    exit(1)


def remove_root(root, path):
    """Takes a path and removes the specified root directory form that path
        This will return a relative path from the root
        Example:
            path: /home/fargus/Documents/something.txt
            root: /home/fargus/
            -----------------
            output: Documents/something.txt

        """
    ##s.check_str([root, path])

    # listifying
    root = root.split('/')[1:-1]
    path = path.split('/')[1:]

    # Validating input
    for x in range(0, len(root)):
        if root[x] != path[x]:
            raise ValueError('Error: Path must be in a subdirectory of the root')

    path = path[len(root):]
    return '/'.join(path)


def copy_list(toMove, dest):
    """Takes a list of absolute paths to files and copies them to a destination
       Also DOES NOT maintain directory structure
       This fully expects the directories to be there"""

    # toMove = get_path_dictionary(src_file_list, relativePath=src_root)

    for fl in toMove:
        # Checking if destination directory exists
        dest_dir = directoryify(dest) + '/'.join(toMove[fl]['relative_path'].split('/')[:-1])
        dest_path = directoryify(dest) + '/'.join(toMove[fl]['relative_path'].split('/')[:-1])

        # Making sure we don't copy to a non existent folder
        if not os.path.exists(dest_dir):
            mkdir(dest_dir)

        # print 'Src: ', toMove[fl]['path'],    '   dest', dest_path

        # Copying files and preserving attributes
        shutil.copy2(toMove[fl]['path'], dest_path)


def md5(fname, blocksize=2048):
    """Shamelessly plagiarized from stack overflow
        https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file"""

    m = hashlib.md5()
    with open(fname, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def directoryify(str):
    if str[-1] != '/':
        str = str + '/'
    return str


def getFilesFrom(targetDir, includeHidden=False):
    '''This just returns a list of files in a specified directory '''
    targetDir = directoryify(targetDir)
    filesList = []
    for filename in os.listdir(targetDir):
        if (not includeHidden) and (filename[0] == '.'):
            continue
        if (os.path.isfile(targetDir + filename)):
            filesList.append(targetDir + filename)
    return filesList


def recurse_file_info(dir, include_hidden=False, compute_md5=False):
    """Gets all information from files in a directory and all subdirectories, then returns the a
        dictionary with all of the file information.

        For more information visit 'get_file_info'"""
    # Validating input
    #s.check_str(dir)
    if not verify_file_exists(dir):
        raise OSError('Error: Specified Directory does not exist')

    # Getting the list of all files from directory
    all_files = recurse_get_files(dir, includeHidden=include_hidden)

    # Returning dictionary of files
    return get_file_info(all_files, compute_md5=compute_md5)


def get_file_ls(target):
    """This returns a list of strings, one for each line in the file"""

    #s.check_str(target)
    verify_file_exists(target)

    ls = []

    with open(target, 'r') as fl:
        for line in fl:
            if line != '\n' and line != '' and line != ' ':
                ls.append(line)

    return ls


def recurse_get_files(targetDir, includeHidden=False):
    '''This just returns a list of files in a specified directory and all subdirectories'''
    targetDir = directoryify(targetDir)
    filesList = []

    for filename in os.listdir(targetDir):

        # skipping hidden directories/files. I am certian there is a better logical way of doing this
        if (not includeHidden) and (filename[0] == '.'):
            continue

        # we dont want directories, only files
        if (os.path.isfile(targetDir + filename)):
            filesList.append(targetDir + filename)

        elif (os.path.isdir(targetDir + filename)):
            filesList = filesList + recurse_get_files(targetDir + filename, includeHidden=includeHidden)

    return filesList


def mkdir(path):
    """Makes a directory if it does not exist.
       Raises errors if unable to make directory."""
    path = directoryify(path)
    if not (os.path.exists(path)):
        try:
            # attempting to make directory
            os.mkdir(path)

            # Verifying directory was made
            if not (os.path.exists(path)):
                raise IOError('Unable to make dir', path)
        except IOError as e:
            print ('File Operator:', str(e))
            print ('Hint: Check if parent directory exists')
            exit(1)


def getFileNameStr(path):
    # Returns the file name from a path to a file
    #   example: '/test/foo.txt' would return 'foo.txt'
    return str(path.split('/')[-1])


def getFileNameDirList(path_list):
    """Returns the file name from a path to a file for a list.
       example: '/test/foo.txt' would return 'foo.txt'"""
    path_list = list(path_list)
    returnVar = []
    for path in path_list:
        returnVar.append(path.split('/')[-1])
    return returnVar


def check_path(target):
    #s.check_str(target)
    if not verify_file_exists(target):
        raise OSError('Error, The target you have selected does not exist')


def verify_file_exists(input):
    if type(input) == str:
        if os.path.exists(input):
            return True
        else:
            return False
    else:
        raise ValueError('Error, input must be string')


def verify_list_exists(input):
    """Returns 2 lists, a list of files that exist and ones that dont exist.
        Raises errors if input is invalid"""

    exists = []
    not_exists = []

    if type(input) != list:
        raise ValueError('Input must be list')
    else:
        for fl in input:
            if type(fl) != str:
                raise ValueError('Files must be represented as strings')
            if os.path.exists(fl):
                exists.append(fl)
            else:
                not_exists.append(fl)

    return exists, not_exists


def get_path_list_from_file_info_dic(input):
    #s.check_dic(input)

    rl = []
    for fl in input:
        rl.append(input[fl]['path'])
    return rl


def get_path_list_from_file_info_dic_with_different_root(input, alternative_root):
    #s.check_dic(input)

    rl = []
    for fl in input:
        rl.append(str(alternative_root + input[fl]['relative_path']))
    return rl


if __name__ == '__main__':
    pass


