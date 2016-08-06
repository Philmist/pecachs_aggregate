#!/usr/bin/python3

from scripts.yp_libs import yp_parser
from natto import MeCab


if __name__ == "__main__":
    idxtxt = yp_parser.httpget_plaintxt(r"http://bayonet.ddo.jp/sp/index.txt")
    idxlist = [yp_parser.parse_indextxt_line(line)
               for line in idxtxt.splitlines()]
    with MeCab("-d /usr/lib/mecab/dic/mecab-ipadic-neologd") as nm:
        for i in idxlist:
            print("----")
            print("Ch name : " + i["ch_name"])
            print("Genre : " + i["genre"])
            print("Original : " + i["detail"])
            try:
                tokenized = nm.parse(i["detail"], as_nodes=True)
                print("Tokenized to:")
                for j in tokenized:
                    if j.is_nor():
                        print(str(j.surface) + ", ", end="")
                    else:
                        print(str(j.surface) + "(UNK), ", end="")
                print("")
            except IndexError:
                print("Cannot tokenized : " + i["detail"])
