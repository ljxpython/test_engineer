

# Python 元组常见操作
'''
可以把元组简单理解为不可变的列表
使用的场景：
1. 当我们需要存储一些不可变的数据时，就可以使用元组
2. 当我们需要存储一些可变的数据时，就可以使用列表
3. 当我们需要存储一些不可变的数据，又需要存储一些可变的数据时，就可以使用元组和列表的结合
'''

# 元组的创建
tuple1 = ()
tuple2 = tuple()
# 1. 创建元组
# 1.1. 直接使用小括号
tuple1 = (1, 2, 3, 4, 5)
print(f"tuple1的内容为：{tuple1}")
# 1.2. 使用 tuple() 函数
tuple2 = tuple([1, 2, 3, 4, 5])
print(f"tuple2的内容为：{tuple2}")
# 1.3. 使用逗号分隔
tuple3 = 1, 2, 3, 4, 5
print(f"tuple3的内容为：{tuple3}")
# 1.4. 使用 tuple() 函数和 range() 函数
tuple4 = tuple(range(1, 6))
print(f"tuple4的内容为：{tuple4}")
# 1.5. 使用 tuple() 函数和字符串
tuple5 = tuple('hello')
print(f"tuple5的内容为：{tuple5}")

# 2. 元组的访问
# 2.1. 使用索引访问
print(f"tuple1[0]的内容为：{tuple1[0]}")
# 2.2. 使用切片访问
print(f"tuple1[0:3]的内容为：{tuple1[0:3]}")
# 2.3. 使用 for 循环访问
for i in tuple1:
    print(i)
# 2.4. 使用 while 循环访问
i = 0
while i < len(tuple1):
    print(tuple1[i])
    i += 1
# 2.5. 使用 enumerate() 函数访问
for i, v in enumerate(tuple1):
    print(i, v)

# 3. 元组的修改
# 3.1. 元组是不可变的，不能修改元组的元素

# 4. 元组的删除
# 4.1. 元组是不可变的，不能删除元组的元素
# 4.2. 可以删除整个元组

# 5. 元组的其他操作
# 5.1. 元组的长度
print(f"tuple1的长度为：{len(tuple1)}")
# 5.2. 元组的拼接
tuple6 = tuple1 + tuple2
print(f"tuple6的内容为：{tuple6}")
# 5.3. 元组的重复
tuple7 = tuple1 * 2
print(f"tuple7的内容为：{tuple7}")
# 5.4. 元组的比较
print(f"tuple1 == tuple2的结果为：{tuple1 == tuple2}")
print(f"tuple1 > tuple2的结果为：{tuple1 > tuple2}")