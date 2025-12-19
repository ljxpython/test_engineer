"""

以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。



示例 1：

输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
示例 2：

输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
示例 3：

输入：intervals = [[4,7],[1,4]]
输出：[[1,7]]
解释：区间 [1,4] 和 [4,7] 可被视为重叠区间。


提示：

1 <= intervals.length <= 104
intervals[i].length == 2
0 <= starti <= endi <= 104


合并区间的思想,如果 [a,b] [c,d]  : 用b 和cd比较,如果b < c 那么就不需要合并 如果b> c,那么就合并bcd中比较大的

"""

class Solution(object):
    def merge(self, intervals:list):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        #不管什么情况先考虑为空的情况
        if len(intervals) == 0:
            return []
        # 对原列表进行排序
        intervals.sort(key=lambda x :x[0])
        merge_list = [intervals[0]]
        # 对intervals本身进行排序
        for i in range(1 ,len(intervals)):
            # 取merge最新的
            merge_list_last = merge_list[-1]
            # 取当期的
            current_element = intervals[i]
            # 开始判断是否合并
            if merge_list_last[1] < current_element[0]:
                merge_list.append(current_element)
            else:
                merge_list[-1][1] = max(merge_list_last[1],current_element[1])
        return merge_list


