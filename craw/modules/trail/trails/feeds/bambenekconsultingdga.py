#!/usr/bin/env python2

"""
Copyright (c) 2014-2019 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

import os
import re
import subprocess
from tempfile import TemporaryDirectory

__url__ = "https://osint.bambenekconsulting.com/feeds/dga-feed.txt"
__check__ = "Domain used by"
__reference__ = "bambenekconsulting.com"
maintainer_url = "bambenekconsulting.com"
maintainer = "John Bambenek of Bambenek Consulting"
list_source_url = __url__
category = "DGA domains"
NAME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"


def fetch():
    retval = {}
    # handle = retrieve_content(__url__)

    with TemporaryDirectory() as dirname:
        retcode = subprocess.Popen(["wget", "-P", dirname, __url__])
        retcode.wait()
        file_name = os.path.join(dirname, 'dga-feed.txt')
        handle = open(file_name)
        if handle:
            try:
                while True:
                    line = handle.readline()
                    if not line:
                        break
                    match = re.search(r"\A([^,\s]+),Domain used by ([^ ]+)", line)
                    if match and '.' in match.group(1):
                        retval[match.group(1)] = ("%s dga (malware)" % match.group(2).lower(), __reference__)
            except:
                pass

    return retval


if __name__ == '__main__':
    fetch()
