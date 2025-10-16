# 京东面试题 - 字符串反转 (LeetCode 344)

def reverse_string(s):
    """
    反转字符串（修改原数组）
    思路：双指针从两端向中间交换
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # 交换字符
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    
    return s

def reverse_string_new(s):
    """
    反转字符串（返回新字符串）
    """
    return s[::-1]

def reverse_words(s):
    """
    反转字符串中的单词顺序
    京东面试常考变种题
    """
    # 去除多余空格并分割
    words = s.strip().split()
    # 反转单词顺序
    words.reverse()
    # 重新连接
    return ' '.join(words)

def is_palindrome(s):
    """
    判断字符串是否为回文串
    京东面试常考相关题
    """
    # 只考虑字母数字字符，忽略大小写
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]

# 测试用例
def test_string_problems():
    print("=== 字符串反转测试 ===")
    
    # 测试用例1：基本反转
    s1 = list("hello")
    print(f"原始字符串: {s1}")
    reverse_string(s1)
    print(f"反转后: {s1}")
    
    # 测试用例2：新字符串反转
    s2 = "world"
    result2 = reverse_string_new(s2)
    print(f"\n原始字符串: {s2}")
    print(f"反转后: {result2}")
    
    # 测试用例3：反转单词顺序
    s3 = "the sky is blue"
    result3 = reverse_words(s3)
    print(f"\n原始字符串: {s3}")
    print(f"单词反转后: {result3}")
    
    # 测试用例4：回文判断
    test_cases = ["race a car", "A man a plan a canal Panama", "", "a"]
    for s in test_cases:
        result = is_palindrome(s)
        print(f"\n'{s}' 是回文串吗？ {result}")
    
    # 测试用例5：边界条件
    print(f"\n=== 边界条件测试 ===")
    print(f"空字符串反转: {reverse_string_new('')}")
    print(f"单个字符反转: {reverse_string_new('a')}")
    print(f"两个字符反转: {reverse_string_new('ab')}")

if __name__ == "__main__":
    test_string_problems()