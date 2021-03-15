#!/bin/bash
cat apk-list.txt | while read pkg
do
    python fetch-apks-apkpure.py $pkg download/ &
done
