"""

给定一个表示 大整数 的整数数组 digits，其中 digits[i] 是整数的第 i 位数字。这些数字按从左到右，从最高位到最低位排列。这个大整数不包含任何前导 0。

将大整数加 1，并返回结果的数字数组。



示例 1：

输入：digits = [1,2,3]
输出：[1,2,4]
解释：输入数组表示数字 123。
加 1 后得到 123 + 1 = 124。
因此，结果应该是 [1,2,4]。
示例 2：

输入：digits = [4,3,2,1]
输出：[4,3,2,2]
解释：输入数组表示数字 4321。
加 1 后得到 4321 + 1 = 4322。
因此，结果应该是 [4,3,2,2]。
示例 3：

输入：digits = [9]
输出：[1,0]
解释：输入数组表示数字 9。
加 1 得到了 9 + 1 = 10。
因此，结果应该是 [1,0]。


提示：

1 <= digits.length <= 100
0 <= digits[i] <= 9
digits 不包含任何前导 0。

"""


class Solution(object):
    def plusOne(self, digits):
        """
        加一问题 - 正确的解法
        :type digits: List[int]
        :rtype: List[int]
        """
        # 从最后一位开始加1
        i = len(digits) - 1
        carry = 1  # 进位，初始为1表示加1
        
        # 从右往左处理每一位
        while i >= 0 and carry:
            # 当前位加上进位
            total = digits[i] + carry
            # 更新当前位的值（个位数）
            digits[i] = total % 10
            # 计算新的进位
            carry = total // 10
            # 移动到前一位
            i -= 1
        
        # 如果最后还有进位，说明需要在最前面添加1
        if carry:
            digits.insert(0, 1)
        
        return digits
    
    def plusOne_your_approach_fixed(self, digits):
        """
        修复你原来的想法
        :type digits: List[int]
        :rtype: List[int]
        """
        # 将数字列表转换为字符串，再转换为整数
        s = ''.join(str(digit) for digit in digits)  # 修复：需要先转换为字符串
        num = int(s)
        num += 1
        num_str = str(num)
        # 将字符串转换为整数列表
        return [int(char) for char in num_str]  # 修复：需要转换回整数
    
    def plusOne_simple(self, digits):
        """
        简化版本 - 更直观的理解
        :type digits: List[int]
        :rtype: List[int]
        """
        # 从最后一位开始
        for i in range(len(digits) - 1, -1, -1):
            # 如果当前位不是9，直接加1返回
            if digits[i] < 9:
                digits[i] += 1
                return digits
            # 如果是9，变成0，继续处理前一位（相当于进位）
            digits[i] = 0
        
        # 如果所有位都是9，需要在最前面添加1
        # 例如：[9,9,9] -> [1,0,0,0]
        return [1] + [0] * len(digits)


def test_solutions():
    """测试不同的解决方案"""
    solution = Solution()
    
    # 测试用例
    test_cases = [
        [1, 2, 3],      # 预期输出: [1, 2, 4]
        [4, 3, 2, 1],   # 预期输出: [4, 3, 2, 2]
        [9],            # 预期输出: [1, 0]
        [9, 9, 9],      # 预期输出: [1, 0, 0, 0]
        [0],            # 预期输出: [1]
        [8, 9, 9]       # 预期输出: [9, 0, 0]
    ]
    
    for i, digits in enumerate(test_cases):
        # 注意：由于我们会修改原数组，所以需要复制
        original = digits[:]
        result1 = solution.plusOne(digits[:])
        result2 = solution.plusOne_your_approach_fixed(original[:])
        result3 = solution.plusOne_simple(original[:])
        
        print(f"测试用例 {i+1}: {original}")
        print(f"  方法1(推荐):     {result1}")
        print(f"  方法2(修复版):   {result2}")
        print(f"  方法3(简化版):   {result3}")
        print(f"  结果一致: {result1 == result2 == result3}")
        print()

if __name__ == '__main__':
    test_solutions()