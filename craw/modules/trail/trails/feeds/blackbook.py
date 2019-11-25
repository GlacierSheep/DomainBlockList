#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import requests

__url__ = "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.csv"
__check__ = "Malware"
__reference__ = "github.com/stamparm/blackbook"
maintainer_url = __reference__
maintainer = "Stamparm"
list_source_url = __url__
category = __check__


def fetch():
    retval = {}

    content = requests.get(__url__).text

    if __check__ in content:
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or '.' not in line:
                continue
            retval[line.split(',')[0].strip()] = ("%s (malware)" % line.split(',')[1].strip(), __reference__)

    return retval
