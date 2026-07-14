# 智教通仓库专业化整理设计

## 目标

在不丢失竞赛资料和现有产品实现的前提下，将 GitHub 仓库整理为结构清晰、可自动验证、便于协作者快速上手的专业项目仓库，并使当前前端重设计 Pull Request 恢复为可合并状态。

## 当前问题

- Pull Request #1 基于较早的前端分支演进，与后来完成目录整理的 `main` 存在冲突。
- 根目录混入 Office `~$` 临时锁文件和 `distill_query*.py` 一次性脚本。
- 竞赛通知、报名表、项目任务文档散落在根目录，但用户要求完整保留。
- `landing-page` 与 `source/frontend` 存在重复页面与重复素材，没有明确的正式实现边界。
- README 的功能、目录、启动说明与当前实现不一致，仓库 URL 和团队信息也缺乏可维护性。
- 仓库没有 CI、贡献指南、安全说明、Issue 模板或 PR 模板。
- GitHub 简介含糊，未设置 Topics，也没有自动化状态检查。
- 默认分支和多个历史分支未受保护，但分支删除和保护规则属于后续治理范围。

## 整理原则

1. 保留产品代码、竞赛原始材料和有价值的设计/QA 记录。
2. 删除可确定为缓存、锁文件或一次性本地工具的内容。
3. 只保留一个正式前端入口：`source/frontend`。
4. 使用 `git mv` 保留文件演进关系，避免复制后删除造成无意义差异。
5. 使用普通 merge 同步 `origin/main`，不重写已推送分支历史。
6. 所有结构调整必须由自动化测试、构建和文档链接检查验证。

## 目标目录

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── docs/
│   ├── competition/
│   │   ├── source/           # 通知、报名表等原始材料
│   │   └── project/          # 任务手册、项目梳理等项目材料
│   ├── design/               # 已确认的产品与交互设计规格
│   ├── guides/               # 环境配置和技术栈说明
│   ├── quality/              # QA 报告与必要截图
│   └── archive/              # 历史实施计划和环境搭建记录
├── source/
│   ├── frontend/             # 唯一正式前端
│   └── backend/              # FastAPI 后端
├── CONTRIBUTING.md
├── SECURITY.md
├── README.md
└── .gitignore
```

`AGENTS.md` 和 `.mimocode` 属于现有协作配置，保持原位。旧 `landing-page` 不再作为正式入口；确认其有效内容已被 `source/frontend` 覆盖后，从当前树中移除，历史版本仍可通过 Git 找回。

## 冲突处理

1. 获取最新 `origin/main`。
2. 在 `codex/eastern-future-ui-design` 上执行普通 merge。
3. 对产品代码冲突优先保留已通过 71 项测试的新版前端。
4. 对文档和目录冲突优先采用 `main` 的去重意图，再按本设计归档。
5. 合并完成后重新计算 PR 差异，确保不再重新引入已从 `main` 清理的重复文件。
6. 禁止 force push 和历史重写。

## 文件整理

### 竞赛资料

- 通知和报名表移动到 `docs/competition/source/`。
- 任务模块手册、项目任务模块手册和项目梳理移动到 `docs/competition/project/`。
- README 增加竞赛资料入口，但不把原始报名信息直接展示在首页。
- Office 临时锁文件 `~$*` 删除，并加入 `.gitignore`。

### 开发文档

- `docs/环境配置指南.md` 和 `docs/技术栈说明.md` 移动到 `docs/guides/`。
- 已确认设计规格移动到 `docs/design/`。
- QA 报告和截图移动到 `docs/quality/`。
- 详细实施计划、Compose 环境搭建记录移动到 `docs/archive/`。
- 文档中的相对链接在迁移后同步更新。

### 临时与重复内容

- 删除根目录 `distill_query.py`、`distill_query2.py`、`distill_query3.py`。
- 删除 Office 锁文件和本地 Visual Companion 目录规则遗漏。
- 移除已被正式 Vue 应用覆盖的 `landing-page` 目录。
- 不在本次任务中清理 Git 历史中的旧大文件；只优化当前工作树。

## README 与协作规范

README 使用中文为主，包含：

- 一句话价值说明和核心功能。
- 教师端、学生端和生命水墨首页的功能概览。
- Vue/FastAPI 架构和目录说明。
- Windows、macOS、Linux 可执行的前后端启动步骤。
- 演示模式、环境变量、测试、构建命令。
- 文档索引、贡献流程和安全问题入口。
- 当前许可证状态说明，不擅自选择开源许可证。

`CONTRIBUTING.md` 规定分支命名、Conventional Commits、测试要求和 PR 流程。`SECURITY.md` 提供私下报告安全问题的方式，避免在公开 Issue 中披露漏洞或密钥。

## GitHub 自动化与元数据

### CI

新增 GitHub Actions：

- 前端：`npm ci`、`npm test -- --run`、`npm run build`。
- 后端：安装 `requirements.txt` 并运行现有 pytest 测试。
- 工作流在 Pull Request 和 `main` push 时触发，使用依赖缓存。

### 模板

- PR 模板要求填写变更概要、测试证据、截图和风险。
- Bug Issue 模板要求复现步骤、期望结果、环境和日志。
- Feature Issue 模板要求说明用户价值、范围和验收标准。

### 仓库设置

- 简介更新为“智教通：面向教师与学生的 AI 智能体教学辅助平台，提供需求引导、工具推荐、AI 问答与学习轨迹”。
- Topics 设置为 `education`、`edtech`、`ai`、`intelligent-agent`、`vue`、`fastapi`、`chinese`。
- 暂不设置 Homepage，因为当前没有已确认的公开部署地址。

## 本次不执行

- 不重命名仓库；当前 `-` 名称虽然不理想，但改名会影响 clone URL 和协作链接。
- 不选择或添加许可证；许可证需要仓库所有者明确决定。
- 不重写 Git 历史或使用 force push。
- 不删除远程历史分支。
- 不启用分支保护或关闭 Issues、Projects、Wiki。
- 不合并 Pull Request；整理完成后仍由协作者审阅。

这些事项会在整理完成后形成单独的 GitHub 治理建议。

## 验证标准

- PR 不再显示 `CONFLICTING`。
- 根目录无 Office 锁文件和一次性查询脚本。
- 所有保留的竞赛资料可从 `docs/competition/` 找到。
- README 中所有仓库内链接可解析。
- 前端完整测试和生产构建通过。
- 后端现有测试通过；若基线失败，记录具体失败并修复本次整理引起的问题。
- GitHub Actions YAML 可解析，工作流被 GitHub 识别。
- PR 模板、Issue 模板、贡献指南和安全说明可访问。
- GitHub 简介和 Topics 与项目定位一致。
- Pull Request #1 更新后仍保留完整提交历史和评审链接。
