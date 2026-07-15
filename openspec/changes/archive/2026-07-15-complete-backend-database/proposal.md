## Why

智教通当前能够演示基础的教师、学生和 AI 对话流程，但缺少迁移、安全边界、可审计工具生命周期、管理员治理和可验证运维能力，无法满足竞赛交付与真实教学数据保护的要求。现在需要先冻结并完成后端和数据库契约，再以稳定 API 驱动最终业务前端。

## What Changes

- 引入 Alembic 迁移、可回滚升级与现有 MySQL 数据校验。
- 增加账号锁定、验证码、会话失效、改密码和管理员账号治理。
- 将工具的广场上架、公开分享、软删除和外部平台跳转解耦，并修复私有工具越权访问。
- 将推荐改为可解释的规则匹配，支持模板复制、收藏和审计日志。
- 为 AI 问答增加受归属校验的会话上下文、SSE 流式响应和可靠使用记录。
- 提供教师看板、学生学习统计、CSV 导出、管理员 API、备份恢复、健康检查和真实环境验证。
- **BREAKING**：公开工具响应不再返回系统提示词和内部配置；学生必须登录后才能使用 AI、收藏或产生学习轨迹。

## Capabilities

### New Capabilities

- `database-migrations`: 可升级、回滚和校验的 MySQL 数据库迁移与索引体系。
- `account-security`: 账号状态、验证码、会话、密码和角色权限安全边界。
- `tool-lifecycle`: 工具复制、搜索、软删除、广场/分享状态、收藏和外部平台跳转。
- `learning-conversation`: 受认证保护的上下文对话、SSE 流和使用记录。
- `analytics-administration`: 教师数据看板、学生轨迹、CSV 导出、管理员治理和审计。
- `operations-readiness`: 健康检查、备份恢复、日志、CI MySQL 集成和安全依赖治理。

### Modified Capabilities

- None.

## Impact

受影响范围包括 `source/backend` 的模型、迁移、路由、服务、配置、测试和运维脚本；`source/frontend` 的 API 适配、认证与业务页面；GitHub Actions、环境变量示例和竞赛文档。新增 Alembic、SSE、Turnstile 配置、CSV 导出、MySQL 集成测试和本地二维码依赖。
