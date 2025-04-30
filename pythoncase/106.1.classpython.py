

class Person:
    sex = 'male'
    def __init__(self, name, age,student): # 初始化方法
        self.__name = name
        self.age = age
        self._student = student

    def get_fake_student(self):
        return self._student

    def get_private(self):
        return self.__name


# man = Person('ma', 18,True)
# print(man.get_private())
# print(man.get_fake_student())
# print(man.age)
# print(man._student)
# print(man.__name)


# __new__方法
# __new__方法用于创建对象，__init__方法用于初始化对象
# __new__方法在__init__方法之前被调用，__new__方法返回一个对象，该对象会被__init__方法初始化

class Person:
    def __new__(cls, *args, **kwargs):
        print("__new__方法被调用了")
        return super().__new__(cls)
    def __init__(self, name, age):
        print("__init__方法被调用了")
        self.name = name
        self.age = age
man = Person('ma', 18)
print(man.name)
print(man.age)


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
class MyClass(Singleton):
    a = 1
my_class = MyClass()
my_class2 = MyClass()
print(my_class is my_class2)
