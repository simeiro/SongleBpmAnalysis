#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__date__ = '2025/01/10'

import requests
import matplotlib.pyplot as plt

"""
SongleAPIのBPM情報からヒストグラムを表示するプログラム
"""

URL = "https://widget.songle.jp/api/v1/song/beat.json?url=http://www.nicovideo.jp/watch/sm44194393"

def main():
    try:
        response = requests.get(URL)
        if response.status_code == 404:
            exit()
    except Exception as e:
        print(e)
        exit()
    beats = response.json()['beats']
    bpms = []
    for beat in beats:
        bpms.append(beat['bpm'])
    
    plt.hist(bpms, bins=10)
    plt.xlabel('BPM')
    plt.ylabel('Frequency')
    plt.ylim(0, 700)
    plt.title('Histogram of Data')
    plt.show()
    

if __name__ == "__main__":
    import sys
    sys.exit(main())