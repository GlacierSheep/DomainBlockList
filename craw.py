# -*- coding: utf-8 -*-

"""
@author: Glacier

@contact: me@xuluhang.cn

@Created on: 2019/11/20 20:13
"""

import os
import subprocess
import sys
import time

from loguru import logger
from pyfiglet import figlet_format
from termcolor import cprint

import craw.modules.trail.plugins.update as myupdate
from craw.modules.trail import sensor
from craw.modules.trail.plugins import util as util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FIL = os.path.basename(os.path.abspath(__file__))
log_file_path = os.path.join(BASE_DIR, 'Log', BASE_FIL.replace('.py', '') + 'file_{time}.Log')
err_log_file_path = os.path.join(BASE_DIR, 'Log', BASE_FIL.replace('.py', '') + 'err.Log')
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(log_file_path, enqueue=True, rotation="1 days", encoding='utf-8')  # Automatically rotate too big file
logger.add(err_log_file_path, enqueue=True, rotation="500 MB", encoding='utf-8', backtrace=True, diagnose=True,
           level='ERROR')


def StartTrailer():
    os.system("clear")
    cprint(figlet_format(('Peeker!').center(12), font='starwars'),
           'red', attrs=['bold'])


def run():
    while (True):
        try:
            my_craw = sensor.My_Craw()
            my_craw.update_trails()
            print('[i] Craw Finished!')
            myupdate.main()
            print('[i] Syn Finished!')
            subprocess.call(["git", "add", "."])
            subprocess.call(
                ["git", "commit", "-m", "auto push at " + time.asctime(time.localtime(time.time()))])  # 加上当前系统的时间
            subprocess.call(["git", "push"])
            # repo = Repo(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # changes = [item.a_path for item in repo.index.diff(None)]
            # print(changes)
            # repo.index.add(changes)
            # repo.index.commit(time.asctime(time.localtime(time.time())))
            # origin = repo.remote('origin')
            # origin.push()
            print('[i] Push Finished!')
            print('[i] Sleep 3600')
            time.sleep(3600)

        except:
            util.wxpush('Crawl', 'Error！', True)
            logger.exception("syn_main")


if __name__ == "__main__":
    run()
