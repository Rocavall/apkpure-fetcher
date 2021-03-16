#!/bin/python 
from lxml import html
import urllib.request
import requests
import os
import multiprocessing
from http.cookiejar import CookieJar
import shutil
import sys
import re

def get_download_ext(filename):
    filename = re.match(r"attachment; filename=\"(.*?)\"", filename, flags=0).group(1)
    if filename.endswith('.apk'):
        return 'apk'
    elif filename.endswith('.xapk'):
        return 'xapk'
    else:
        raise ValueError(f'File extension \'{filename.split(".")[-1]}\'not recognized')

def download_apk(packageName, dst='.'):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'referer' : 'https://apkpure.com/apkpure/{}/download?from=details'.format(packageName),
    }
    urlFormat = 'https://apkpure.com/apkpure/{}/download?from=details'.format(packageName)
    r = requests.get(urlFormat, headers=headers)
    tree = html.fromstring(r.content)
    downloadUrl = tree.xpath('//*[@id="download_link"]/@href')[0]

    with (requests.get(downloadUrl, stream=True)) as r:
        filename = r.headers["Content-Disposition"]
        outPath = f'{dst}/{packageName}.{get_download_ext(filename)}'
        with open(outPath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return outPath

if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print("Usage: python fetch-apks-apkpure.py packageName [dstFolder]")
    exit(-1)

try:
    dst = sys.argv[2] if len(sys.argv) == 3 else '.'
    outPath = download_apk(sys.argv[1], dst)
    print(f"Downloaded {sys.argv[1]} into {outPath}")
except Exception as e:
    print(f"Error downloading {sys.argv[1]}. Is the package name correct? Does it exist in apkpure.com?")
    print(f"Exception: {e}")
    exit(-1)
