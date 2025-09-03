'''

给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。

输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]

输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

'''


# 这题还要理解一点矩阵的知识,做这个题的时候有点无语了
# 知道矩阵的基础,其实做这个题是很简单的
# 所谓的90度顺时针旋转,其实是先转置,之后每行翻转
# 所谓的90度逆时针旋转,其实是先翻转每行再转置


class Solution(object):
    def rotate(self, matrix:list[list[int]]):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        num = len(matrix)
        for i in range(num):
            for j in range(i,num):
                matrix[i][j] ,matrix[j][i] = matrix[j][i],matrix[i][j]
        for i in range(num):
            matrix[i] = matrix[i][::-1]
        return matrix


if __name__ == '__main__':
    s = Solution()
    matrix =[[1,2,3],[4,5,6],[7,8,9]]
    res = s.rotate(matrix=matrix)
    print(res)

