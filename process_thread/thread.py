import threading
import multiprocessing

"""
@desc ：多线程
@author Pings
@date   2018/05/15
@version V1.0
"""


# **多线程无法利用多核心cpu
def loop():
    x = 0
    while True:
        x = x ^ 1
        print(threading.current_thread().name, x)

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()
