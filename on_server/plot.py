
# vim: fileencoding=utf-8

import numpy
import pandas

import matplotlib
matplotlib.use('cairo')  # Select backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import pylab


locator = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)

if __name__ == "__main__":
    print("Read csv.txt.")
    data = pandas.read_csv("csv.txt")

    print("Manupulate data.")
    data_dt = pandas.to_datetime(data["datetime"])
    del data["datetime"]
    series = dict()
    for i in data:
        series[i] = data[i].values

    print("Plot data.")
    fig, ax = plt.subplots()
    for k, v in series.items():
        print("* " + str(k))
        ax.plot(data_dt, v, linestyle = "-", marker = "o", label = str(k))
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid(True)
    plt.xlabel("datetime")
    plt.ylabel("counts")
    #ax.legend(bbox_to_anchor = (1.0, 1.05), loc = 9, borderaxespad = 0., ncol = 4)
    fig.autofmt_xdate()
    #pylab.subplots_adjust(top = 0.8)
    
    print("Save figure")
    plt.savefig("graph.png")



