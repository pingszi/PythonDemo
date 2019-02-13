#!/usr/bin/python3
# **reducer
import sys
from itertools import groupby
from operator import itemgetter


def read1():
    """测试数据源"""
    datas = [
             '1929 19.61',
             '1929 19.11',
             '1930 20.72',
             '1930 24.61',
             '1931 21.28'
            ]

    for line in datas:
        yield line.split(" ", 1)


def read2():
    """hadoop数据源"""
    for line in sys.stdin:
        yield line.split("\t", 1)


def max_temperature_reducer():
    """计算年份的最高温度"""
    for year, temperature_list in groupby(read2(), itemgetter(0)):
        max = 0
        for t in temperature_list:
            if len(t) > 1:
                temp = float(t[1])
                max = temp if temp > max else max
        print("{0}\t{1}".format(year, max))
    

max_temperature_reducer()

# hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.1.jar -file max_temperature_mapper.py -mapper max_temperature_mapper.py -file max_temperature_reducer.py -reducer max_temperature_reducer.py -input /pings/1929.txt -output /pings/out/