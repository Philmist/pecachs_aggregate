#!/usr/bin/python

import count
import operator
from datetime import datetime

if __name__ == "__main__":
    result = []
    dt_now = datetime.now()
    now_str = r"{0:%y}{0:%m}{0:%d}_{0:%H}{0:%M}".format(dt_now)
    yps = [
            { "name": "SP", "url": r"http://bayonet.ddo.jp/sp/" },
            { "name": "TP", "url": r"http://temp.orz.hm/yp/" }
            ]
    for i in yps:
        result.extend(count.parse_indextxt(i["url"]))
        with open("index_" + i["name"] + "_" + now_str + ".txt", "w") as f:
            count.write_indextxt(f, i["url"])
    with open("host_" + now_str + ".txt", "w") as f:
        for i in result:
            f.write(i[0] + "\n")
    c = count.count_hosts(result)
    with open("count_" + now_str + ".txt", "w") as f:
        for k, v in sorted(c.items(), key=operator.itemgetter(1), reverse=True):
            f.write("{}, {}\n".format(k, v))

