#!/usr/bin/python
# vim: fileencoding=utf-8

import socket
import httplib2
import re
import operator

http_client = httplib2.Http(".cache")

def parse_indextxt(url):
    (headers, content) = http_client.request(url + str(r"index.txt"), "GET")
    result = []
    lines = content.decode("utf-8").splitlines()
    for n, i in enumerate(lines):
        # print(str(i).split("<>")[2])
        # print("{0}/{1}".format(n+1, len(lines)))
        r = re.search(r"(.+):.*", i.split("<>")[2])
        if r is None:
            continue
        addr = r.group(1)
        try:
            host = socket.gethostbyaddr(addr)
        except (socket.gaierror, OSError, ValueError, socket.herror):
            continue
        result.append(host)
    return result

def count_hosts(hosts):
    c = {}
    r_2 = re.compile(r".+\.(.+\..+\..{2})$")
    r_3 = re.compile(r".+\.(.+\..{3})$")
    for i in hosts:
        g = r_2.search(i[0])
        if g is None:
            g = r_3.search(i[0])
        if g is None:
            continue
        if not g.group(1) in c:
            c[g.group(1)] = 1
        else:
            c[g.group(1)] += 1
    return c

def write_indextxt(stream, url):
    (headers, content) = http_client.request(url + str(r"index.txt"), "GET")
    stream.write(content.decode("utf-8"))

if __name__ == "__main__":
    result = []
    yps = [
            {
                "name": "SP",
                "url": r"http://bayonet.ddo.jp/sp/"
            },
            {
                "name": "TP",
                "url": r"http://temp.orz.hm/yp/"
            }
        ]
    for i in yps:
        result.extend(parse_indextxt(i["url"]))
        with open(i["name"]+"_index.txt", "w") as f:
            write_indextxt(f, i["url"])
    f = open("host.txt", "w")
    for i in result:
        print(i)
        f.write(i[0] + "\n")
    c = count_hosts(result)
    fc = open("count.txt", "w")
    for k, v in sorted(c.items(), key=operator.itemgetter(1), reverse=True):
        fc.write("{}, {}\n".format(k, v))

