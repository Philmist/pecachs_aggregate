#!/usr/bin/python3
"""
詳細などを分割するモジュールです。
"""

import pathlib
import rakutenma

RMA_MODELFILE = pathlib.Path(__file__).parent.joinpath("rakutenma/model_ja.json")
rma = rakutenma.RakutenMA()
rma.load(str(RMA_MODELFILE))
