from functools import reduce

a = lambda x: x * x

print(a(2))


b = map(a, [1, 2, 3, 4, 5])
print(list(b))

c = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])# reduce函数会对参数序列进行累积
print(c)

d = filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
print(list(d))

e = sorted([1, 2, 3, 4, 5], reverse=True)
print(e)

class SingleClass(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # cls._instance = object.__new__(cls,*args,**kwargs)
            cls._instance = super().__new__(cls,*args,**kwargs)
            return cls._instance
        else:
            return cls._instance

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        pass


s1 = SingleClass()
s2 = SingleClass()
print(s1 is s2)