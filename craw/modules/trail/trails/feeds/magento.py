#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

from modules.trail.plugins.util import wget_content

__url__ = "https://raw.githubusercontent.com/gwillem/magento-malware-scanner/master/rules/burner-domains.txt"
__check__ = ".com"
__info__ = "magento (malware)"
__reference__ = "github.com/gwillem"

maintainer_url = __reference__
maintainer = "gwillem"
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
