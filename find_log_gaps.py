#!/usr/bin/python3

import datetime
import os
import re
import sys

filepath = sys.argv[1]

class Gap(object):
    def __init__(self, duration, current_line, last_line):
        self.duration = duration
        self.current_line = current_line
        self.last_line = last_line

regex = re.compile('^(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d\d\d)\s')
last = None
maxt = datetime.timedelta(0)
top5 = []

with open(filepath) as fp:
    for line in fp:
        r = regex.match(line)
        if r:
            dt = datetime.datetime.strptime(r.group(1), '%Y-%m-%dT%H:%M:%S.%f')
            if last:
                duration = dt-last
                if len(top5) < 5:
                    top5.append(Gap(duration, line, lastline))
                else:
                    durations = [x.duration for x in top5]
                    mind = min(durations)
                    if duration > mind:
                        top5.append(Gap(duration, line, lastline))
                top5 = sorted(top5, key=lambda i:i.duration, reverse=True)[:5]
            last = dt
            lastline = line

print('Five longest time gaps identified:')
for gap in top5:
    print('Duration: {}'.format(gap.duration))
    print('Log lines (n and n-1):')
    print(gap.last_line)
    print(gap.current_line)
    print('%%%%%%%%%%%%%%')
