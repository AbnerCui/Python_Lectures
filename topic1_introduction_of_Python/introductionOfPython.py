import math
import random
from datetime import date

def basic_python():

    pi = math.pi
    print(pi)

    random_choice = random.choice(['apple', 'pear', 'banana'])
    print(random_choice)

    now = date.today()
    birthday = date(1999, 8, 20)
    age = now - birthday
    print(age.days)


def arithmetic_calculation():

    a = 21
    b = 10
    c = 0

    c = a + b
    print("c 的值为：", c)

    c = a - b
    print("c 的值为：", c)

    c = a * b
    print("c 的值为：", c)

    c = a / b
    print("c 的值为：", c)

    c = a % b  # 取余数
    print("c 的值为：", c)

    # 修改变量 a 、b 、c
    a = 2
    b = 3
    c = a ** b
    print("c 的值为：", c)

    a = 10
    b = 5
    c = a // b  # 取整
    print("c 的值为：", c)

def comparison_calculation():
    a = 21
    b = 10
    c = 0

    if a == b:
        print("a 等于 b")
    else:
        print("a 不等于 b")

    if a != b:
        print("a 不等于 b")
    else:
        print("a 等于 b")

    if a < b:
        print("a 小于 b")
    else:
        print("a 大于等于 b")

    if a > b:
        print("a 大于 b")
    else:
        print("a 小于等于 b")

    # 修改变量 a 和 b 的值
    a = 5
    b = 20
    if a <= b:
        print("a 小于等于 b")
    else:
        print("a 大于  b")

    if b >= a:
        print("b 大于等于 a")
    else:
        print("b 小于 a")

def logic_calculation(a, b):


    if a and b:
        print("变量 a 和 b 都为 true")
    else:
        print("变量 a 和 b 有一个不为 true")

    if a or b:
        print("变量 a 和 b 都为 true，或其中一个变量为 true")
    else:
        print("变量 a 和 b 都不为 true")

    if not (a and b):
        print("变量 a 和 b 都为 false，或其中一个变量为 false")
    else:
        print("变量 a 和 b 都为 true")

def assignment_calculation(a, b, c):


    c = a + b
    print("c 的值为：", c)

    c += a
    print("c 的值为：", c)

    c *= a
    print("c 的值为：", c)

    c /= a
    print("c 的值为：", c)

    c = 2
    c %= a
    print("c 的值为：", c)

    c **= a
    print("c 的值为：", c)

    c //= a
    print("c 的值为：", c)


def if_statement():

    num = 9
    if num >= 0 and num <= 10:  # 判断值是否在0~10之间
        print('hello')

    num = 10
    if num < 0 or num > 10:  # 判断值是否在小于0或大于10
        print('hello')
    else:
        print('undefine')

    num = 8
    # 判断值是否在0~5或者10~15之间
    if (num >= 0 and num <= 5) or (num >= 10 and num <= 15):
        print('hello')
    else:
        print('undefine')

def do_statement():

    count = 0
    while count < 5:
        print(count, " is  less than 5")
        count = count + 1
    else:
        print(count, " is not less than 5")

    fruits = ['banana', 'apple', 'mango']
    for index in range(len(fruits)):
        print('当前水果 :', fruits[index])
    print("Good bye!")

def other_statement():

    for letter in 'Python':
        if letter == 'h':
            break
        print('当前字母 :', letter)

    for letter in 'Python':
        if letter == 'h':
            continue
        print('当前字母 :', letter)

    # 输出 Python 的每个字母
    for letter in 'Python':
        if letter == 'h':
            pass
            print('这是 pass 块')
        print('当前字母 :', letter)

    print("Good bye!")

if __name__ == '__main__':

    comparison_calculation()
    arithmetic_calculation()
    comparison_calculation()
    logic_calculation(True, False)
    assignment_calculation(21, 10, 0)
    if_statement()
    do_statement()
    other_statement()