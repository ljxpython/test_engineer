'''
快速排序
说到快速排序,那什么是快速排序呢?其实就是我们把数组中,随便选一个数来排序
只要大于这个数的就放到右边
只要小于这个数的就放到左边
那么,可以想象第一轮下去,这个数在第k个位置,那个k左边的都是小于等于这个数的,右边的全是大于这个数的

那么接着循环,因为有两个数组了,那么对这两个数组重复上面的操作

终止条件是什么呢?就是当这个k相等时,我们就不需要排序了

这是一个迭代的思想

分割->排序->找条件,然后终止,就是这样很简单的一个流程

'''


# arr = [4, 2, 9, 6, 5, 1, 3]
def quick_sort(arr,left,right):
    # 分割的函数
    def part_arr(arr,left,right):
        # 把最后一个数当做基准值
        pivot = arr[right]
        # 初始k的位置从最小的值开始
        k = left -1
        # 分割归类
        for i in range(left,right):
            # 我们要保证第k个数包括第k个数都比pivot小,如果不是,如下方式进行替换
            if arr[i] <= pivot:
                k+=1
                arr[i],arr[k] = arr[k],arr[i]
        # 最后把基准值放到正确的位置上
        arr[k+1],arr[right] = arr[right],arr[k+1]  # 这里我曾经写错,之前是k的位置,这样是错误的,因为第k个元素是比该元素小或者相等的
        return k+1
    # 终止条件为 left>right
    if left >= right:
        return
    else:
        # 迭代里面就是分割
        pi = part_arr(arr,left,right)
        quick_sort(arr,left,pi-1)
        quick_sort(arr,pi+1,right)


def partition(arr, low, high):
    i = (low - 1)  # 最小元素索引
    pivot = arr[high]
    # print(pivot)

    for j in range(low, high):

        # 当前元素小于或等于 pivot
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
        # print(arr)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


if __name__ == '__main__':
    # arr = [1,3,5,9,0,4]
    # print(partition(arr=arr,low=0,high= len(arr)-1))
    # print(arr)
    arr = [4, 2, 9, 6, 5, 1, 3]
    quick_sort(arr,0,len(arr)-1)
    print(arr)