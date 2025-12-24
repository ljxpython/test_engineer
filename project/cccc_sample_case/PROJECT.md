# 示例项目：测试用例管理全栈应用（React TS + FastAPI + SQLite）

> 注意：本目录仅作为 CCCC Pair 的**完整真实案例**。实际使用时，建议把这里的内容拷贝/合并到你自己项目根目录下的 `PROJECT.md` 中，并按实际情况修改项目名、仓库地址等信息。

## 一、项目背景

本示例是一个 **“测试用例与执行记录管理”** 的全栈应用，主要面向测试工程师 / 测试开发工程师：

- 前端：使用 **React + TypeScript** 实现一个单页应用（SPA）。
- 后端：使用 **Python 3.13 + FastAPI** 暴露 RESTful API。
- 数据库：使用 **SQLite** 作为嵌入式数据库，方便本地开发与 CI 运行。

主要业务能力：

- 管理测试用例（创建 / 编辑 / 删除 / 按模块分类）。
- 记录某次执行结果（通过 / 失败 / 阻塞、执行时间、执行人）。
- 支持简单的查询与过滤（按模块、按标签、按状态筛选）。

## 二、目录结构建议

示例仓库结构（仅作为说明，可按需调整）：

```text
your-project/
  frontend/                 # React + TS 前端
    src/
      components/
      pages/
      api/                  # 前端调用后端的 API 封装
    package.json
    tsconfig.json
    vite.config.ts 或 webpack 配置

  backend/                  # FastAPI + SQLite 后端
    app/
      main.py               # FastAPI 入口
      models.py             # Pydantic / ORM 模型
      db.py                 # SQLite 初始化与会话管理
      routers/
        testcases.py        # 测试用例相关接口
        runs.py             # 执行记录相关接口
    pyproject.toml 或 requirements.txt

  context/                  # ccontext 上下文（由 CCCC Pair 维护）
  PROJECT.md                # 可由本文件内容初始化
  FOREMAN_TASK.md           # 可由示例 FOREMAN_TASK 初始化
```

## 三、核心业务需求

1. **测试用例管理**
   - 字段：`id`、`title`、`module`（模块）、`steps`、`expected_result`、`priority`、`tags`、`created_at`、`updated_at`。
   - API 示例：
     - `GET /api/testcases`：分页 + 条件查询。
     - `POST /api/testcases`：创建新用例。
     - `PUT /api/testcases/{id}`：更新用例。
     - `DELETE /api/testcases/{id}`：删除用例（软删或硬删可配置）。

2. **执行记录管理**
   - 字段：`id`、`testcase_id`、`result`（pass/fail/blocked）、`executor`、`executed_at`、`comment`。
   - API 示例：
     - `GET /api/runs?testcase_id=` 查询某用例历史记录。
     - `POST /api/runs` 创建执行记录。

3. **前端功能**
   - 用例列表页：支持搜索、按模块/标签过滤、按优先级排序。
   - 用例详情页：支持查看、编辑步骤与预期结果，查看历史执行记录。
   - 执行记录表单：选择结果、填写备注并提交。

## 四、技术栈与约定

- 前端：
  - React 18 + TypeScript。
  - 使用 Vite 或 Create React App 创建项目。
  - UI 库可选：Ant Design / MUI / Tailwind 等，示例中不强制。

- 后端：
  - Python 3.13。
  - FastAPI + Uvicorn。
  - SQLite 通过 `sqlite3` 或 SQLAlchemy / SQLModel 管理。

- 通用约定：
  - 所有对外 API 前缀统一为 `/api`，返回 JSON。
  - 必要字段做基础校验（长度、必填、枚举值等）。
  - 新增接口必须至少有一个对应的自动化测试（后端单测或 API 测试）。

## 五、开发与运行命令示例

> 以下命令假设前后端在 `frontend/` 与 `backend/` 目录中，实际使用时请按你的真实路径调整。

- 启动后端（开发环境）：
  - `cd backend`
  - `uvicorn app.main:app --reload`

- 启动前端（开发环境）：
  - `cd frontend`
  - `npm install`
  - `npm run dev`

- 运行后端测试：
  - `cd backend`
  - `pytest`

- 运行前端测试 / 类型检查：
  - `cd frontend`
  - `npm test` 或 `npm run test`
  - `npm run lint` / `npm run typecheck`

## 六、建议交给 CCCC Pair 的工作流

下面是一条可以直接交给 CCCC Pair（双 Peer）的「从 0 到 1」开发路径，便于你参考：

1. 初始建项
   - PeerA：创建 `backend` 目录，搭建 FastAPI + SQLite 骨架，完成 `/health` 健康检查接口。
   - PeerB：创建 `frontend` 目录，搭建 React + TS 项目，完成基础路由和布局组件。

2. 用例模型与 API
   - PeerA：在 `backend/app/models.py` 与 `backend/app/routers/testcases.py` 中实现用例模型和 CRUD API；补充后端测试。
   - PeerB：在 `frontend/src/api/testcases.ts` 中封装对应的 API 调用，并在 `pages/TestcaseList` 中渲染列表。

3. 执行记录与详情页
   - PeerA：实现执行记录数据表与 `/api/runs` 相关接口，确保关联用例 ID。
   - PeerB：在用例详情页中加载执行记录列表，并实现新执行记录的提交表单。

4. 联调与质量保障
   - 双方：
     - 联调前后端接口，确保 CORS / JSON 结构一致。
     - 收敛关键路径（创建用例 → 执行一次 → 查看历史）的自动化测试。
     - 使用小步提交+代码 review 的方式推进。

## 七、与根目录 PROJECT.md 的关系

- 你可以直接把本文件复制为自己项目根目录的 `PROJECT.md`，然后：
  - 修改应用名称、业务领域；
  - 根据团队真实命令调整启动 / 测试脚本；
  - 把「建议交给 CCCC Pair 的工作流」部分改写成你希望双 Peer 实际去做的任务。
- 也可以保留本目录作为「模板案例」，在不同项目中反复复用。

