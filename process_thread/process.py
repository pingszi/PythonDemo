import multiprocessing
import time

"""
@desc ：多进程
@author Pings
@date   2018/05/15
@version V1.0
"""


# **创建函数并将其作为多个进程
def worker_1(interval):
    print("worker_1")
    time.sleep(interval)
    print("end worker_1")


def worker_2(interval):
    print("worker_2")
    time.sleep(interval)
    print("end worker_2")


def test2():
    # **创建进程，启动任务worker
    p1 = multiprocessing.Process(target=worker_1, args=(2,))
    p2 = multiprocessing.Process(target=worker_2, args=(3,))

    # **启动进程
    p1.start()
    p2.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for pr in multiprocessing.active_children():
        print("child p.name:" + pr.name + "\tp.id" + str(pr.pid))
    print("END!!!!!!!!!!!!!!!!!")


# **进程类
# **1.继承Process
class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    # **2.重写run方法
    def run(self):
        n = 5
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1


# **守护进程，不管守护进程自身执行到哪里，守护进程都会在主进程执行完成后结束
def test3():
    pr = multiprocessing.Process(target=worker_1, args=(3,))
    pr.daemon = True
    pr.start()
    # **想要守护进程执行完毕，需要在主线程中调用join，等待线程线束
    pr.join()
    print("end!")


# **进程锁,worker_no_with等待worker_with完成释放进程锁之后运行
def worker_with(lock, f):
    with lock:
        fs = open(f, 'a+')
        n = 10
        while n > 1:
            fs.write("Lockd acquired via with\n")
            n -= 1
        fs.close()


def worker_no_with(lock, f):
    # **获取进程锁
    lock.acquire()
    try:
        fs = open(f, 'a+')
        n = 10
        while n > 1:
            fs.write("Lock acquired directly\n")
            n -= 1
        fs.close()
    finally:
        lock.release()  # **释放进程锁


def test4():
    lock = multiprocessing.Lock()
    f = "file.txt"
    w = multiprocessing.Process(target=worker_with, args=(lock, f))
    nw = multiprocessing.Process(target=worker_no_with, args=(lock, f))
    w.start()
    nw.start()
    print("end")


# ** Semaphore用来控制对共享资源的访问数量，例如池的最大连接数
def worker(s, i):
    s.acquire()
    print(multiprocessing.current_process().name + "acquire")
    time.sleep(i)
    print(multiprocessing.current_process().name + "release\n")
    s.release()


def test5():
    s = multiprocessing.Semaphore(2)
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(s, i*2))
        p.start()


# **Event用来实现进程间同步通信
def wait_for_event(e):
    print("wait_for_event: starting")
    e.wait()
    print("wairt_for_event: e.is_set()->" + str(e.is_set()))


def wait_for_event_timeout(e, t):
    print("wait_for_event_timeout:starting")
    e.wait(t)
    print("wait_for_event_timeout:e.is_set->" + str(e.is_set()))


def test6():
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name="block", target=wait_for_event, args=(e,))

    w2 = multiprocessing.Process(name = "non-block", target=wait_for_event_timeout, args=(e, 2))
    w1.start()
    w2.start()

    time.sleep(3)

    e.set()
    print("main: event is set")


# **Queue多进程安全的队列
def writer_proc(q):
    try:
        q.put(1, block=False)
    except:
        pass


def reader_proc(q):
    try:
        print(q.get(block=False))
    except:
        pass


def test7():
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=writer_proc, args=(q,))
    writer.start()

    reader = multiprocessing.Process(target=reader_proc, args=(q,))
    reader.start()

    reader.join()
    writer.join()


# **Pipe代表一个管道的两个端，实现双向通信
def proc1(pipe):
    while True:
        for i in range(10000):
            print("send: %s" % i)
            pipe.send(i)
            time.sleep(1)


def proc2(pipe):
    while True:
        print("proc2 rev:", pipe.recv())
        time.sleep(1)


def proc3(pipe):
    while True:
        print("PROC3 rev:", pipe.recv())
        time.sleep(1)


def test8():
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
    p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
    p3 = multiprocessing.Process(target=proc3, args=(pipe[1],))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


# **线程池，获取子进程返回结果
def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")
    return msg


def test9():
    pool = multiprocessing.Pool(processes=3)

    # **执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    rst = []
    for i in range(4):
        msg = "hello %d" % i
        data = pool.apply_async(func, (msg,))
        rst.append(data)

    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    # **调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool
    pool.close()
    pool.join()
    print([i.get() for i in rst])
    print("Sub-process(es) done.")

if __name__ == "__main__":
    # test2()

    # p = ClockProcess(3)
    # # **进程p调用start()时，自动调用run()
    # p.start()

    # test3()

    # test4()

    # test5()

    # test6()

    # test7()

    # test8()

    test9()
