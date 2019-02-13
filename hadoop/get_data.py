# **下载hadoop权威指南的气象数据
import os
import tarfile
import gzip
from urllib import request

def get_data(remote="ftp://ftp.ncdc.noaa.gov/pub/data/gsod/", local="d:/data/"):
    """下载数据"""
    if not os.path.exists(local):
        os.makedirs(local)

    start, end = 1929, 1950
    for year in range(start, end + 1):
        file = "gsod_{}.tar".format(year)
        path = "{0}/{1}".format(year, file)
        resp = request.urlretrieve("{0}{1}".format(remote, path), local + file)

    print(resp)


def merge(year, dir="D:/data/gsod_1929", savedir="D:/data/1/"):
    """把包含的gz文件的内容合并为一个文本文件"""
    files = os.listdir(dir)

    with open('{0}{1}.txt'.format(savedir, year), 'w') as newfile:
        for i, file in enumerate(files):
            with gzip.open(dir + "/" + file, 'r') as pf:
                for line in pf:
                    line = str(line)
                    if i and ("YEARMODA" in line):
                        continue

                    line = line[2:-3]
                    newfile.write(line + "\n")


def merges(dir="D:/data/"):
    """获取所的目录"""
    files = os.listdir(dir)
    for file in files:
        if file != '1':
            merge(file[-4:], dir + file) 


if __name__ == "__main__":
    # get_data()
    merges()
