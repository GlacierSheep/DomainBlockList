#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: Glacier

@contact: me@xuluhang.cn

@Created on: 2019/10/30 20:49
"""

import os
import os.path
import shutil
from tempfile import TemporaryDirectory

from pyfiglet import figlet_format
from termcolor import cprint


def StartTrailer():
    os.system("clear")
    cprint(figlet_format(('Peeker!').center(12), font='starwars'),
           'red', attrs=['bold'])


def run():
    path = 'https://github.com/stamparm/maltrail.git'
    import git
    with TemporaryDirectory() as dirname:
        git.Repo.clone_from(url=path, to_path=dirname, depth=1)
        copytree(dirname + '/trails/static/malware', './craw/modules/trail/trails/static/malware')
        copytree(dirname + '/trails/static/suspicious', './craw/modules/trail/trails/static/suspicious')


def copytree(src, dst, symlinks=False):
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except OSError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)


def main():
    run()
