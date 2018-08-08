# **语法-类级别以下


def test1():
    """"""
    # **用带星号的表达式获取单个变量中的多个元素
    a, b, *c = "foo", "bar", "100", "200"
    print(a)
    print(c)

    # **嵌套解包
    (a, b), (c, d) = (1, 2), (3, 4)
    print(a)
    print(d)


def test2():
    """集体set()"""
    # **在一个set()或frozenset()中能包含另一个不可变的frozenset()
    s = set([frozenset([1, 2, 3]), frozenset([4, 5, 6])])
    print(s)
    # **在一个set()或frozenset()中不能包含另一个普通的可变的set()
    set([set([1, 2, 3]), set([4, 5, 6])])


# **创建迭代器
# **1.函数
myiter = iter("abc")
# **2.类
class CountDown(object):

    def __init__(self, step):
        self.step = step
    
    def __next__(self):
        """返回容器的下一个元素"""
        # **遍历完序列时，会引发一个StopIteration异常，以与循环兼容，终止循环
        if self.step <= 0:
            raise StopIteration
        
        self.step -= 1
        return self.step

    def __iter__(self):
        """返回迭代器本身"""
        return self

def test3():
    """测试迭代器"""
    for i in myiter:
        print(i)
    
    count = CountDown(10)
    for i in count:
        print(i)


# **生成器
def fibonacci():
    """斐波纳契数列"""
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b

def psychologist():
    """通过send传递值"""
    print("......")
    while True:
        answer = (yield)
        if answer is not None:
            if answer.endswith("?"):
                print("?")
            elif "good" in answer:
                print("good")
            elif "bad" in answer:
                print("bad")

def test4():
    """测试生成器"""
    a = fibonacci()
    print(next(a))
    print(next(a))
    print(next(a))

    b = psychologist()
    next(b)
    b.send("test?")
    b.send("goodtest")
    b.send("testbad")


# **装饰器
def mydecorator(func):
    """装饰器函数(无参)"""
    from functools import wraps
    @wraps(func)
    def wrapped(*args, **kwargs):
        # **在调用函数之前处理
        print("before")
        rst = func(*args, **kwargs)  
        # **在调用函数之后处理
        print("after")
        # **返回结果
        return rst
    # **返回wrapped作为装饰函数
    return wrapped

class DecoratorAsClass(object):
    """装饰器类(无参)"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # **在调用函数之前处理
        print("before...")
        rst = self.func(*args, **kwargs)  
        # **在调用函数之后处理
        print("after...")
        # **返回结果
        return rst

def xmlrpc(in_=(), out=(type(None),)):
    from functools import wraps

    """参数类型检查"""
    def decorator(function):
        # **打印签名
        print("{0}: {1}".format(function.__name__, (in_, out)))
        def _check_types(elements, types):
            """检查类型的子函数"""
            if len(elements) != len(types):
                raise TypeError("argument count is wrong")
            typed = enumerate(zip(elements, types))
            for index, couple in typed:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError("arg #{0} should be {1}".format(index, of_the_right_type))

        @wraps(function)
        def wrapper(*args):
            # **检查输入的内容(如果是类的方法，第一参数是self，需要删除)
            checkable_args = args
            _check_types(checkable_args, in_)
            # **运行函数
            rst = function(*args)
            # **检查输出的内容
            if not type(rst) in (tuple, list):
                checkable_rst = (rst,)
            else:
                checkable_rst = rst
            _check_types(checkable_rst, out)

            # **函数及其类型检查成功
            return rst
        return wrapper
    return decorator

#@mydecorator
#@DecoratorAsClass
@xmlrpc(in_=(int, int), out=(int,))
def test5(a, b):
    """测试装饰器"""
    print("...")
    return a + b


# **上下文管理器
class ContextIllustration(object):
    """类"""
    def __enter__(self):
        print("entering context")

    def __exit__(self, exc_type, exc_value, traceback):
        print("leaving context")

        if exc_type is None:
            print("with no error")
        else:
            print("with an error ({0})".format(exc_value))

from contextlib import contextmanager
@contextmanager
def context_illustration():
    """函数"""
    print("entering context")

    try:
        yield
    except Exception as e:
        print("leaving context")
        print("with an error ({0})".format(e))

        # **需要再次抛出异常
        raise
    else:
        print("leaving context")
        print("with no error")

def test6():
    """测试上下文管理器"""
    # with ContextIllustration():
    #     print("test")

    # with ContextIllustration():
    #     raise RuntimeError("test error")

    with context_illustration():
        print("test")

    with context_illustration():
        raise RuntimeError("test error")


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    # print(test5(1, 2))
    # test6()

    print({i for i in [1, 2]})