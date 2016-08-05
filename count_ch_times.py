#!/usr/bin/python3
"""
配信のファイル一覧をとりこみ、
チャンネルの配信時間(1時間単位)を集計するスクリプトです。
"""

import fileinput
import re

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
    戻り値:  [
                "YP": YP名,
                "YEAR": 年(数値),
                "MONTH": 月(数値),
                "HOUR": 時(24時間制 数値),
                "MINUTE": 分(数値)
            ]
    """
    match = FILE_PATTERN.search(filename)
    result = {
        "YP": match.group("YP"),
        "YEAR": int(match.group("YEAR")),
        "MONTH": int(match.group("MONTH")),
        "HOUR": int(match.group("HOUR")),
        "MINUTE": int(match.group("MINUTE"))
        }
    return result

if __name__ == "__main__":
    # コマンドラインからファイルの一覧を取りこんで
    # 順番に開いていく
    with fileinput.input() as f:
        # 順番に行を読みこんでいくけれど…
        for line in f:
            # もし読みこんだ行が標準入力からだったのなら
            if f.isstdin():
                # 次のファイルへスキップする(無いかもしれないけど)
                f.nextfile()
            elif f.isfirstline():
                print(parse_filename(f.filename()))
