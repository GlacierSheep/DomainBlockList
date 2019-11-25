#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

from craw.modules.trail.plugins.util import wget_content

__url__ = "https://raw.githubusercontent.com/Hestat/minerchk/master/hostslist.txt"
__check__ = ".com"
__info__ = "crypto mining (suspicious)"
__reference__ = "github.com/Hestat"

maintainer_url = __reference__
maintainer = "Hestat"
list_source_url = __url__
category = __info__


def fetch():
    retval = {}
    content = wget_content(__url__)

    if __check__ in content:
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or '.' not in line:
                continue
            retval[line] = (__info__, __reference__)

    return retval
