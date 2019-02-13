#!/usr/bin/python3
# **mapper
import sys
import re


def toC(qty):
    """华氏温度转换成摄氏温度（摄氏＝5/9(°F－32)）"""
    return round(5 / 9 * (qty - 32), 2)


def max_temperature_mapper():
    """计算年份的最高温度"""
    for line in sys.stdin:
        line = re.split(r" *", line)
        if len(line) > 17:
            qty = line[17]
            if qty != '9999.9':
                qty = qty[:-1] if qty.endswith("*") else qty
                print("{0}\t{1}".format(line[2][:4], toC(float(qty))))


max_temperature_mapper()