# 参与智教通开发

感谢参与智教通。提交代码前，请先确认改动范围明确、没有泄露密钥或竞赛报名个人信息，并完成与改动相关的验证。

## 开发流程

1. 从最新 `main` 创建短生命周期分支。
2. 在本地完成实现和测试，不直接向 `main` 提交。
3. 推送分支并创建 Pull Request，说明变更、验证证据、界面截图和已知风险。
4. 根据评审意见更新同一分支；不要通过 force push 擅自重写协作者已经评审的历史。

推荐的分支前缀：

- `feat/`：新功能或体验。
- `fix/`：缺陷修复。
- `docs/`：文档与说明。
- `test/`：测试改进。
- `chore/`：依赖、CI 或仓库维护。

## 提交信息

提交使用 Conventional Commits，主题保持简短并描述单一意图，例如：

```text
feat: add student learning records
fix: prevent stale ink reveal trails
docs: clarify backend setup
ci: verify frontend and backend
```

不要提交无意义的“update”“修改一下”或把互不相关的改动打包在同一个提交中。

## 必须通过的检查

前端改动：

```bash
cd source/frontend
npm ci
npm test -- --run
npm run build
```

后端改动（Python 3.11）：

```bash
cd source/backend
python -m pip install -r requirements.txt
python -m pytest
```

文档或仓库结构改动还应确认所有相对链接存在，并运行 `git diff --check`。

## Pull Request 要求

PR 应当：

- 说明用户或开发者能观察到的变化及变更原因。
- 标出教师端、学生端、后端、文档或基础设施等影响范围。
- 列出实际运行过的命令和结果，不使用“应该通过”代替证据。
- 界面变化提供桌面端和移动端截图；交互变化说明键盘与减少动态偏好表现。
- 说明数据库、环境变量、兼容性、安全和回滚风险。
- 保持聚焦，避免顺手重构与需求无关的代码。

## 数据与密钥

禁止提交：

- `.env`、API Key、Token、数据库密码和生产连接串。
- `node_modules/`、`dist/`、覆盖率、缓存和编辑器临时文件。
- 未脱敏的报名表内容、联系方式、账号或真实学习记录。

如发现密钥或个人信息已进入提交，请立即停止传播并按 [SECURITY.md](SECURITY.md) 私下报告。

## 设计边界

- DeepSeek 只承担文本问答，不在本应用内创建智能体工作流。
- 教学需求推荐使用可解释的条件匹配，不以生成式 AI 替代规则。
- `source/frontend` 是唯一正式前端入口。
- 不要创建第二套前端根目录，也不要从 `docs/archive/` 导入代码；归档内容只用于历史追溯。
- 功能完成后同步更新对应文档和测试。
