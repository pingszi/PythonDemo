# **语法-类级别以上


# **super关键字
class A:
    def __init__(self):
        print("A", end="")
        super().__init__()

class B:
    def __init__(self):
        print("B", end="")
        super().__init__()

class C(A, B):
    def __init__(self):
        print("C", end="")
        A.__init__(self)
        B.__init__(self)

def test1():
    print("MRO:", [x.__name__ for x in C.__mro__])
    C()


# **描述符
class RevealAccess:
    """数据描述符"""
    def __init__(self, initval=None, name="var"):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print("Retrieving", self.name)
        return self.val

    def __set__(self, obj, val):
        self.val = val

class MyClass:
    x = RevealAccess(10, 'var "x"')
    y = 5

def test2():
    m = MyClass()
    print(m.x)
    m.x = 20
    print(m.x)
    print(m.y)


# **property
class Rectangle:
    """定义property属性"""
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2,y2
    
    def _width_get(self):
        return self.x2 - self.x1

    def _width_set(self, value):
        self.x2 = self.x1 + value

    def _height_get(self):
        return self.y2 - self.y1

    def _height_set(self, value):
        self.y2 = self.y1 + value

    width = property(_width_get, _width_set, doc="width")
    height = property(_height_get, _height_set, doc="height")

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(self.__class__.__name__, self.x1, self.y1, self.x2, self.y2)

class Rectangle2:
    """property装饰器"""
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2,y2
    
    @property
    def width(self):
        return self.x2 - self.x1

    @width.setter
    def width(self, value):
        self.x2 = self.x1 + value

    @property
    def height(self):
        return self.y2 - self.y1

    @height.setter
    def height(self, value):
        self.y2 = self.y1 + value

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(self.__class__.__name__, self.x1, self.y1, self.x2, self.y2)

def test3():
    #rectangle = Rectangle(10, 10, 25, 34)
    rectangle = Rectangle2(10, 10, 25, 34)
    print("({}, {})".format(rectangle.width, rectangle.height))

    rectangle.width = 100
    print(rectangle)

    rectangle.height = 100
    print(rectangle)

    help(Rectangle)


# **槽
class Frozen:
    __slots__ = ["ice", 'cream']

def test4():
    print('__dict__' in dir(Frozen))

    print('ice' in dir(Frozen))

    frozen = Frozen()
    frozen.ice = True
    frozen.cream = None
    # **定义了槽的类实例，不允许动态添加属性
    #frozen.icy = True


# **__new__()方法覆写实例创建过程
class NonZero(int):
    def __new__(cls, value):
        return super().__new__(cls, value) if value != 0 else None
    
    def __init__(self, value):
        print("__init__ call")
        super().__init__()

def test5():
    v1 = NonZero(3)
    v2 = NonZero(0)


# **元类
class RevealingMeta(type):
    """定义一个元类"""
    def __new__(mcs, name, bases, namespace, **kwargs):
        print(mcs, "__new__ called")
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print(mcs, "__prepare__ called")
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls,  name, bases, namespace, **kwargs):
        print(cls, "__init__ called")
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        print(cls, "__call__ called")
        return super().__call__(*args, **kwargs)

class RevealingClass(metaclass=RevealingMeta):
    def __new__(cls):
        print(cls, "__new__ called")
        return super().__new__(cls)

    def __init__(self):
        print(self, "__init__ called")
        super().__init__

def test6():
    print(RevealingClass())


# 面向对象的示例
class Test:
    """
    @desc ： 默认继承自object(python3)，一个模块可以有多个类。
             python没有真正的作用域，全部为公有，只有约定的私有语法
    @author  Pings
    @date    2018/08/06
    @version V1.0
    """
    p1 = ""        # **类变量
    _p2 = 18       # **类变量，_约定私有标记，也适用于方法
    __p3 = "男"    # **类变量，自动转换为:_People__sex，也适用于方法

    def __init__(self, str):
        """内建方法，会在创建对象之后马上调用"""
        self.p4 = str  # **成员变量

    def m1(self, str):
        """成员方法，第一个参数代表类的实例，约定使用self。只能通过实例调用"""
        print(str)

    @classmethod
    def m2(cls, str):
        """类方法，第一个参数代表类本身，约定使用cls。可通过类调用，也可通过实例调用"""
        print(str)

    @staticmethod
    def m3(str):
        """静态方法。只能通过类调用"""
        print(str)


class Test1(Test):
    """继承自Test"""

    def __init__(self, str):
        """内建方法，会在创建对象之后马上调用"""
        super().__init__(str)    #**父类没有无参初始化方法时，需要显示调用

    def m1(self, str):
        """重写父类的m1成员方法"""
        print(str)


# 抽象类示例
import abc
class A1(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractproperty
    def value(self):
        return 'should never see this.'
    @value.setter
    def value(self, _value):
        return
 
class B1(A1):
    _value = 'default'
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, _value):
        self._value = _value

def test7():
    b = B1()
    print(b.value)
    b.value = 'hello'
    print(b.value)
    

if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    test7()