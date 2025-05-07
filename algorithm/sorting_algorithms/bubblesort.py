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


if __name__ == '__main__':
    list_demo = [1,2,3,9,2,4]
    print(bulubulu_sort(list_demo=list_demo))