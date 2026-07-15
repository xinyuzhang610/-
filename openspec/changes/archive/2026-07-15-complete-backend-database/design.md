## Context

现有 FastAPI 服务使用 SQLAlchemy `create_all`、7 天 JWT、单一 `is_public` 状态和硬编码推荐。当前数据库未配置可复现连接，公开详情会泄露内部提示词，聊天没有上下文或可恢复流。项目需要在保留预设工具和历史数据的前提下完成竞赛级后端。

## Goals / Non-Goals

**Goals:**

- 在 MySQL 和测试数据库上以 Alembic 管理可回滚的 schema 演进。
- 建立服务器端会话、安全认证、工具可见性、审计、统计和管理员治理。
- 为后续 Vue 业务页提供固定、分页、可测试的 API 契约。
- 将师大智能体平台限制为带白名单上下文的新窗口跳转。

**Non-Goals:**

- 不在本应用创建师大智能体工作流或交换平台账号数据。
- 不让 DeepSeek 生成工具/工作流；其职责仅为学习文本问答。
- 不在后端稳定前重做业务页的最终视觉样式。

## Decisions

- **迁移：**使用 Alembic baseline 加增量迁移。现有数据库先备份并验证表指纹后 stamp baseline；新库从 revision 0 升级。相比 `create_all`，它保留已有数据并支持回滚。
- **会话：**JWT 含 `jti` 和用户 token version，`auth_sessions` 保存最后活动、过期和撤销状态。每个受保护请求校验 30 分钟 idle timeout；改密码、禁用账号和退出会撤销会话。纯 30 分钟无状态 JWT 无法可靠实现无操作超时，因此不采用。
- **工具状态：**`plaza_status`、`share_enabled/share_expires_at` 与 `deleted_at` 独立。公开 DTO 永不返回提示词、内部界面配置或所有者私密数据。相比复用 `is_public`，可满足下架不影响有效分享。
- **推荐：**规则按精确学科、分类、通用三个层级匹配，同层按 priority 降序；无命中返回可解释兜底。规则及工具选择均由管理员维护，不使用 AI。
- **对话：**保存会话与消息，普通接口保持兼容；流接口采用 SSE `meta/delta/done/error`。只有完整成功响应增加成功使用次数；中断写 aborted 记录。
- **审计：**所有写操作和平台跳转通过统一服务追加 audit log；生产应用账号不具备删除审计记录权限。数据库触发器作为 MySQL 附加保护，SQLite 测试以服务层保证行为。
- **运维：**分离 liveness 和 readiness；备份脚本通过受限账号读取，恢复验证到临时库；真实 DeepSeek 测试仅在显式环境变量存在时运行。

## Risks / Trade-offs

- [现有 MySQL schema 与 ORM 有差异] → 迁移前运行 schema/data 检查并自动生成备份；不匹配时拒绝升级。
- [Turnstile 本地不可用] → 仅在 DEBUG 和显式 bypass 配置下允许测试 token，生产缺 token 一律拒绝。
- [SSE 客户端断开难检测] → 捕获取消异常，写 aborted 状态并不计成功使用。
- [统计表增长] → 为时间、工具、用户建立复合索引，并在 10 万日志数据上测量聚合。
- [平台地址被滥用] → 仅使用服务端配置和工具白名单 URL，不接受任意跳转地址。

## Migration Plan

1. 备份现有数据库并记录 users/tools/usage_logs/recommend_rules 的行数。
2. 将确认的旧 schema stamp 为 baseline，再 upgrade 到新 revision。
3. 运行迁移校验、预设工具校验和 API smoke test。
4. 失败时 downgrade 到 baseline 并从备份恢复；不删除审计或使用记录。

## Open Questions

无。学生公开注册、登录后互动、DeepSeek 文本问答边界、公开预览与外部平台跳转已由产品决策确定。
