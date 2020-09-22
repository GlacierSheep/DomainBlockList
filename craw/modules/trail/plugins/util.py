# -*- coding: utf-8 -*-

"""
@author: Glacier

@contact: me@xuluhang.cn

@Created on: 2019/11/13 20:22
"""
import datetime
import json
import os
import subprocess
import traceback
from tempfile import TemporaryDirectory

import pandas as pd
import requests


def wget_content(url):
    """
    Retrieves page content from given URL
    """

    try:

        for i in range(len(url)):
            url[i].replace(' ', "%20") if i > url.find('?') else url[i]

        with TemporaryDirectory() as dirname:
            retval = ''
            retcode = subprocess.Popen(["wget", "--tries=5", '--timeout=10', url, "-O", os.path.join(dirname, "1.txt")])
            retcode.wait()
            file_name = os.path.join(dirname, "1.txt")
            handle = open(file_name)
            if handle:
                retval = handle.read()


    except Exception as ex:
        if url.startswith("https://") and "handshake failure" in retval:
            return wget_content(url.replace("https://", "http://"))
        else:
            wxpush("Crawler module failure", traceback.extract_stack(), True)

    return retval or ""


def hebing(csv_list, outputfile):
    for inputfile in csv_list:
        f = open(inputfile)
        try:
            data = pd.read_csv(f)
            data.to_csv(outputfile, mode='a', index=False, header=None)
        except:
            print("[x] A csv file is empty!")
    print("[i] Merger Completed!")


def quchong(file, file1):
    df = pd.read_csv(file, header=0, error_bad_lines=False)
    df.columns = ['A', 'B', 'C']
    datalist = df.drop_duplicates(['A', 'C'], keep='first')
    datalist.to_csv(file1, index=False, header=None)
    print('[i] De-duplication Completed!')


def getYesterday():
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return str(yesterday)


def wxpush(title, content, option):
    if option:
        baychat = 'https://hook.bearychat.com/=bwHAy/incoming/4babc554d32edcc1f16742ff8005e975'
        request_data = {
            "text": title,
            "attachments": [
                {
                    "title": title,
                    "text": content,
                    "color": "#ffa500",
                    "images": [{"url": "http://i1.fuimg.com/661719/4e7f8e384e2ff9fc.png"}]
                }
            ]
        }

        header = {'Content-Type': 'application/json'}
        req = requests.post(url=baychat,
                            headers=header,
                            data=json.dumps(request_data).encode("utf-8"))
    else:
        print('fault')
