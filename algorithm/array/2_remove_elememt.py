# 移除数组元素
# 这里需要注意的点： 数组的元素在内存地址中是连续的，不能单独删除数组中的某个元素，只能覆盖。
from pre_commit.output import write_line

from test.test import list_1


# 力扣题目： https://leetcode.cn/problems/remove-element/description/
# 题解： https://programmercarl.com/0027.%E7%A7%BB%E9%99%A4%E5%85%83%E7%B4%A0.html#%E6%80%9D%E8%B7%AF

# 方法： 双指针法，暴力解法

'''
双指针法：
    什么是双指针法呢？
        所谓的双指针法，其实是，快慢指针，这两个指针就是为了查找符合满足条件的数组或者数组下标
    什么时候慢指针移动呢？
        当快指针捕获的值需要慢指针覆盖或者移动时，比如 01需要移动到 10，这个时候慢指针+1
        
通用的表示方式：
def fast_slow_point(nums:list):
    n = len(nums)
    fast = slow = 0
    while fast < n:
        if nums[fast] != target:
            xxxxx
            slow += 1
        fast += 1
    return xxxx

代表题目：
    1. 删除数组中某个元素
            
    


'''

class Solution(object):
    def removeElement(self, nums:list[int], val:int):
        """
        # 暴力解法，需要两个指针，当遇到相等的值时，移动一下指针，当两个指针相遇时，停止
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        left,right = 0,len(nums)
        while left<right:
            if nums[left] == val:
                for j in range(left+1,right):
                    nums[j-1] = nums[j]
                left -= 1
                right -= 1
            left += 1
            print(nums)
        return left

    def removeElement_(self, nums:list[int], val:int):
        """
        快慢指针法，需要两个指针：
            快指针的作用： 一直向前查找
            慢指针：作为记录者，比如这道题，如果遇到需要移除的元素，那么指针位置不动，把下一个元素和现在的元素替换位置
            最后输出慢指针和 nums[0::slow]即是所求
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        slow = 0
        fast = 0
        while fast< len(nums): # 不加等于是因为，fast = size 时，nums[fast] 会越界
            # 慢指针什么时候移动,当不需要移除值的时候移动，每次吧fast 的值移动过去
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow +=1
            fast += 1
        return slow


# 力扣变种题目：26. 删除有序数组中的重复项 https://leetcode.cn/problems/remove-duplicates-from-sorted-array/description/
    def removeDuplicates(self, nums):
        """
        双指针法：
            慢指针指定用来覆盖值
            快指针来查找值
        :type nums: List[int]
        :rtype: int
        """
        slow = fast = 1
        n = len(nums)
        while fast < n:
            if nums[fast] != nums[fast-1]:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1

        print(nums)
        return slow

# 力扣变种题目：283. 移动零：https://leetcode.cn/problems/move-zeroes/description/
# 除了使用双指针，剩下的就是 nums[j-1],nums[j] = nums[j],nums[j-1] ab 两个相互交换一下
    def moveZeroes(self, nums):
        """
        暴力解法
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        point = 0
        while point < n:
            print(point,n)
            if nums[point] == 0:
                for j in range(point+1,n):
                    nums[j-1],nums[j] = nums[j],nums[j-1]
                point -= 1
                n -= 1
            point += 1
            print(nums)
        # print(nums)
        return nums
    def moveZeroes_(self, nums):
        """
        双指针法
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        fast,slow = 0,0
        n = len(nums)
        while fast < n:
            if nums[fast] != 0:
                nums[slow],nums[fast] = nums[fast],nums[slow]
                slow += 1
            fast += 1
        return nums



# 力扣变种题目： 884，比较含退格的字符串： https://leetcode.cn/problems/backspace-string-compare/description/
    def backspaceCompare(self, s, t):
        """
        暴力解法
        :type s: str
        :type t: str
        :rtype: bool
        """
        # 处理退格
        def context(con):
            str_ = ''
            for i in con:
                if "#" != i:
                    str_+= i
                else:
                    str_ = str_[:-1]
            return str_
        s = context(s)
        t = context(t)
        # if s == t:
        #     return True
        # else:
        #     return False
        return s == t

    def backspaceCompare_(self, s, t):
        """
        双指针法：
            快指针一直向前走，当遇到#号时，回退，注意，当#为第一个值时不回退
        网上那么多，但是我看了答案还是感觉暴力解法就很好了啊，解法就不写了
        :type s: str
        :type t: str
        :rtype: bool
        """

# 力扣变种题： 977，有序数组的平方
# https://leetcode.cn/problems/squares-of-a-sorted-array/
    def sortedSquares(self, nums):
        """
        这道题：暴力的排序方式就不写了，就来时间复杂度为 O(n)的排序方式了
        双指针方法的思路：
            1. 其实是求绝对值之后的大小，那么我们应该从 0 或者负数的那一个位置来开始
            2. 每次左右移动一个位置，来比较值的大小，然后将值写入到列表中，注意两个指针的位置左边的指针需要大于 0，右指针需要小于数组的长度

        :type nums: List[int]
        :rtype: List[int]
        """
        n = len(nums)
        # 判断数组中是否有负数
        negative = -1
        for index,num in enumerate(nums):
            print(index,num)
            if num < 0:
                negative = index
            else:
                break
        ans = list()
        # 定义左右指针
        i,j = negative,negative+1
        while i>=0 or j <n:
            # 这说明没有负数的存在了
            if i <0:
                ans.append(nums[j]*nums[j])
                j+=1
            # 这说明没有正整数的存在了
            elif j ==n:
                ans.append(nums[i]*nums[i])
                i-=1
            elif nums[i]*nums[i] < nums[j]*nums[j]:
                ans.append(nums[i]*nums[i])
                i-=1
            else:
                ans.append(nums[j]*nums[j])
                j+=1
        return ans














if __name__ == '__main__':
    s = Solution()
    # resp = s.removeElement([3,2,2,3],2)
    # resp = s.removeDuplicates(nums=[1,1,2])
    # resp = s.moveZeroes([1,2,0,2,0,1,1])
    # resp = s.moveZeroes([0,0,1])
    # resp = s.moveZeroes_([0,0,1])
    resp = s.sortedSquares([-4,-1,0,3,10])
    print(resp)
    # print([1,2,3,4][:-1])


