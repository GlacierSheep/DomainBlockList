#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import re

from craw.modules.trail.plugins.util import wget_content

__url__ = "https://osint.bambenekconsulting.com/feeds/c2-dommasterlist-high.txt"
__check__ = "Master Feed"
__reference__ = "bambenekconsulting.com"
maintainer_url = "bambenekconsulting.com"
maintainer = "Master Feed"
list_source_url = __url__
category = 'c2'


def fetch():
    retval = {}
    content = wget_content(__url__)

    if __check__ in content:
        for match in re.finditer(r"(?m)^([^,#]+),Domain used by ([^,/]+)", content):
            retval[match.group(1)] = ("%s (malware)" % match.group(2).lower().strip(), __reference__)

    return retval
