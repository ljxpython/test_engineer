# Backtracking 学习索引

本目录包含：
- 学习计划：`backtracking_learning_plan.md`
- 题目与文件索引（建议逐步实现）：
  - 46 全排列 → `bt_permute.py`
  - 47 全排列 II → `bt_permute_unique.py`
  - 77 组合 → `bt_combine_k.py`
  - 39 组合总和 → `bt_combination_sum.py`
  - 40 组合总和 II → `bt_combination_sum2.py`
  - 78 子集 → `bt_subsets.py`
  - 90 子集 II → `bt_subsets_with_dup.py`
  - 22 括号生成 → `bt_generate_parentheses.py`
  - 131 分割回文串 → `bt_palindrome_partition.py`
  - 93 复原 IP 地址 → `bt_restore_ip.py`
  - 51/52 N 皇后 → `bt_n_queens.py`
  - 37 数独求解 → `bt_sudoku_solver.py`
  - 79 单词搜索 → `bt_word_search.py`
  - 490/200/130 迷宫/岛屿/被围绕区域 → `bt_grid_paths.py`

## 代码约定
- 每个文件提供 `solve()` 或同名函数，以及 `if __name__ == '__main__':` 的基础自测。
- 文件头部注明：LeetCode 题号、题名、链接、时间/空间复杂度目标。

## 快速开始
1. 先阅读 `backtracking_learning_plan.md`。
2. 从 46/77/39 开始实现（排列、组合、组合总和），逐步加入剪枝/去重。
3. 完成后在本目录补充你自己的笔记与边界用例。