# CCCC Pair 使用实践指南

> 本文档说明：如何在本项目中实战使用 **CCCC Pair（双 AI 自主协作编排器）**，让两个 AI 长时间自动协作完成开发 / 测试任务。

---

## 1. CCCC 在本项目中要干什么？

在本项目中，我们把 CCCC 当成一个“**双 AI 小组长 + 自动监工**”：

- 你负责：  
  - 说明项目背景、当前目标、约束条件（写在 `PROJECT.md` / `FOREMAN_TASK.md` / 任务文件里）。  
  - 在关键节点做决策（RFD 请求时给出批准或调整）。

- CCCC 负责：  
  - 启动两个 AI Agent（PeerA / PeerB），自动沟通、分工、互相 review。  
  - 跑测试、改代码、更新 `context/` 里的任务进度。  
  - Foreman 定期巡检，保证测试和里程碑不“烂尾”。

适用的典型场景：

- 为已有代码补齐或改进 **自动化测试**（单元 / API / UI）。  
- 在既有架构下，实现一个中小型新功能（CRUD 接口、小工具、小脚本）。  
- 对一块已有模块做“重构 + 覆盖率提升”，并保持测试绿灯。  
- 持续处理一批重复性任务（格式修正、简单重构、日志统一等）。

---

## 2. 环境准备

在开始前，请确保：

- 系统依赖  
  - `Python >= 3.9`  
  - `tmux`（多窗格终端）  
    - macOS：`brew install tmux`  
    - Ubuntu/Debian：`sudo apt install tmux`  
    - Windows：需要在 WSL 中使用（例如 Ubuntu on WSL），并在 WSL 终端中安装与运行 CCCC  
  - `git`

- 至少安装一个 Agent CLI（推荐选 1~2 个用）：

  ```bash
  # Claude Code（推荐起步）
  npm install -g @anthropic-ai/claude-code

  # 可选：Codex CLI
  npm install -g @openai/codex

  # 可选：Gemini CLI
  npm install -g @anthropic-ai/gemini-cli

  # 可选：OpenCode
  go install github.com/opencode-ai/opencode@latest
  ```

- 安装 CCCC Pair 本体（推荐 `pipx` 隔离环境）：

  ```bash
  pip install pipx         # 若未安装 pipx
  pipx install cccc-pair   # 安装 CCCC Pair

  # 或者直接
  # pip install cccc-pair
  ```

---

## 3. 第一次接入：从 0 到能跑

> 以下步骤都在你要让 CCCC 接管的项目根目录执行。

### 3.1 初始化 CCCC

```bash
cd your-project-root  # 切到本项目根目录

# 第一次初始化（生成 .cccc/ 配置 & 基础结构）
cccc init

# 检查环境是否就绪（缺什么会提示）
cccc doctor
```

执行完后，项目中会多出几个关键目录 / 文件：

- `.cccc/`：CCCC 自己的编排器域（配置、日志、状态等）。  
- `context/`：共享上下文和任务追踪（ccontext 兼容）。  
- （如果不存在）建议你手动创建并维护：`PROJECT.md`、`FOREMAN_TASK.md`。

### 3.2 编写 `PROJECT.md` —— 对 AI 说“我们是谁、要干啥”

在项目根目录创建或补充 `PROJECT.md`，它会被自动注入 PeerA / PeerB 的系统提示词，相当于“项目说明书”。

示例（针对测试开发项目可以这样写）：

```markdown
# 项目简介
这是一个测试工程示例项目，包含：
- 若干算法练习代码
- Web 应用（示例）
- API/UI 自动化测试代码

技术栈：
- Python + Pytest
- Playwright（UI 自动化）
- SQLite / 简单文件存储

# 当前阶段重点目标
1. 补充关键模块的单元测试，提高测试覆盖率（目标 > 80%）
2. 保持现有测试全部为绿（不得忽略失败测试）
3. 在重构时保证行为等价，并通过回归测试验证

# 代码与协作规范
- 保持函数有清晰的 docstring 和类型注解
- 新增功能必须有对应自动化测试
- 对外行为不明时，优先通过阅读现有测试和运行代码来获得结论
- 出现疑问时，优先在 context 中补充 notes，而不是随意猜测实现
```

请根据你的真实项目情况调整技术栈和目标。

### 3.3 编写 `FOREMAN_TASK.md` —— 给 Foreman 的巡检清单

`FOREMAN_TASK.md` 是给 Foreman（监工）看的定期任务清单。示例：

```markdown
# Foreman 巡检任务（本项目）

## 每次巡检须执行
1. 运行 `pytest`，若存在失败测试必须在日志中明确标记，并提醒 Peer 修复
2. 检查 context/context.yaml 中 milestones 的状态是否合理：
   - 不允许长时间 active 但无 notes 或任务更新
3. 检查 context/tasks/ 下是否有长时间 pending 的步骤，提醒 Peer 拆解或关闭

## 质量门禁要求
- 不允许忽略/跳过失败测试
- 不允许在未更新 context/tasks/ 的情况下声称“任务完成”
- 新增的关键逻辑必须有至少 1 个自动化测试样例
```

后续你可以按需要扩展，比如增加“定期更新文档”“检查日志告警”等。

---

## 4. 日常使用：如何让双 AI 真正帮你干活

### 4.1 启动 / 停止

在项目根目录：

```bash
# 启动 CCCC（会打开 tmux 四窗格布局）
cccc run
```

首次启动会弹出一个 TUI Setup 面板，让你选择各角色使用哪个 CLI：

- PeerA：推荐先选 Claude Code。  
- PeerB：可以同样选 Claude Code，或者选择另一套 CLI；如果暂时只想用一个 AI，就把 PeerB 设为 `none`。

停止时可以：

- 在 TUI 中用 `/quit`。  
- 或者在外部终端用 `cccc kill` 结束编排器。

### 4.2 给 AI 下达任务（实践范例）

假设当前目标是“补齐登录模块测试，提高覆盖率到 80%”，你可以在 TUI 中这样开始对话：

```text
both: 当前目标是提高登录模块的测试覆盖率到 80%，请你们先一起梳理现有测试情况，总结缺口，再给出一个分步执行计划。
```

接下来可以用类似的指令驱动它们：

```text
a: 你负责先审查现有登录模块测试，列出缺失的测试场景和风险点，并更新 context/tasks 下的任务列表。
b: 你根据 PeerA 的任务拆解，优先实现最关键的测试用例，并保证 pytest 全绿。
```

过程中，你可以随时插话：

```text
a: 注意优先关注安全相关场景（暴力破解、多次失败锁定、密码复杂度等）。
b: 重构前先写回归测试，不要直接动核心逻辑。
```

### 4.3 常用 TUI 命令

在 TUI 输入框中（支持 Tab 补全）：

- `/a <消息>`：只对 PeerA 说话。  
- `/b <消息>`：只对 PeerB 说话。  
- `/both <消息>`：广播给两个 Peer。  
- `/pause` / `/resume`：暂停/恢复 handoff（消息进 inbox 但暂不投递）。  
- `/restart peera|peerb|both`：重启对应 Peer 的 CLI 进程。  
- `/aux <提示>`：临时叫 Aux 跑一次重任务（例如“跑一次完整 UI 回归”）。  
- `/foreman on|off|status|now`：开关 / 查询 Foreman。  
- `/help`：查看命令帮助。

也可以不用斜杠，用冒号自然路由：

```text
a: 帮我检查刚刚那次重构是否引入潜在性能问题
b: 重新跑一遍和订单相关的集成测试
both: 对当前里程碑做一个总结，并更新 context/context.yaml
```

---

## 5. 任务寿命管理：一个阶段结束后怎么办？

当你觉得“本轮任务差不多完成了”，例如：

- 当前里程碑已经完成。  
- 或者 context/tasks 里主要任务都 complete。  

你可以重置 CCCC 的运行状态，以干净的视角开始下一轮：

```bash
# 在项目根目录
cccc reset           # 清理 state/mailbox/logs/work 和任务文件
# 或
cccc reset --archive # 先把任务归档到带时间戳目录，再清理
```

> 建议先 `cccc kill` 结束当前运行，再执行 `cccc reset`，避免状态被同时修改。

---

## 6. 最佳实践与注意事项

- **务必认真写好 `PROJECT.md` 和 `FOREMAN_TASK.md`**  
  - 它们决定 AI 是否真的理解你的项目和目标。  
  - 随着项目演进，可以定期更新这两个文件，让 AI 跟上节奏。

- **善用 `context/` 作为“项目大脑”**  
  - `context/context.yaml`：愿景、里程碑、长期笔记。  
  - `context/tasks/`：任务与步骤，建议在重要变更前后都让 AI 更新这里。  
  - 这样你可以跨 session、跨天续接工作，而不需要重新解释一遍。

- **先从小目标练手**  
  - 建议先选一个风险小、影响面小的任务（比如补一块模块测试），让 CCCC 跑一两轮，熟悉它的行为。  
  - 等你熟悉它的节奏后，再交给它更大范围的重构或功能开发。

- **任何时候都可以插手**  
  - CCCC 的设计并不是替代你，而是“你 + 两个 AI 合作”。  
  - 当你觉得方向不对、质量不够、节奏太快/太慢，都可以直接在 TUI/IM 里下达指令进行干预。

---

> 如需更进阶配置（Telegram/Slack/Discord/WeCom 桥接、Agent CLI 组合策略等），请参考 CCCC 官方 README 或在本文件基础上补充你自己的团队规范。

