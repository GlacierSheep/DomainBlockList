#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import re

from modules.trail.plugins.util import wget_content

__url__ = "https://rules.emergingthreats.net/open/suricata/rules/emerging-dns.rules"
__check__ = "Emerging Threats"
__info__ = "malware"
__reference__ = "emergingthreats.net"
maintainer_url = __reference__
maintainer = __check__
list_source_url = __url__
category = __info__


def fetch():
    retval = {}
    content = wget_content(__url__)

    if __check__ in content:
        for match in re.finditer(r"(?i)C2 Domain \.?([^\s\"]+)", content):
            retval[match.group(1)] = (__info__, __reference__)

    return retval
