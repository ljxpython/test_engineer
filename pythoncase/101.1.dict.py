
# 字典的一些常见操作
# 1. 字典的创建
dict1 = {}
dict2 = dict()
dict3 = {'a': 1, 'b': 2, 'c': 3}
dict4 = dict([('a', 1), ('b', 2), ('c', 3)])
dict5 = dict(a=1, b=2, c=3)
dict6 = dict({'a': 1, 'b': 2, 'c': 3})
dict7 = dict(zip(['a', 'b', 'c'], [1, 2, 3]))
dict8 = dict.fromkeys(['a', 'b', 'c'], 1)
dict9 = dict.fromkeys('abc', 1)
dict10 = dict.fromkeys(['a', 'b', 'c'], [1, 2, 3])
print(dict1)
print(dict2)
print(dict3)
print(dict4)
print(dict5)
print(dict6)
print(dict7)
print(dict8)
print(dict9)
print(dict10)
# 2. 字典的访问
print("*"*100)
print(f"字典的内容为：{dict3}")
print(dict3['a'])
print(dict3.get('a'))
print(dict3.get('d'))
print(dict3.get('d', 'default'))
print(dict3.keys())
print(dict3.values())
print(dict3.items())
# 3. 字典的增改
print("*"*100)
print(f"字典的内容为：{dict3}")
dict3['d'] = 4
print(dict3)
dict3.update({'a': 6})
print(dict3)
dict3.update({'e': 7})
print(dict3)
# 4. 字典的删
print("*"*100)
print(f"字典的内容为：{dict3}")
dict3.pop('a')
print(dict3)
dict3.pop('f', 'default')# 删除不存在的键，会报错
print(dict3)
del dict3['b']
print(dict3)
dict3.clear()
print(dict3)
# 5. 字典的其他操作
print("*"*100)
dict3 = {'a': 1, 'b': 2, 'c': 3}
print(f"字典的内容为：{dict3}")
print(len(dict3))
print('a' in dict3)
print('a' not in dict3)
print(dict3.copy())
print(dict3.get('a', 'default'))
print(dict3.items())
print(dict3.keys())
print(dict3.values())