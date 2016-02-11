#!/usr/bin/python3
"""
詳細などを分割するモジュールです。
"""

import json


class GameSearcher(object):

    """
    渡されたリストの中からある特定の単語が含まれているかどうかを
    チェックするためのクラスです。
    """

    def __init__(self, jsonfp):
        """
        jsonfpからJSONを読みこみ、
        単語リストを構築します。

        JSONは以下の形式でなければなりません。
        {"分類1": ["単語1", "単語2", ...], "分類2": [ ... ], ... }
        """
        self._orig_data = json.load(jsonfp)
        if not isinstance(self._orig_data, dict):
            raise ValueError("Given json data is not valid")
        self.conv_dict = dict()
        for k, v in self._orig_data.items():
            for i in v:
                self.conv_dict[i] = k

    def search_group_from_sentence(self, sentence):
        """
        渡された文から分類のリストを返します。
        """
        result = [self.conv_dict[k]
                  for k in self.conv_dict.keys()
                  if k in sentence]
        return result
