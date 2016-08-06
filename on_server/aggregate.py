#!/usr/bin/python
# vim: fileencoding=utf-8

import numpy
import pandas

import csv
import re

if __name__ == "__main__":
    print("Read total.txt.")
    data = pandas.read_csv("total.txt")

    print("Manupulate data.")
    # convert str to timestamp
    data["timestamp"] = pandas.to_datetime(data["datetime"])
    del data["datetime"]
    
    data["weekday"] = data["timestamp"].dt.weekday
    data["month"] = data["timestamp"].dt.month
    data["hour"] = data["timestamp"].dt.hour

    gr_weekday = data.groupby("weekday")
    mean_weekday = gr_weekday.aggregate(numpy.mean)

    gr_month = data.groupby("month")
    mean_month = gr_month.aggregate(numpy.mean)

    gr_hour = data.groupby("hour")
    mean_hour = gr_hour.aggregate(numpy.mean)
    
    print("Output data.")
    mean_weekday.to_csv("weekday.txt")
    mean_month.to_csv("month.txt")
    mean_hour.to_csv("hour.txt")


