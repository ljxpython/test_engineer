'''
54题目
给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]

输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]

'''

# 这道题我就不写具体代码了,只写一个思路



class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        # 处理空矩阵
        if len(matrix) == 0:
            return []
        result = []

        # 矩阵的宽,高
        wight,high = len(matrix[0])-1,len(matrix)-1
        # 旋转时的起始点
        top_wight,top_high = 0,0
        # 当上下边界和不重合时,循环,每次旋转一圈
        while wight >= top_wight and high >= top_high:
            pass



"""

class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        if not matrix or not matrix[0]:  # 处理空矩阵
            return []
        
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        
        while top <= bottom and left <= right:
            # 1. 从左到右遍历上边界
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1  # 上边界下移
            
            # 2. 从上到下遍历右边界
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1  # 右边界左移
            
            # 3. 从右到左遍历下边界（需检查上边界是否仍在下方）
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1  # 下边界上移
            
            # 4. 从下到上遍历左边界（需检查左边界是否仍在右方）
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1  # 左边界右移
        
        return result


if __name__ == '__main__':
    s = Solution()
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    res = s.spiralOrder(matrix=matrix)  
    print(res)  # 输出: [1, 2, 3, 6, 9, 8, 7, 4, 5]


"""





if __name__ == '__main__':
    s = Solution()
    matrix =[[1,2,3],[4,5,6],[7,8,9]]
    res = s.rotate(matrix=matrix)
    print(res)

