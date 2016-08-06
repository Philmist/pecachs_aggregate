#!/usr/bin/python3

import sys
from scripts.yp_libs import yp_parser, game_searcher


def search_tag(idxlist):
    with open(r"scripts/yp_libs/gamelist/pecalist.json",
              mode="r",
              encoding="utf-8") as f:
        gs = game_searcher.GameSearcher(f)
        gamedict = {i["ch_name"]:
                    {"tag": gs.search_group_from_sentence(i["detail"]
                                                          + i["genre"]),
                     "orig": (i["detail"] + " " + i["genre"])}
                    for i in idxlist if i["listener"] > -2}
    return gamedict


if __name__ == "__main__":
    if True:
        idxtxt = yp_parser.httpget_plaintxt(
            r"http://bayonet.ddo.jp/sp/index.txt")
        idxlist = [yp_parser.parse_indextxt_line(line)
                   for line in idxtxt.splitlines()]
        gamedict = search_tag(idxlist)
        for k, v in gamedict.items():
            print("CH: " + str(k))
            print("TAG: " + str(v["tag"]))
            print("ORIG: " + str(v["orig"]))
            print("----")
    else:
        unknown_set = set()
        idxlist = [yp_parser.parse_indextxt_line(line)
                   for line in sys.stdin.readlines()]
        for k, v in search_tag(idxlist).items():
            if len(v["tag"]) == 0:
                unknown_set.add(v["orig"])
        for i in unknown_set:
            print(i)
