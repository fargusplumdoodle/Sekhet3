# !/usr/bin/python

#import sekhnet as s
import datetime
import time

class SpoolPrinter(object):
    """For outputing to both stdout and a file"""
    def __init__(self, output_file, overwrite=False):
#        import sekhnet as s
#        s.check_str(output_file)
        self.output_file = output_file

        if overwrite:
            self.overwrite_file()

    def overwrite_file(self):
        """Makes an empty file where the target output file is"""
        of = open(self.output_file, "w")
        of.write('')
        of.close()

    def println(self, output_line):
        """Prints output to both stdout and a file"""
        output_line = str(output_line)

        # Printing output to stdout
        print(output_line)

        try:
            # Opening file
            of = open(self.output_file, "a")

            # Writing output
            of.write(str(output_line))
            of.write('\n')

            # Closing file
            of.close()
        except IOError as e:
            print('Printerln:', str(e))

    def printls(self, output_ls):
        """Prints a list of outputs to both stdout and a file"""

        # Verifying input
        s.check_list(output_ls)

        # Writing to stdout
        for x in output_ls:
            print(x)
        print

        try:
            # Opening file
            of = open(self.output_file, "a")

            # Writing output to file
            of.writelines(output_ls)
            of.write('\n')

            # Closing file
            of.close()
        except IOError as e:
            print('Printerls:', str(e))

class VerbosityPrinter(object):
    '''

    :param msg: message you want to print
    :param v: verbosity level of message

    When the program is ran, a verbosity level is selected

    v = 1: <msg>
    v = 2: <msg> <name>
    v = 3: <msg> <time>
    v = 4: <msg> <name> <time>

    '''

    def __init__(self, v=4, name='Spooky'):
        self.verbose = v
        self.name = name
        self.length = 40

    def print(self, msg, v=4, ):
        if not self.verbose == 0 and not v > self.verbose :
            msg = msg + (' ' * (self.length - len(msg)))
            if v == 1 and self.verbose >= v:
                print((msg))
            if v == 2 and self.verbose >= v:
                print("%s: %s" % (self.name, msg))
            if v == 3 and self.verbose >= v:
                print("%s   %s " % (msg, time.time()))
            if v == 4 and self.verbose >= v:
                print("%s: %s    %s" % (self.name, msg, time.time()))

    def overwrite_file(self):
        """Makes an empty file where the target output file is"""
        of = open(self.output_file, "w")
        of.write('')
        of.close()

    def println(self, output_line):
        """Prints output to both stdout and a file"""
        output_line = str(output_line)

        # Printing output to stdout
        print(output_line)

        try:
            # Opening file
            of = open(self.output_file, "a")

            # Writing output
            of.write(str(output_line))
            of.write('\n')

            # Closing file
            of.close()
        except IOError as e:
            print('Printerln:', str(e))

    def printls(self, output_ls):
        """Prints a list of outputs to both stdout and a file"""

        # Writing to stdout
        for x in output_ls:
            print(x)
        print

        try:
            # Opening file
            of = open(self.output_file, "a")

            # Writing output to file
            of.writelines(output_ls)
            of.write('\n')

            # Closing file
            of.close()
        except IOError as e:
            print('Printerls:', str(e))

def from_now_on_computer_generated(self):
    self.println('''###################################################
# FROM HERE FORTH, THE DATA IS COMPUTER GENERATED #
# Sekhnet SpoolPrinter ''' + print_now() + ''' #
###################################################''')

def is_even(x):
    # checks if number and returns true for even, false for not even
    if x % 2 == 0:
        return True
    else:
        return False

def print_footer(str):
    # getting the length that we need to just with
    # then dividing it by two
    x = 47 - 2 - len(str)
    x = int(x / 2)
    # Checking to see if this number is even, if it isnt we subtract one from it later to make up the space difference
    hashes = '#' * x

    output = hashes + ' ' + str + ' ' + hashes

    return output

def print_json(json):
    """Hopefully prints all of json data, has not been tested very well and probbably wont work"""
    #import sekhnet
    #s.check_dic(json)

    def print_each_item(input, indent=0):
        if type(input) == list:
            for x in input:
                print_each_item(x, indent=indent + 4)
        elif type(input) == tuple:
            for x in input:
                print_each_item(x, indent=indent + 4)
        elif type(input) == dict:
            for x in input:
                print(' ' * indent + str(x) + '\n')
                print_each_item(input[x], indent=indent + 4)
        else:
            # This is not an iterable, hopefully....
           print(' ' * indent + str(input) + '\n')

    print_each_item(json)


def print_header(str):
    returnStr = ''
    ln = len(str)
    hashes = '#' * (47)
    returnStr = returnStr + '\n'
    returnStr = returnStr + hashes
    returnStr = returnStr + '\n'
    returnStr = returnStr + '#' + str.center(len(hashes) - 2 ) + '#'
    returnStr = returnStr + '\n'
    returnStr = returnStr + hashes
    returnStr = returnStr + '\n'
    return returnStr


