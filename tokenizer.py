#!/usr/bin/python3
"""
詳細などを分割するモジュールです。
"""

import pathlib
import rakutenma

RMA_MODELFILE = pathlib.Path(__file__).parent.joinpath("rakutenma/model_ja.json")
rma = rakutenma.RakutenMA()
rma.load(str(RMA_MODELFILE))


def train_from_list(train_list):
    for sentence in train_list:
        rma.train_one(sentence)


TRAIN_LIST = [
        [["&lt;", "E"]],
        [["&gt;", "E"]],
        ]
train_from_list(TRAIN_LIST)
