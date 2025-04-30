

# 列表的一些常见操作,增删改查
# 列表定义
list1 = [1,2,3,4,5,6,7,8,9]
print(list1)
# 列表的索引
print(list1[0])
print(list1[1])

# 增
# 1.append()  末尾添加
list1.append(10)
print(list1)
# 2.insert()  指定位置添加
list1.insert(0,0)
print(list1)
# 3.extend()  末尾添加多个元素
list1.extend([11,12,13])
print(list1)
# 4.+  末尾添加多个元素
list1 = list1 + [14,15,16]
print(list1)

# 删
# 1.pop()  删除末尾元素
list1.pop()
print(list1)
# 2.pop(0)  删除指定位置元素
list1.pop(0)
print(list1)
# 3.remove()  删除指定元素
list1.remove(1)
print(list1)
# 4.del  删除指定元素
del list1[0]
print(list1)
# 5.clear()  清空列表
list1.clear()
print(list1)

# 改
# 1.直接赋值
list1 = [1,2,3,4,5,6,7,8,9]
list1[0] = 0
print(list1)
# 2.切片赋值
list1[0:3] = [0,0,0]
print(list1)

# 查
# 1.index()  查询指定元素的索引
print(list1.index(0))
# 2.count()  查询指定元素的个数
print(list1.count(0))
# 3.len()  查询列表的长度
print(len(list1))
# 4.in  查询指定元素是否在列表中
print(0 in list1)
# 5.for  查询列表中的元素
for i in list1:
    print(i)
# 6.切片查询
print(list1[0:3])

# 其他
# 1.列表推导式
print([i for i in list1])
# 2.列表生成式
print([i for i in range(10)])
