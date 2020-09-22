#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import re

from craw.modules.trail.plugins.util import wget_content

__url__ = "https://data.netlab.360.com/feeds/dga/chinad.txt"
__check__ = "netlab 360"
__info__ = "chinad dga (malware)"
__reference__ = "360.com"
maintainer_url = "360.com"
maintainer = "netlab 360"
list_source_url = __url__
category = __info__


def fetch():
    retval = {}
    content = wget_content(__url__)

    if __check__ in content:
        for match in re.finditer(r"(?m)^([\w.]+)\s+2\d{3}\-", content):
            retval[match.group(1)] = (__info__, __reference__)

    return retval
