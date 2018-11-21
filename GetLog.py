#!/usr/bin/python3.6

import os
import re


def GetLog(search, lines=200):
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


        try:
            date = date.group(0)
        except AttributeError:
            date = 'NO DATE FOUND'

        try:
            src = src.group(0)[4:]
        except AttributeError:
            # if there is no src it was not a ufw block rule
            continue

        data.append({
            'type': search_term,
            'date': date,
            'src': src
        })


    return data




