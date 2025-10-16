


from collections import Counter

# 从字符串创建Counter
s = "hello world"
counter = Counter(s)
print(counter)  # 输出: Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

# 从列表创建Counter
fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
fruit_counter = Counter(fruits)
print(fruit_counter)  # 输出: Counter({'apple': 3, 'banana': 2, 'orange': 1})

# 从字典创建Counter
d = {'a': 3, 'b': 2, 'c': 1}
counter_from_dict = Counter(d)
print(counter_from_dict)  # 输出: Counter({'a': 3, 'b': 2, 'c': 1})





counter = Counter(['a', 'a', 'b', 'c', 'c', 'c'])

# 直接通过键访问计数值
print(counter['a'])  # 输出: 2
print(counter['b'])  # 输出: 1
print(counter['d'])  # 输出: 0 (不存在的键返回0)

# 使用get方法访问计数值
print(counter.get('c', 0))  # 输出: 3


counter = Counter('programming')

# elements(): 返回一个迭代器，包含所有元素，每个元素重复其计数次数
print(list(counter.elements()))  # 输出: ['p', 'r', 'o', 'g', 'r', 'a', 'm', 'm', 'i', 'n', 'g']

# most_common(n): 返回计数最多的n个元素和它们的计数
print(counter.most_common(3))  # 输出: [('r', 2), ('g', 2), ('m', 2)]

# subtract(): 减去另一个可迭代对象中的计数
counter.subtract('pro')
print(counter)  # 输出: Counter({'g': 2, 'm': 2, 'r': 1, 'a': 1, 'i': 1, 'n': 1, 'p': 0, 'o': 0})

# update(): 更新计数器，增加元素计数
counter.update('python')
print(counter)  # 输出: Counter({'g': 2, 'm': 2, 'n': 2, 'p': 1, 'r': 1, 'a': 1, 'i': 1, 't': 1, 'h': 1, 'o': 0, 'y': 1})

# clear(): 清空计数器
counter.clear()
print(counter)  # 输出: Counter()



'''

defaultdict

'''
from collections import defaultdict

# 创建一个默认值为 int 类型的 defaultdict
# 当访问不存在的键时，会自动创建该键并设置默认值为 0
count_dict = defaultdict(int)
count_dict['apple'] += 1
count_dict['banana'] += 2
print(count_dict)  # 输出: defaultdict(<class 'int'>, {'apple': 1, 'banana': 2})

# 访问不存在的键不会引发 KeyError
print(count_dict['orange'])  # 输出: 0 (自动创建并设置默认值)
print(count_dict)  # 输出: defaultdict(<class 'int'>, {'apple': 1, 'banana': 2, 'orange': 0})