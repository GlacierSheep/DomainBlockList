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
log_file_path = os.path.join(BASE_DIR, 'log', BASE_FIL.replace('.py', '') + 'file_{time}.log')
err_log_file_path = os.path.join(BASE_DIR, 'log', BASE_FIL.replace('.py', '') + 'err.log')
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(log_file_path, enqueue=True, rotation="1 days", encoding='utf-8')  # Automatically rotate too big file
logger.add(err_log_file_path, enqueue=True, rotation="500 MB", encoding='utf-8', backtrace=True, diagnose=True,
           level='ERROR')


def StartTrailer():
    os.system("clear")
    cprint(figlet_format(('Peeker!').center(12), font='starwars'),
           'red', attrs=['bold'])


def run():
    round_num = 0
    while (True):
        try:
            StartTrailer()
            logger.info('[i] ' + str(round_num) + ' Round craw begin!')
            my_craw = sensor.My_Craw()
            my_craw.update_trails()
            logger.info('    [i] ' + str(round_num) + ' Round craw finished!')
            logger.info('    [i] ' + str(round_num) + ' Round syn begin!')
            myupdate.main()
            logger.info('    [i] ' + str(round_num) + ' Round syn finished!')
            logger.info('    [i] ' + str(round_num) + ' git push begin!')
            subprocess.call("cd " + BASE_DIR + "&& git add .", shell=True)
            subprocess.call(
                "cd " + BASE_DIR + " && git commit -m 'auto push at " + time.asctime(
                    time.localtime(time.time())) + "'", shell=True)  # 加上当前系统的时间
            subprocess.call("cd " + BASE_DIR + "&& git gc --prune=now", shell=True)
            subprocess.call("cd " + BASE_DIR + "&& git push github master", shell=True)
            subprocess.call("cd " + BASE_DIR + "&& git push coding master", shell=True)
            logger.info('    [i] ' + str(round_num) + ' git push finished!')
            logger.info('[i] ' + str(round_num) + ' Round finished! Sleep 3600 sec')
            round_num += 1
            try:
                util.wxpush('Crawl.service Log', '第' + str(round_num) + '轮DomainBlockList爬取服务结束！一切正常', True)
            except:
                logger.exception("wxpush")
            time.sleep(21600)

        except:
            util.wxpush('Crawl.service Error Log', '在第' + (round_num) + '轮DomainBlockList爬取服务发生错误！请管理员叙述查证！', True)
            logger.exception("Main")


if __name__ == "__main__":
    run()
