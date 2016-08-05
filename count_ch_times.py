#!/usr/bin/python3
"""
配信の一覧をとりこみ、
チャンネルの配信時間(1時間単位)を集計するスクリプトです。
"""

import fileinput

if __name__ == "__main__":
    with fileinput.input() as f:
        for line in f:
            if f.isfirstline():
                print(f.filename())
