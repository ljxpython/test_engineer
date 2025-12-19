

"""
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？



示例 1：

输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶
示例 2：

输入：n = 3
输出：3
解释：有三种方法可以爬到楼顶。
1. 1 阶 + 1 阶 + 1 阶
2. 1 阶 + 2 阶
3. 2 阶 + 1 阶


提示：

1 <= n <= 45



"""



class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        from functools import cache
        # 这题好像是迭代,迭代的做法就是定义好初始值,然后把最后的也定义好
        # 从最后一层退回去,还有 1+1 和2两种,那么f(n) = f(n-1)+f(n-2)
        @cache
        def dst(i:int):
            if i <= 1:
                return 1
            return dst(i-2) + dst(i-1)
        return dst(n)

if __name__ == '__main__':
    n = 9
    res = Solution().climbStairs(n=9)
    print(res)



