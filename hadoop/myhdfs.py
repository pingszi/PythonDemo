# **hdfs操作
import os
from hdfs import client

#**url：ip：端口
client = client.InsecureClient("http://yh001:50070", user="hadoop" ,root="/") 


def upload(remote_dir="/pings/wordcount/", local_dir="D:/data/1/"):
    """上传本地文件到hdfs"""
    client.delete(remote_dir, True)
    client.makedirs(remote_dir)
    for file in os.listdir(local_dir):
        client.upload(remote_dir, local_dir + file)


if __name__ == "__main__": 
    upload()
    print(client.list("/"))
