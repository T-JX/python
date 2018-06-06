# coding:utf-8

# 闭包:1.函数内嵌套函数  2.内部函数引用外部函数的局部变量  3.外部函数的返回值是内部函数

# def eat():
#     pass
# <class 'function'> 函数的类型
# print(type(eat))
def test(number):
    # number 局部变量,生命周期  从声明开始往下,到代码块结束
    def test_2(number_in):
        # 内部函数引用外部函数局部变量
        return number * number_in

    # 返回一个函数对象
    return test_2


# <function test.<locals>.test_2 at 0x00000000004837B8> test_2函数对象
# 执行test函数后返回的是一个函数对象,这个对象就是test_2
# 由于内部函数引用了外部函数的局部变量,导致外部函数执行完之后,局部变量没有及时释放,占用内存
rs = test(10)
# 因为rs是一个函数对象,可以被执行,rs(20)相当执行了test_2这个函数,在test_2中引用了test中的局部变量number,并且test返回的就是test_2这函数,所以我们称test_2为闭包
s = rs(20)
print(s)


# 带两个参数的
def sum(a, b):
    def numbers(x, y):
        return a * x + b * x + a * y + b * y

    return numbers


num = sum(10, 20)
rs = num(30, 40)
print(rs)


# 利用闭包自定义装饰器
# func 把一个函数作为参数
def w1(func):
    def inner():
        # 返回调用传递进来的函数执行的结果
        return func()
    return inner
# @w1 装饰器  返回一个内部函数inner
# 装饰器的作用:在不更改原始函数的基础上,为函数添加一些额外功能
# 在装饰器下定义的f1函数实际上就是传递到装饰器的参数
@w1
def f1():
    return 123456


rs = f1()
print(rs)

# 打印输出某个函数执行消耗的时间

from datetime import datetime


def run_time(func):
    def test():
        # 获取开始执行的时间
        start_time = datetime.now()
        func()
        # 计算执行消耗的时间
        print('执行{},消耗了{}时间'.format(func.__name__, datetime.now() - start_time))

    return test


@run_time
def for_test():
    for x in range(10000):
        c = x + x

for_test()


@run_time
def for1000000_tetst():
    for x in range(1000000):
        c = x * x


for1000000_tetst()


# 带参数的装饰器
def test(name):
    if name == '张三':
        # 定义装饰器用到闭包
        def run(func):

            def sleep():
                func()

            return sleep

        return run
    else:
        def error(func):
            #
            print('你不是张三,没有权限吃饭')

        return error


@test('李四')
def eat():
    print('只有张三才能吃饭')


eat()