# 智教通仓库专业化整理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在完整保留竞赛正式资料和新版产品实现的前提下，将仓库整理为结构清晰、可自动验证、便于协作者上手且当前 Pull Request 可合并的专业项目仓库。

**Architecture:** 先用普通 merge 将 `origin/main` 合入当前功能分支并解决冲突，再通过 `git mv` 将竞赛材料、开发指南、设计规格和 QA 记录归入稳定目录。`source/frontend` 作为唯一正式前端，根 README、协作规范、GitHub 模板和双端 CI 共同构成仓库入口与质量门禁。

**Tech Stack:** Git、GitHub Actions、Vue 3、Vite、Vitest、FastAPI、pytest、Markdown、YAML

---

### Task 1: 同步默认分支并消除 PR 冲突

**Files:**
- Modify: `source/frontend/`（仅在 merge 冲突时保留新版前端实现）
- Modify: 根目录和 `docs/`（仅在 merge 冲突时保留 `main` 的去重意图，随后由后续任务归档）

- [ ] **Step 1: 获取远程状态并记录当前基线**

Run:

```powershell
git fetch origin --prune
git status -sb
git log --oneline --decorate -5
```

Expected: 当前分支为 `codex/eastern-future-ui-design`，除被忽略的本地 `.superpowers/` 外没有待提交改动。

- [ ] **Step 2: 运行前后端基线测试**

Run:

```powershell
Push-Location source/frontend; npm test -- --run; npm run build; Pop-Location
Push-Location source/backend; python -m pytest; Pop-Location
```

Expected: 前端 Vitest 全部通过且 Vite 构建成功；后端 6 项 pytest 全部通过。

- [ ] **Step 3: 使用普通 merge 同步 `origin/main`**

Run:

```powershell
git merge --no-ff origin/main
```

Expected: merge 成功，或只产生可人工判定的产品代码/文档冲突；不得 rebase 或 force push。

- [ ] **Step 4: 解决冲突并检查结果**

对 `source/frontend/` 冲突保留已通过测试的东方未来主义新版实现；对根目录和文档冲突保留 `main` 的有效正式资料和去重结果。随后运行：

```powershell
git diff --name-only --diff-filter=U
git status --short
```

Expected: 第一条命令无输出；正式竞赛 DOCX 和任务文档仍存在于工作树。

- [ ] **Step 5: 重新验证并提交 merge**

Run:

```powershell
Push-Location source/frontend; npm test -- --run; npm run build; Pop-Location
Push-Location source/backend; python -m pytest; Pop-Location
git diff --check
git commit
```

Expected: 全部检查通过，生成普通 merge commit。

### Task 2: 清理根目录并归档竞赛资料

**Files:**
- Modify: `.gitignore`
- Delete: `distill_query.py`
- Delete: `distill_query2.py`
- Delete: `distill_query3.py`
- Delete: `~$*.docx`
- Move: `关于举办湖南省第22届大学生计算机程序设计竞赛校内预选赛暨湖南师范大学大学生计算机程序设计竞赛的通知.docx` → `docs/competition/source/`
- Move: `附件1_2026年湖南省程序设计竞赛（应用开发）报名表.docx` → `docs/competition/source/`
- Move: `任务模块手册.md` → `docs/competition/project/`
- Move: `项目任务模块手册.md` → `docs/competition/project/`
- Move: `项目梳理.md` → `docs/competition/project/`

- [ ] **Step 1: 扩充本地生成物忽略规则**

在 `.gitignore` 中加入：

```gitignore
# Local assistant and editor state
.superpowers/
~$*

# Test and coverage output
coverage/
.coverage
.pytest_cache/
```

- [ ] **Step 2: 删除确定无保留价值的临时文件**

Run:

```powershell
git rm -- distill_query.py distill_query2.py distill_query3.py
git rm -- '~$*.docx'
```

Expected: 三个一次性查询脚本和两个 Office 锁文件进入删除暂存区，正式 DOCX 不受影响。

- [ ] **Step 3: 用 `git mv` 归档所有正式竞赛材料**

Run:

```powershell
New-Item -ItemType Directory -Force docs/competition/source, docs/competition/project | Out-Null
git mv -- '关于举办湖南省第22届大学生计算机程序设计竞赛校内预选赛暨湖南师范大学大学生计算机程序设计竞赛的通知.docx' docs/competition/source/
git mv -- '附件1_2026年湖南省程序设计竞赛（应用开发）报名表.docx' docs/competition/source/
git mv -- '任务模块手册.md' docs/competition/project/
git mv -- '项目任务模块手册.md' docs/competition/project/
git mv -- '项目梳理.md' docs/competition/project/
```

Expected: 通知和报名表位于 `source/`，三份项目文档位于 `project/`；若 `main` 去重后只保留其中一份任务手册，则移动所有实际存在的正式文件，不创建重复副本。

- [ ] **Step 4: 验证并提交根目录整理**

Run:

```powershell
Get-ChildItem docs/competition -Recurse -File
git ls-files | Select-String '(^|/)~\$|distill_query'
git diff --check
git add .gitignore docs/competition
git commit -m "chore: archive competition materials"
```

Expected: 竞赛资料清单完整，临时文件搜索无输出，提交成功。

### Task 3: 重组开发文档并修复链接

**Files:**
- Create: `docs/README.md`
- Move: `docs/环境配置指南.md` → `docs/guides/环境配置指南.md`
- Move: `docs/技术栈说明.md` → `docs/guides/技术栈说明.md`
- Move: `docs/superpowers/specs/*` → `docs/design/`
- Move: `docs/superpowers/reports/*` → `docs/quality/`
- Move: `docs/compose/*` → `docs/archive/compose/`
- Move: `docs/superpowers/plans/*` → `docs/archive/plans/`

- [ ] **Step 1: 创建目标目录并迁移指南与设计规格**

Run:

```powershell
New-Item -ItemType Directory -Force docs/guides, docs/design, docs/quality, docs/archive/compose, docs/archive/plans | Out-Null
git mv docs/环境配置指南.md docs/guides/
git mv docs/技术栈说明.md docs/guides/
git mv docs/superpowers/specs/* docs/design/
```

Expected: 环境/技术指南与所有已确认设计规格进入目标目录。

- [ ] **Step 2: 迁移 QA 报告、截图和历史计划**

Run:

```powershell
git mv docs/superpowers/reports/* docs/quality/
git mv docs/compose/* docs/archive/compose/
git mv docs/superpowers/plans/* docs/archive/plans/
```

Expected: `docs/quality/screenshots/` 保留全部 QA 截图；计划与 Compose 记录归入 `docs/archive/`。

- [ ] **Step 3: 修复迁移后的内部链接**

将原 `docs/compose/plans/2026-07-11-environment-setup.md` 中的 `../reports/environment-setup.md` 更新为迁移后可解析的 `../reports/environment-setup.md`（在 `docs/archive/compose/plans/` 到同级 reports 仍保持此路径），并搜索全部 Markdown 链接确认不存在旧 `docs/superpowers` 或 `docs/compose` 路径。

Run:

```powershell
Get-ChildItem docs -Recurse -Filter *.md | Select-String 'docs/(superpowers|compose)|\.\./reports/'
```

Expected: 仅保留迁移后仍能解析的 `../reports/environment-setup.md`，没有指向旧根路径的链接。

- [ ] **Step 4: 创建文档索引**

`docs/README.md` 应列出竞赛资料、项目设计、开发指南、质量报告和历史归档五个入口，并注明 `docs/competition/source/` 可能包含报名信息，不应在公开讨论中复制个人资料。

- [ ] **Step 5: 验证并提交文档迁移**

Run:

```powershell
git diff --check
git add docs
git commit -m "docs: organize project knowledge base"
```

Expected: 无空白错误，所有移动和索引进入提交。

### Task 4: 移除重复旧前端

**Files:**
- Delete: `landing-page/`
- Keep: `source/frontend/`

- [ ] **Step 1: 再次验证重复素材结论**

Run:

```powershell
Get-ChildItem landing-page/assets -File | ForEach-Object {
  $peer = Join-Path 'source/frontend/src/assets' $_.Name
  [PSCustomObject]@{ Name = $_.Name; Same = (Test-Path $peer) -and ((Get-FileHash $_.FullName).Hash -eq (Get-FileHash $peer).Hash) }
}
```

Expected: 15 个旧素材均有同名且哈希相同的正式前端副本。

- [ ] **Step 2: 删除旧入口并验证正式前端**

Run:

```powershell
git rm -r landing-page
Push-Location source/frontend
npm test -- --run
npm run build
Pop-Location
```

Expected: 旧入口完全删除；正式前端测试和构建通过。

- [ ] **Step 3: 提交唯一前端入口**

Run:

```powershell
git commit -m "chore: keep a single frontend application"
```

Expected: 提交只删除已被 `source/frontend` 覆盖的重复目录。

### Task 5: 重写项目入口和协作规范

**Files:**
- Modify: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`

- [ ] **Step 1: 重写根 README**

README 使用中文说明：项目定位、教师端/学生端/生命水墨首页、Vue→FastAPI→MySQL/DeepSeek 架构、目录树、Windows/macOS/Linux 启动方式、演示模式与环境变量、测试/构建命令、文档入口、贡献和安全入口。明确当前仓库未声明开源许可证，不添加错误的 MIT 声明。

- [ ] **Step 2: 新增贡献指南**

`CONTRIBUTING.md` 规定：从最新 `main` 建立功能分支；使用 `feat/`、`fix/`、`docs/`、`chore/` 等前缀；提交遵循 Conventional Commits；前端必须测试和构建，后端必须 pytest；PR 必须说明影响、证据、截图和风险；禁止提交 `.env`、密钥、报名个人信息或生成目录。

- [ ] **Step 3: 新增安全说明**

`SECURITY.md` 规定：漏洞、密钥泄漏和个人信息暴露不得通过公开 Issue 披露；优先通过 GitHub Security Advisory 的私密报告入口联系维护者；报告应包含影响范围、复现步骤、环境和最小证据；维护者确认后再公开修复信息。

- [ ] **Step 4: 验证链接并提交**

Run:

```powershell
Select-String -Path README.md,CONTRIBUTING.md,SECURITY.md -Pattern '待补充|待完成|成员A|成员B|成员C|MIT License|cd -'
git diff --check
git add README.md CONTRIBUTING.md SECURITY.md
git commit -m "docs: refresh project and collaboration guides"
```

Expected: 占位/错误声明搜索无输出，文档提交成功。

### Task 6: 添加 GitHub 模板与双端 CI

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/pull_request_template.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`

- [ ] **Step 1: 创建 CI 工作流**

`.github/workflows/ci.yml` 在 `pull_request` 和 `main` push 时触发。前端 job 使用 Node 20、`npm ci`、`npm test -- --run`、`npm run build`；后端 job 使用 Python 3.11、`pip install -r requirements.txt`、`python -m pytest`。两个 setup action 均启用对应锁文件/requirements 缓存。

- [ ] **Step 2: 创建 PR 模板**

模板必须包含变更概要、关联问题、影响范围复选框、验证命令与结果、界面截图、风险/回滚、提交前检查，不含“待补充”等无意义占位文本。

- [ ] **Step 3: 创建结构化 Issue 表单**

Bug 表单包含问题描述、复现步骤、期望/实际结果、浏览器/系统/提交版本、日志与隐私确认；Feature 表单包含目标用户、用户价值、方案范围、非目标和可验证验收标准；`config.yml` 关闭空白 Issue，并提供私密安全报告链接。

- [ ] **Step 4: 解析 YAML 并提交**

Run:

```powershell
python -c "import pathlib, yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in pathlib.Path('.github').rglob('*.yml')]; print('YAML OK')"
git diff --check
git add .github
git commit -m "ci: add repository quality gates"
```

Expected: 输出 `YAML OK`，模板和 CI 提交成功。

### Task 7: 更新 GitHub 仓库元数据

**Files:**
- External setting: GitHub repository description
- External setting: GitHub repository topics

- [ ] **Step 1: 安全取得当前 GitHub CLI 会话并确认仓库**

使用 Git Credential Manager 临时向当前 PowerShell 进程提供 `GH_TOKEN`，不得打印或保存令牌。

Run:

```powershell
gh repo view xinyuzhang610/- --json nameWithOwner,description,homepageUrl,repositoryTopics
```

Expected: 返回 `xinyuzhang610/-` 当前元数据。

- [ ] **Step 2: 更新批准范围内的简介与 Topics**

Run:

```powershell
gh repo edit xinyuzhang610/- --description '智教通：面向教师与学生的 AI 智能体教学辅助平台，提供需求引导、工具推荐、AI 问答与学习轨迹' --add-topic education --add-topic edtech --add-topic ai --add-topic intelligent-agent --add-topic vue --add-topic fastapi --add-topic chinese
```

Expected: 简介与 7 个 Topics 更新；Homepage、仓库名、许可证、分支保护、Issues/Projects/Wiki 均不改变。

- [ ] **Step 3: 读取回验并清理临时认证环境变量**

Run:

```powershell
gh repo view xinyuzhang610/- --json nameWithOwner,description,homepageUrl,repositoryTopics
Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
```

Expected: 读取值与批准内容一致，Homepage 仍为空。

### Task 8: 全量验证、推送并检查 PR

**Files:**
- Verify: entire repository
- Update: Pull Request #1 branch and description if necessary

- [ ] **Step 1: 运行前端完整验证**

Run:

```powershell
Push-Location source/frontend
npm ci
npm test -- --run
npm run build
Pop-Location
```

Expected: 至少现有 14 个测试文件、71 项测试全部通过，Vite 生产构建退出码为 0。

- [ ] **Step 2: 运行后端完整验证**

Run:

```powershell
Push-Location source/backend
python -m pip install -r requirements.txt
python -m pytest
Pop-Location
```

Expected: 6 项后端测试全部通过。

- [ ] **Step 3: 验证文档、YAML 和仓库卫生**

Run:

```powershell
python -c "import pathlib, re, sys, yaml; root=pathlib.Path('.'); [yaml.safe_load(p.read_text(encoding='utf-8')) for p in root.joinpath('.github').rglob('*.yml')]; bad=[]; pattern=re.compile(r'!?\[[^\]]*\]\((?!https?://|mailto:|#)([^)]+)\)'); [(bad.append((str(p),t)) if not (p.parent/t.split('#')[0]).resolve().exists() else None) for p in root.rglob('*.md') for t in pattern.findall(p.read_text(encoding='utf-8')) if t.split('#')[0]]; print('links OK' if not bad else bad); sys.exit(bool(bad))"
git diff --check
git status -sb
```

Expected: YAML 可解析、内部 Markdown 链接全部存在、无空白错误、工作树只剩被忽略的 `.superpowers/`。

- [ ] **Step 4: 推送当前分支**

Run:

```powershell
git push -u origin codex/eastern-future-ui-design
```

Expected: 普通 push 成功，不使用 `--force`。

- [ ] **Step 5: 检查 PR 合并状态与 Actions**

Run:

```powershell
gh pr view 1 --repo xinyuzhang610/- --json url,state,isDraft,mergeable,mergeStateStatus,changedFiles,additions,deletions,statusCheckRollup
```

Expected: PR #1 URL 保持不变，`mergeable` 不再为 `CONFLICTING`；GitHub 已识别 CI，等待或通过的检查可在 `statusCheckRollup` 中看到。

- [ ] **Step 6: 形成后续治理建议但不执行高风险设置**

最终交付中单独列出仓库改名、许可证选择、远程历史分支清理和 `main` 分支保护建议，明确这些项目本次未执行。
