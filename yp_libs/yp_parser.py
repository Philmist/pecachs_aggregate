#!/usr/bin/python3
"""
index.txtで色々するモジュールです。
"""

import httplib2
import re
import datetime
import ipaddress
from xml.sax.saxutils import unescape

http_client = httplib2.Http(".cache")


def httpget_plaintxt(url):
    """
    urlからプレーンテキストを読みとります。
    読みこむ際のサーバ応答のヘッダにContent-Typeがついており、
    charsetがないと正常に動作しません。

    @retval 文字列(str)
    """
    (headers, content) = http_client.request(url, "GET")
    if "text/plain" not in headers["content-type"]:
        raise ValueError("content-type is not text/plain")
    encoding_match = re.search(r"charset=(?P<charset>\S+)",
                               headers["content-type"])
    encoding_string = encoding_match.group("charset")
    return content.decode(encoding_string)


def parse_indextxt_line(line):
    """
    渡されたindex.txt由来のlineを分割して辞書として返します。

    キー文字列と値の対応は以下のとおり。
    'ch_name': チャンネル名
    'channel_id': チャンネル固有のID
    'ipaddr': 配信者のIPアドレス
    'ipport': 配信者が使用しているポート
    'contact_url': コンタクトURL
    'genre': ジャンル
    'detail': 詳細(index.txtではhttpでの文字指定がされています)
    'listener': リスナー数(負の値あるいはNoneを取ることがあります)
    'relay': リレー数(負の値あるいはNoneを取ることがあります)
    'bitrate': ビットレート[kbps](数値)
    'type': 配信コンテナの種別(FLV, MKV, WMVなど)
    'track_artist': トラックアーティスト
    'track_album': トラックアルバム
    'track_title': トラックタイトル
    'track_contacturl': トラックコンタクトURL
    'uptime': 配信時間(datetime.timedelta)
    'comment': コメント
    """
    # 使用する正規表現
    ipaddr_regex = re.compile(r"(?P<addr>.+):(?P<port>.+)")
    uptime_regex = re.compile(r"(?P<hour>.+):(?P<min>.+)")
    # 項目の分割
    splited = str(line).split("<>")
    # 分割数確認
    if not len(splited) == 19:
        raise ValueError("Invalid data")
    # 結果
    result = dict()
    result['ch_name'] = str(splited[0])
    result['channel_id'] = str(splited[1])
    ipaddr_match = ipaddr_regex.search(splited[2])
    if ipaddr_match is not None:
        result['ipaddr'] = ipaddress.ip_address(ipaddr_match.group("addr"))
        result['ipport'] = int(ipaddr_match.group("port"))
    else:
        result['ipaddr'] = None
        result['ipport'] = None
    result['contact_url'] = str(splited[3])
    result['genre'] = str(splited[4])
    result['detail'] = str(unescape(splited[5]))
    result['listener'] = int(splited[6])
    result['relay'] = int(splited[7])
    result['bitrate'] = int(splited[8])
    result['type'] = str(splited[9])
    result['track_artist'] = str(splited[10])
    result['track_album'] = str(splited[11])
    result['track_title'] = str(splited[12])
    result['track_contacturl'] = str(splited[13])
    uptime_match = uptime_regex.search(splited[15])
    if uptime_match is not None:
        result['uptime'] = datetime.timedelta(
            minutes=int(uptime_match.group("min")),
            hours=int(uptime_match.group("hour"))
            )
    else:
        result['uptime'] = None
    result['comment'] = str(splited[17])
    # 戻り値
    return result
