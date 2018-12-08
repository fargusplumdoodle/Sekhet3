#!/usr/bin/python3.6

import Printer as p
import fo
import os
import re


def GetData(search, lines=1000):
    #
    logs = os.popen('sudo journalctl -n --lines=%s' % lines).read()

    logs = logs.split('\n')


    incidents = []
    search_term = search
    search = r'.*' + search + r'.*'

    # Here we filter out all logs that do not match the search term that the user provided
    for x in logs:
        if re.match(search, x):
            incidents.append(x)

    # Here we extract relevant information from the logs
    data = []
    for x in incidents:
        date = re.search(r'^\w+ \d+ \d\d:\d\d:\d\d', x)
        src = re.search(r'SRC=(\d|:|\.|\w)+', x)
        port = re.search(r'DPT=(\d)+', x)

        try:
            date = date.group(0)
        except AttributeError:
            date = 'NO DATE FOUND'

        try:
            src = src.group(0)[4:]
        except AttributeError:
            # if there is no src it was not a ufw block rule
            continue

        try:
            port = port.group(0)[4:]
        except AttributeError:
            port = 'Failed to find port'

        # traceroute = 'example traceroute output'# os.popen('traceroute %s' % src).read()

        data.append({
            'type': search_term,
            'date': date,
            'src': src,
            'port': port,
        })
    return data

def traceroute(src):
    print('Running traceroute for %s' % src)
    return os.popen('traceroute %s -m 5' % src).read()

def GetTemp():
    #
    logs = os.popen('sensors -u | grep \'temp[0-9]_input\'').read()

    logs = logs.split('\n')

    temps = []
    # Finding temperature from sensors output
    for x in logs:
        if x != '':
            y = re.search(r'\d{1,3}\.\d+$', x)
            temps.append(float(y.group(0)))

    # Getting average temperature from CPU sources
    return str(sum(temps) / float(len(temps)))

def GetBattery():
    return os.popen('upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | rev | cut -d\' \' -f1 | rev').read()[:-1]

def GetHostname():
    return os.popen('hostname').read()[:-1]

def AnalyzeDirectory(dir, includeHidden=False):

    all_files = fo.recurse_get_files(dir, includeHidden=includeHidden)

    # Inefficient method of removing unwanted directories, if runs to
    # slow or will be ran often,
    # add ignore funtionality when searching for files

    all_files = fo.get_file_info(all_files)
    p.print_json(all_files)

if __name__ == '__main__':
    AnalyzeDirectory('/home/fargus/Projects/ThreadingTesting')
