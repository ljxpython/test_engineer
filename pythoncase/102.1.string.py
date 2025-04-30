
# 字符串相关操作
# 字符串定义
str1 = 'hello world'
print(str1) # hello world
# 字符串的索引
print(str1[0]) # h
print(str1[1]) # e
# 字符串的切片
print(str1[0:5]) # hello
print(str1[6:]) # world
print(str1[:5]) # hello
print(str1[:]) # hello world
# 字符串的拼接
print(str1 + '!') # hello world!
print(str1 * 2) # hello worldhello world
# 字符串的长度
print(len(str1)) # 11
# 字符串的查找
print(str1.find('world')) # 6
print(str1.find('hello')) # 0
print(str1.find('!')) # -1
# 字符串的替换
print(str1.replace('world', 'python')) # hello python
# 字符串的分割
print(str1.split(' ')) # ['hello', 'world']
# 字符串的大小写转换
print(str1.upper()) # HELLO WORLD
print(str1.lower()) # hello world
# 字符串的反转
print(str1[::-1]) # dlrow olleh
# 字符串的去空格,更详细的用法可参考:https://blog.csdn.net/shizheng_Li/article/details/145780451
str2 = str1.strip()
print(str2) # hello world
# 字符串的格式化
print('hello %s' % 'world') # hello world
print('hello {}'.format('world')) # hello world
print(f'hello {str1}') # hello hello world
# 字符串的判断
print(str1.isalpha()) # False
print(str1.isdigit()) # False
print(str1.isalnum()) # True
print(str1.isspace()) # False
print(str1.islower()) # True
print(str1.isupper()) # False
print(str1.startswith('hello')) # True
print(str1.endswith('world')) # True
# 字符串的截取
print(str1[0:5]) # hello
print(str1[6:]) # world
print(str1[:5]) # hello
print(str1[:]) # hello world