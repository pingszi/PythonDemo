from functools import reduce

"""
@desc ：函数式编程
@author Pings
@date   2018/04/27
@version V1.0
"""

# **把函数本身赋值给变量
f = abs
print(f(-10))


# **map函数示例
def f(x):
    return x * x
r = map(f, [1, 2, 3, 4, 5])
print(list(r))


# **reduce函数示例
def add(x, y):
    return x + y
r = reduce(add, [1, 3, 5, 7, 9])
print(r)

# **字符串倒序排序
s = '可减按cvcc征收车1234辆购置税的乘用车购置日期如何确定？'
print(s[::-1])
