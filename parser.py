#!/usr/bin/python3
"""
index.txtで色々するモジュールです。
"""

import socket
import httplib2
import re
import operator
import datetime

http_client = httplib2.Http(".cache")

def httpget_plaintxt(url):
    """
    urlからプレーンテキストを読みとります。
    読みこむ際のサーバ応答のヘッダにContent-Typeがついており、
    charsetがないと正常に動作しません。

    @retval 文字列(str)
    """
    (headers, content) = http_client.request(url, "GET")
    if "text/plain" not in headers["Content-Type"]:
        raise ValueError("Content-type is not text/plain")
    result = []
    encoding_match = re.search(r"charset=(?P<charset>\S+)", headers["Content-Type"])
    encoding_string = re.group("charset")
    return content.decode(encoding_string)


def parse_indextxt_line(line):
    """
    渡されたindex.txt由来のlineを分割して辞書として返します。

    キー文字列と値の対応は以下のとおり。
    'ch_name': チャンネル名
    'channel_id': チャンネル固有のID
    'ipaddr': 配信者のIPアドレスとポート
    'contact_url': コンタクトURL
    'genre': ジャンル
    'detail': 詳細(index.txtではhttpでの文字指定がされています)
    'listener': リスナー数(負の値あるいはNoneを取ることがあります)
    'relay': リレー数(負の値あるいはNoneを取ることがあります)
    'bit_rate': ビットレート[kbps](数値)
    'type': 配信コンテナの種別(FLV, MKV, WMVなど)
    'track_artist': トラックアーティスト
    'track_album': トラックアルバム
    'track_contacturl': トラックコンタクトURL
    'uptime': 配信時間(datetime.timedelta)
    'comment': コメント
    """
