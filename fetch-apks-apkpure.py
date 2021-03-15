#!/bin/python 
from lxml import html
import urllib.request
import requests
import os
import multiprocessing
from http.cookiejar import CookieJar
import shutil
import sys

def download_apk(packageName, dst='.'):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'referer' : 'https://apkpure.com/apkpure/{}/download?from=details'.format(packageName),
    }
    urlFormat = 'https://apkpure.com/apkpure/{}/download?from=details'.format(packageName)
    #print(f"1st url:{urlFormat}")
    r = requests.get(urlFormat, headers=headers)
    tree = html.fromstring(r.content)
    downloadUrl = tree.xpath('//*[@id="download_link"]/@href')[0]
    #print(downloadUrl)

    with (requests.get(downloadUrl, stream=True)) as r:
        with open(f'{dst}/{packageName}.apk', 'wb') as f:
            shutil.copyfileobj(r.raw, f)

if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print("Usage: python fetch-apks-apkpure.py packageName [dstFolder]")
    exit(-1)

try:
    dst = sys.argv[2] if len(sys.argv) == 3 else '.'
    download_apk(sys.argv[1], dst)
    print(f"Downloaded {sys.argv[1]}")
except:
    print(f"Error downloading {sys.argv[1]}. Is the package name correct? Does it exist in apkpure.com?")
    exit(-1)
