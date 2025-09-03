'''
给你一个 非严格递增排列 的数组 nums ，请你 原地 删除重复出现的元素，使每个元素 只出现一次 ，返回删除后数组的新长度。元素的 相对顺序 应该保持 一致 。然后返回 nums 中唯一元素的个数。

考虑 nums 的唯一元素的数量为 k ，你需要做以下事情确保你的题解可以被通过：

更改数组 nums ，使 nums 的前 k 个元素包含唯一元素，并按照它们最初在 nums 中出现的顺序排列。nums 的其余元素与 nums 的大小不重要。
返回 k 。
判题标准:

系统会用下面的代码来测试你的题解:

int[] nums = [...]; // 输入数组
int[] expectedNums = [...]; // 长度正确的期望答案

int k = removeDuplicates(nums); // 调用

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
如果所有断言都通过，那么您的题解将被 通过。



示例 1：

输入：nums = [1,1,2]
输出：2, nums = [1,2,_]
解释：函数应该返回新的长度 2 ，并且原数组 nums 的前两个元素被修改为 1, 2 。不需要考虑数组中超出新长度后面的元素。
示例 2：

输入：nums = [0,0,1,1,1,2,2,3,3,4]
输出：5, nums = [0,1,2,3,4]
解释：函数应该返回新的长度 5 ， 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4 。不需要考虑数组中超出新长度后面的元素。

'''


# 这题使用快慢指针法
# 快慢指针的核心思想就是,快指针负责遍历,慢指针当遇到不同的值时负责移动


class Solution(object):
    def removeDuplicates1(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # # 我的思路是创建一个新的列表,将不重复的元素放入新的数组中
        list_need  = []
        for i in nums:
            if i not in list_need:
                list_need.append(i)
        print(list_need)
        nums[:] = list_need
        return len(list_need)

    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # # 我的思路是创建一个新的列表,将不重复的元素放入新的数组中
        if nums == 0:
            return 0
        slow = fast = 1
        n = len(nums)
        while fast < n:
            if nums[slow] != nums[fast-1]:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        return slow


if __name__ == '__main__':
    s = Solution()
    res = s.removeDuplicates(nums=[1,1,2])
    print(res)

