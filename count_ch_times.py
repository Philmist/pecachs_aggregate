#!/usr/bin/python3
"""
配信のファイル一覧をとりこみ、
チャンネルの配信履歴を集計するスクリプトです。
"""

from datetime import datetime
import fileinput
from glob import glob
import numpy as np
import pandas as pd
import pickle
import re
import sys

from yp_libs.yp_parser import parse_indextxt_line

FILE_PATTERN = re.compile("""
.*_                 # プレフィックス
(?P<YP>.+)          # YP名
_                   # 区切り
(?P<YEAR>\d{2})     # 年(2桁)
(?P<MONTH>\d{2})    # 月(2桁)
(?P<DAY>\d{2})      # 日(2桁)
_                   # 区切り
(?P<HOUR>\d{2})     # 時(2桁)
(?P<MINUTE>\d{2})   # 分(2桁)
.*                  # サフィックス(拡張子等)
""", re.VERBOSE)


def parse_filename(filename):
    """ファイル名を解析して、各種情報を返します。

    filename: 解析したいファイル名
    戻り値:  {
                "YP": YP名(str),
                "DATETIME": 日時(datetime)
            }
    """
    match = FILE_PATTERN.search(filename)
    result = {
        "YP": match.group("YP"),
        "DATETIME": datetime(
            int("20" + match.group("YEAR")),
            int(match.group("MONTH")),
            int(match.group("DAY")),
            int(match.group("HOUR")),
            int(match.group("MINUTE"))
        )
    }
    return result

if __name__ == "__main__":
    # チャンネルを入れる辞書を初期化
    ch_list = dict()
    # コマンドラインからファイルの一覧を取りこんで
    # 順番に開いていく
    # see: http://stackoverflow.com/questions/21731097/how-to-pass-wildcard-argument-like-txt-in-windows-cmd
    all_files = [f for files in sys.argv[1:] for f in glob(files)]
    if len(all_files) <= 1:
        sys.exit(1)
    with fileinput.input(all_files, openhook=fileinput.hook_encoded("utf-8")) as f:
        # 変数を初期化
        current_file_datetime = datetime.today()
        # 順番に行を読みこんでいくけれど…
        for line in f:
            # もし読みこんだ行が標準入力からだったのなら
            if f.isstdin():
                # 次のファイルへスキップする(無いかもしれないけど)
                f.nextfile()
                continue
            # もし読みこんだのが最初の行だったら
            if f.isfirstline():
                # ファイル名から日時を設定する
                current_file_datetime = parse_filename(f.filename())
            # 配信を読みこむ
            try:
                bcst = parse_indextxt_line(line)
            except ValueError:
                continue
            # もしチャンネルが無いのなら
            if not bcst['ch_name'] in ch_list:
                # 新しくリストを作っておく
                ch_list[bcst['ch_name']] = list()
            # リストに配信を追加する
            bcst["datetime"] = current_file_datetime["DATETIME"]
            bcst["yp"] = current_file_datetime["YP"]
            ch_list[bcst['ch_name']].append(bcst)

    # チャンネルを時間順にソート
    for k in ch_list.keys():
        ch_list[k].sort(key=lambda x: x["datetime"],
                        reverse=True)

    # チャンネルの配信時間を計算する
    ch_time = dict()
    for key, value in ch_list.items():
        ch_time[key] = list()
        for n, v in enumerate(value):
            pass
