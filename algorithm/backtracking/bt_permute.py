from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """返回给定数组的所有排列（LeetCode 46 全排列）

    回溯三要素：
    - 路径 path: 当前已经选择的数字序列
    - 选择列表: 还可以选择哪些数字（通过 used 标记控制）
    - 结束条件: 当 path 长度等于 nums 长度时，得到一个完整排列
    """

    res: List[List[int]] = []  # 用来收集所有结果
    path: List[int] = []       # 当前路径
    used: List[bool] = [False] * len(nums)  # 记录每个位置的数字是否已经被使用

    def backtrack(depth: int = 0) -> None:
        """回溯核心函数，不断扩展 path 直到形成一个完整解

        增加 depth 参数用于调试打印，帮助理解递归调用栈：
        - depth 表示当前递归的层数（从 0 开始），只用于缩进和观察，不参与逻辑。
        """

        print("  " * depth, "进入 depth =", depth, "path =", path)

        # 1. 结束条件：当路径长度等于 nums 的长度时，说明选满了
        if len(path) == len(nums):
            print("  " * depth, "收集结果", path)
            res.append(path[:])  # 这里要拷贝一份 path
            return

        # 2. 遍历当前这一步可以做的所有选择
        for i in range(len(nums)):
            # 如果这个数字已经在当前路径中使用过了，跳过
            if used[i]:
                continue

            # 做选择：把 nums[i] 放进路径，并标记为已使用
            used[i] = True
            path.append(nums[i])

            # 进入下一层决策树
            backtrack(depth + 1)

            # 撤销选择：回到这一步之前的状态
            path.pop()
            used[i] = False
            print("  " * depth, "回到 depth =", depth, "path =", path)

    # 从空路径开始搜索
    backtrack(0)
    return res


if __name__ == "__main__":
    # 简单自测
    print(permute([1, 2, 3]))
