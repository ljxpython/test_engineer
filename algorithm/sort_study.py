

d = {'apple': 3, 'banana': 1, 'orange': 2}

sorted_keys = sorted(d.items(),key=lambda x:x[1],reverse=True)
print(sorted_keys)


'''
列表

'''
# 原地排序
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()
print(numbers)  # 输出: [1, 1, 3, 4, 5, 9]
numbers.sort(reverse=True)
print(numbers)  # 输出: [1, 1, 3, 4, 5, 9]
# 自定义排序键（按字符串长度）
words = ['apple', 'banana', 'kiwi', 'orange']
words.sort(key=len)
print(words)  # 输出: ['kiwi', 'apple', 'banana', 'orange']

# 返回新列表的排序：sorted() 函数
# 基本用法
numbers = [3, 1, 4, 1, 5, 9]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # 输出: [1, 1, 3, 4, 5, 9]
print(numbers)  # 原列表不变: [3, 1, 4, 1, 5, 9]

# 降序排序
reverse_sorted = sorted(numbers, reverse=True)

# 自定义排序键
words = ['apple', 'banana', 'kiwi', 'orange']
len_sorted = sorted(words, key=len)

'''
字典
'''
d = {'apple': 3, 'banana': 1, 'orange': 2}

# 方法1：获取按键排序的键列表
sorted_keys = sorted(d.keys())
print(sorted_keys)  # 输出: ['apple', 'banana', 'orange']

# 方法2：获取按键排序的(键,值)对列表
sorted_items = sorted(d.items())
print(sorted_items)  # 输出: [('apple', 3), ('banana', 1), ('orange', 2)]

# 转换为按键排序的字典（Python 3.7+）
sorted_dict = dict(sorted_items)
print(sorted_dict)  # 输出: {'apple': 3, 'banana': 1, 'orange': 2}


d = {'apple': 3, 'banana': 1, 'orange': 2}

# 使用lambda函数作为key参数
sorted_by_value = sorted(d.items(), key=lambda x: x[1])
print(sorted_by_value)  # 输出: [('banana', 1), ('orange', 2), ('apple', 3)]

# 转换为按值排序的字典
sorted_dict = {k: v for k, v in sorted_by_value}
print(sorted_dict)  # 输出: {'banana': 1, 'orange': 2, 'apple': 3}

# 按值降序排序
sorted_by_value_desc = sorted(d.items(), key=lambda x: x[1], reverse=True)

# 先按长度排序，长度相同时按字母顺序排序
words = {'abc': 3, 'a': 1, 'ab': 2, 'abd': 4}
sorted_words = sorted(words.items(), key=lambda x: (len(x[0]), x[0]))
print(sorted_words)  # 输出: [('a', 1), ('ab', 2), ('abc', 3), ('abd', 4)]