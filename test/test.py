from functools import reduce

from setuptools import setup, find_packages

# def multi():
#     return [lambda x : i*x for i in range(4)]
# print([m(3) for m in multi()])

def multi():
    return [lambda x, i=i: i*x for i in range(4)]
print([m(3) for m in multi()])


# 讲解以下Python的回调函数

print(map(lambda x:x*x,[y for y in range(3)]))
a= list(map(lambda x:x*x,[y for y in range(3)]))
print(a)

## reduce(lambda x,y : x*y,range(1,n+1))
a = reduce(lambda x,y : x*y,range(1,3+1))
print(a)

a = lambda x,y : x*y
print(a(1,2))

# N =100
print ([[x for x in range(1,100)] [i:i+3] for i in range(0,100,3)])
print([i for i in range(0,100,3)])