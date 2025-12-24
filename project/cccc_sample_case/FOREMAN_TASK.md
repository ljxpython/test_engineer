# Foreman 示例任务：守护全栈应用的质量（React TS + FastAPI + SQLite）

> 注意：本文件仅作为 **React + TypeScript 前端 + FastAPI + SQLite 后端** 的真实示例。实际使用时，请将内容合并到仓库根目录的 `FOREMAN_TASK.md` 中，并按你的项目路径和命令进行调整。

## 一、Foreman 每次唤醒要做的事

假设项目结构为：

- 前端：`frontend/`
- 后端：`backend/`

Foreman 每次被唤醒（例如每 15 分钟）时，建议按以下顺序执行：

1. **检查后端健康与关键测试**
   - 在 `backend/` 目录执行：`pytest`。
   - 如果有用例失败：
     - 在 `context/notes` 中追加一条记录，简要说明失败的测试名和错误信息。
     - 通过 mailbox 向 PeerA / PeerB 发送摘要，建议优先修复。

2. **检查前端构建与基础测试**
   - 在 `frontend/` 目录执行：
     - `npm test`（或 `npm run test`）执行关键单元测试 / 组件测试。
     - `npm run lint` / `npm run typecheck`（如有）做基础质量检查。
   - 若前端构建或测试失败：
     - 同样记录到 `context/notes`。
     - 提醒 Peer 在下一轮自检中处理。

3. **检查 ccontext 任务进度**
   - 读取 `context/context.yaml`：
     - 关注与本应用相关的里程碑（例如 `M_FULLSTACK_MVP`、`M_API_TESTS` 等）。
   - 检查 `context/tasks/`：
     - 查找仍处于 `active` / `in_progress` 状态的任务，例如：
       - `T_BACKEND_TESTCASE_API`
       - `T_FRONTEND_TESTCASE_PAGE`
     - 如果某个任务长时间无提交或无状态更新，可提醒 Peer 拆分任务或更新进度。

4. **扫描仓库中的 TODO / FIXME**
   - 在整个仓库中搜索 `TODO` / `FIXME`，重点关注：
     - `backend/app/` 下的接口与数据一致性问题。
     - `frontend/src/` 下的交互、状态管理与错误处理 TODO。
   - 将高优先级的 TODO 汇总到一条 `context/notes` 中，方便 Peer 在后续迭代中处理。

## 二、质量门禁规则示例

为了保证这个全栈应用在持续迭代中不“越写越乱”，Foreman 可以执行以下门禁策略：

1. **后端门禁**
   - 若 `backend` 下的 `pytest` 不通过，则：
     - 标记当前检查为失败；
     - 阻止与后端相关的功能被标记为「完成」（需要 Peer 在任务文件中手动确认修复后再推进里程碑状态）。

2. **前端门禁**
   - 若 `frontend` 下的关键测试或类型检查失败，则：
     - 建议不要将对应功能合入主分支；
     - 提醒 Peer 补齐测试或修复类型问题后再发起 RFD 申请合并。

3. **变更与测试绑定**
   - 当 Foreman 在 `ledger.jsonl` 或提交信息中检测到：
     - 有对 `backend/app/routers/` 或 `frontend/src/pages/` 的改动，
   - 但本轮检查中没有新增或更新对应测试文件（例如 `tests/` 或 `*.test.tsx`），则：
     - 在 `context/notes` 里记录一条「潜在未配套测试」的提醒；
     - 鼓励 Peer 在下一轮迭代中补齐测试。

## 三、适合作为长期常驻任务的项

可以在 `FOREMAN_TASK.md` 顶部写明以下长期目标，由 Foreman 在每次唤醒时顺带检查：

- 定期统计：
  - 已实现的后端 API 数量，与对应的测试用例数（大致对应即可，不必精确到 1:1）。
  - 主要页面（用例列表页、详情页、执行记录页）的前端测试覆盖情况。
- 定期提醒：
  - 将重要结论（例如「某个接口的性能瓶颈」「某类错误出现频率高」）整理进 `context/context.yaml` 的 `notes` 或 `milestones` 中，而不是只保留在对话里。
- 选做：
  - 定期检查依赖版本（npm / Python），在安全可控的范围内建议 Peer 做小步升级。

## 四、如何应用到你自己的项目

- 将本文件内容复制到你项目根目录的 `FOREMAN_TASK.md` 中，然后：
  - 把 `frontend/`、`backend/` 换成你的真实路径；
  - 把测试命令改成你实际使用的脚本（例如 `pnpm`、`poetry run pytest` 等）；
  - 补充你团队惯用的门禁规则（例如强制通过 E2E 测试、强制检查 CI 状态等）。
- 启用 Foreman 后，它会按这里的规则定期提醒和压实质量，和双 Peer 的日常开发形成闭环。

