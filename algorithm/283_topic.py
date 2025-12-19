"""


给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

请注意 ，必须在不复制数组的情况下原地对数组进行操作。



示例 1:

输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
示例 2:

输入: nums = [0]
输出: [0]


提示:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1


进阶：你能尽量减少完成的操作次数吗？

"""


def moveZeroes( nums):
    """
    :type nums: List[int]
    :rtype: None Do not return anything, modify nums in-place instead.
    """
    # 我个人的想法,检测到0就两两互换,换到后面
    n = len(nums)
    right = n -1
    for i in range(n):
        if nums[i] == 0:
            j = i
            while j < right:
                nums[j],nums[j+1] = nums[j+1],nums[j]
                j +=1
            right -= 1
    return nums

    # 这道题遇到快慢指针,而且不改变非0顺序的解法
    # 其实是当遇到非零,且快慢指针不相等时就移动一下位置
    # 快慢指针不等于零,且索引相等,那么就不动
    # 快指针等于零,此时快慢指针不相等,那么调换快慢指针位置
    # 其实如果快慢指针不相等,相当于慢指针其实是在零的位置停留,不知道你理解不理解
def other_main(nums:list[int]):
    slow = 0 
    for fast in range(len(nums)): 
        if nums[fast] != 0:  # 只要不是0就处理
            if slow != fast:  # 只有位置不同时才需要交换,因为
                nums[slow],nums[fast] = nums[fast],nums[slow] 
            slow +=1  # 无论是否交换，slow都应该前进
    return nums