# 指标口径与采集来源（测试管理度量手册）

> 目的：统一指标定义与计算口径，明确采集来源与看板字段，避免不同项目口径不一致。

---

## 1. 质量类
- 逃逸缺陷率（Escape Rate）
  - 定义：生产发现缺陷数 / 全部缺陷数（生产+测试）
  - 口径：统计周期内按严重级汇总（建议关注严重/高）
  - 来源：缺陷平台（Jira/禅道），生产告警系统
  - 看板字段：escape_rate_total、escape_rate_blocker_high

- 缺陷密度（Defect Density）
  - 定义：缺陷数 / 需求点（或每千行代码KLOC）
  - 来源：缺陷平台 + 需求管理平台（需求计数）/代码平台（KLOC）
  - 看板字段：defect_density_per_story、defect_density_per_kloc

- 严重缺陷拦截率
  - 定义：发布前发现的严重/致命缺陷数 / 严重/致命缺陷总数
  - 来源：缺陷平台 + 发布单
  - 看板字段：sev_blocker_intercept_rate

## 2. 效率类
- 回归周期（Regression Cycle Time）
  - 定义：从回归启动到回归完成的总时长
  - 来源：CI日志（回归任务）、测试排期记录
  - 看板字段：regression_cycle_hours

- 平均修复时长（MTTR）
  - 定义：从缺陷被确认到修复验证通过的平均时长
  - 来源：缺陷平台状态时间戳
  - 看板字段：defect_mttr_hours

- 按期率（On-time Rate）
  - 定义：按计划发布时间准时发布的比例
  - 来源：发布单/里程碑记录
  - 看板字段：release_on_time_rate

## 3. 覆盖/稳定类
- 自动化覆盖率（Automation Coverage）
  - 定义：关键路径覆盖的比例（或满足率）
  - 来源：测试管理/用例库 + CI 测试结果
  - 看板字段：auto_cov_key_path、auto_cov_total

- 构建成功率（Build Success Rate）
  - 定义：成功构建次数 / 总构建次数
  - 来源：CI/CD
  - 看板字段：build_success_rate

- 关键路径通过率
  - 定义：关键路径用例通过数 / 关键路径用例总数
  - 来源：测试执行平台/CI
  - 看板字段：key_path_pass_rate

## 4. 协作/流程类
- 阻塞平均处理时长
  - 定义：阻塞项从提出到解除的平均时长
  - 来源：看板任务状态时间戳（Jira状态流/自定义字段）
  - 看板字段：blocker_avg_duration_hours

- 冲突升级次数
  - 定义：跨团队冲突触发升级流程的次数
  - 来源：会议纪要/升级记录（建议表单化收集）
  - 看板字段：conflict_escalations

- 结论采纳率
  - 定义：测试结论被对应责任人采纳并完成闭环的比例
  - 来源：一页纸周报+结论-行动绑定清单
  - 看板字段：conclusion_adoption_rate

---

## 数据对接建议
- 统一事实源：需求/任务/缺陷/CI/发布单在同一数据域做关联键（issue_key、build_id、release_id）
- CI 接入：将关键测试结果（通过率、失败用例列表）以 API 或 artifact 形式输出，供看板拉取
- 缺陷平台：启用状态时间戳与严重级字段，保证统计可用
- 一页纸与看板：每条结论绑定责任人/截止期/校验标准（Definition of Success）

## 注意事项
- 指标只做“有用的统计”：能用于决策与改进；避免唯指标论
- 版本化：记录计算口径版本，避免历史不可比
- 透明化：在团队内对口径进行宣贯，确保一致理解

