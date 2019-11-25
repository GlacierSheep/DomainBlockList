#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import re

from craw.modules.trail.plugins.util import wget_content

__url__ = "https://openphish.com/feed.txt"
__check__ = "http://"
__info__ = "phishing"
__reference__ = "openphish.com"

maintainer_url = __reference__
maintainer = __check__
list_source_url = __url__
category = __info__


def fetch():
    retval = {}
    content = wget_content(__url__)

    if __check__ in content:
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '://' in line:
                line = re.search(r"://(.*)", line).group(1)
            line = line.rstrip('/')
            retval[line] = (__info__, __reference__)

    return retval
