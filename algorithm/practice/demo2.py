def threeSum(nums: list[int]):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    # 三数之和为0 也就是 a + b + c = 0
    # 固定一个值,然后寻找后面两个值是否加起来等于这个值
    # 需要注意 三个元素的index不能相同,那么如何不相同呢? i j k 不相等
    # 加入到res_list的元素不能重复   -> 可以考虑先去重
    # 做一道题没有思路时,要考虑一下,是不是需要排序,双指针可以解决那些事,滑动窗口可以解决那些事
    # 正式解决这个问题时的前,要去除哪些异常情况?
    # 双指针还要考虑清楚什么时候移动左指针,什么之后移动右指针
    if len(nums) < 3:
        return []
    
    res_list = []
    # 排序
    nums.sort()
    n = len(nums)
    
    # 循环
    for i in range(n - 2):
        # 如果当前数字大于0，则三数之和不可能为0
        if nums[i] > 0:
            break
            
        # 去重：跳过重复的元素
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left = i + 1
        right = n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                res_list.append([nums[i], nums[left], nums[right]])
                
                # 去重：跳过重复的元素
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                    
                # 移动指针
                left += 1
                right -= 1
            elif total < 0:
                # 和太小，移动左指针
                left += 1
            else:
                # 和太大，移动右指针
                right -= 1
                
    return res_list