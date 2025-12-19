'''

说一下我理解的冒泡排序把,所谓的冒泡,其实就是咕噜咕噜的向上,这个比喻很形象
对应来说,就是两个数先进行比较,然后大的数就像泡泡一样向上,小的泡泡会再下面
那么冒泡排序的思想就是:
    就像泡泡一样,一直是两个数两两比较,然后大的在右边,那么首先第一轮我们就会得出最大的那个
    第二轮我们就会得出第二大的
    以此类推,我们就把这个数组排完
    这个时间复杂度,O(n^2)
'''


def bulubulu_sort(list_demo:list):
    def sort_(a,b):
        if a >b:
            return b,a
        else:
            return a,b
    right = len(list_demo)-1   # 这块之前做错,注意
    while right >0:
        left = 0
        while left < right:
            print(left)
            list_demo[left],list_demo[left+1] = sort_(list_demo[left],list_demo[left+1] )
            left +=1
        right -= 1

    return list_demo


# 选择排序

def chocessort(nums:list[int]):
    '''
    核心思想：每一轮从i位置开始，找出最小（或最大）元素放到i位置
比较方式：i位置元素与后面所有元素比较
交换次数：最多O(n)次交换


    :param nums:
    :return:
    '''
    for i in range(len(nums)-1):
        for j in range(i,len(nums)):
            # 两两比较
            if nums[i] > nums[j]:
                nums[i],nums[j] = nums[j],nums[i]
    return nums

def bubble_sort(nums: list[int]):
    '''
    核心思想：相邻元素两两比较，大的元素像气泡一样"上浮"到末尾
比较方式：只比较相邻元素（j和j+1）
交换次数：最多O(n²)次交换

    :param nums:
    :return:
    '''
    n = len(nums)
    # 外层循环：控制排序轮数，共n-1轮
    for i in range(n - 1):
        # 内层循环：从第一个元素开始，比较相邻元素
        # 每轮结束后，最大的元素会"冒泡"到末尾
        for j in range(n - 1 - i):  # 每轮范围缩小
            if nums[j] > nums[j + 1]:  # 比较相邻元素
                nums[j], nums[j + 1] = nums[j + 1], nums[j]  # 交换相邻元素
    return nums


if __name__ == '__main__':
    list_demo = [1,2,3,9,2,4]
    print(bulubulu_sort(list_demo=list_demo))