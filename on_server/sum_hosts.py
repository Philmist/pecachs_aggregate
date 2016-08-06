#!/usr/bin/python
# vim: fileencoding=utf-8

from pathlib import Path
import csv
import re
import operator

def read_csv(f):
    reader = csv.reader(f)
    result = dict()
    for row in reader:
        if not len(row) == 2:
            continue
        result[row[0]] = int(row[1])
    return result

def ltod(l):
    d = dict()
    for i in l:
        d[i[0]] = int(i[1])
    return d


if __name__ == "__main__":
    current_dir = Path('.')
    count_files = current_dir.glob(r'count_*_*.txt')
    data = list()
    reg = re.compile(r"_(.+)_(.+)\.txt")
    for i in count_files:
        print("Open: " + i.name)
        with i.open(mode='r') as f:
            r = read_csv(f)
        g = reg.search(i.name)
        d = {'datetime': str(g.group(1)) + str(g.group(2)), 'data': r}
        data.append(d)
    print("Calculating")
    print("* Collect providers")
    provider = set()
    for i in data:
        for j in i['data'].keys():
            provider.add(j)
    print("* Collect datetime")
    dt = set()
    for i in data:
        dt.add(i['datetime'])
    print("* Sort data")
    data = sorted(data, key=operator.itemgetter('datetime'))
    print("* Create table")
    row_provider = list()
    for i in provider:
        row_provider.append(i)
    rows_data = list()
    for i in data:
        row = list()
        dt = i['datetime']
        row.append("20"+dt[0:2]+"/"+dt[2:4]+"/"+dt[4:6]+" "+dt[6:8]+":"+dt[8:10])
        for prov in row_provider:
            if not prov in i['data']:
                row.append(0)
            else:
                row.append(i['data'][prov])
        rows_data.append(row)
    row_provider.insert(0, 'datetime')
    print("Output data to csv.txt")
    with open('csv.txt', 'w') as f:
        csv_w = csv.writer(f)
        csv_w.writerow(row_provider)
        for i in rows_data:
            csv_w.writerow(i)
    print("Calculate sum")
    rows_total = list()
    for row in rows_data:
        dt = row[0]
        total = 0
        for column in row[1:]:
            total += int(column)
        rows_total.append([dt, total])
    print("Output to total.txt")
    with open("total.txt", "w") as f:
        csv_w = csv.writer(f)
        csv_w.writerow(["datetime", "total"])
        for row in rows_total:
            csv_w.writerow(row)
    print("Completed")


