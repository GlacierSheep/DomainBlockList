# -*- coding: utf-8 -*-

"""
@author: Glacier

@contact: me@xuluhang.cn

@Created on: 2019/11/20 20:13
"""

import os
import sys
import time

from git import Repo
from loguru import logger
from modules.trail import sensor
from modules.trail.plugins import util as util
from pyfiglet import figlet_format
from termcolor import cprint

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
            # update.main()
            print('[i] Update Finished!')
            repo = Repo(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            repo.index.add('.')
            repo.index.commit('Test')
            origin = repo.remote('origin')
            origin.push()
            time.sleep(3600)

        except:
            util.wxpush('Crawl', 'Error！', True)
            logger.exception("syn_main")


if __name__ == "__main__":
    run()
