#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__date__ = '2025/01/10'

import requests
import numpy as np
import matplotlib.pyplot as plt

"""
niconicoURLリストから楽曲全体のBPMの標準偏差を求めヒストグラム化するプログラム
※リクエスト過多にならないよう注意
"""

def main():
    """SongleAPIを利用し、分析する"""

    # テキストからリストに変換
    base_url = "https://widget.songle.jp/api/v1/song/beat.json?url="
    with open('url_list.txt', 'r') as file:
        urls = [base_url + line.strip() for line in file.readlines()]
    
    # 楽曲ごとの標準偏差を求める
    aves = []
    stds = []
    url_and_std = {}
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 404:
                continue
        except Exception as e:
            print(e)
            continue
        beats = response.json()['beats']
        bpms = []
        for beat in beats:
            bpms.append(beat['bpm'])
        ave = np.mean(bpms)
        std = np.std(bpms)

        aves.append(ave)
        stds.append(std)
        url_and_std[url] = std
        print(url)
        print(f'age: {ave}')
        print(f'std: {std}')
    print(stds)

    # ヒストグラムを作成
    # 今回はbins=7としている
    bins = 7
    plt.hist(stds, bins=bins)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')
    plt.show()



    # ヒストグラムを計算
    bin_counts, bin_edges = np.histogram(stds, bins=bins)

    # 各ビンに含まれるデータを抽出
    bin_values = []
    for i in range(bins):
        # 各ビンの範囲に含まれるデータを抽出
        bin_data = [d for d in stds if bin_edges[i] <= d < bin_edges[i + 1]]
        bin_values.append(bin_data)

    # 各ビンのデータを表示
    with open('histgram.txt', 'w') as file:
        for i, bin_data in enumerate(bin_values):
            print(f"ビン {i+1}: {bin_data}")
            file.write(f"ビン {i+1}\n")
            for datum in bin_data:
                matching_urls = [url for url, std in url_and_std.items() if std == datum]
                for url in matching_urls:
                    file.write(f"{url}\n")

if __name__ == "__main__":
    import sys
    sys.exit(main())