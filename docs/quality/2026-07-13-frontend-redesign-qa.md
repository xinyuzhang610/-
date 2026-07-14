# 智教通「东方未来主义」前端重设计 QA 报告

日期：2026-07-14
验收地址：`http://127.0.0.1:5173`
验收模式：`VITE_DEMO_MODE=true`（页面持续显示“演示数据”标记）

## 自动化验证

- `npm test -- --run`：通过，10 个测试文件、49 项测试。
- `npm run build`：通过。
- `git diff --check`：通过。
- 最大 JavaScript chunk：Element Plus 约 797 KB，低于优化前约 1.04 MB；Vue、网络层与其他依赖已拆分。

## 浏览器检查

使用真实 Chromium、1440×900 与 390×844 两种视口检查：

- `/`：首屏、生成式水墨素材、知识核心、六段叙事、教师/学生入口、跳过动态。
- `/login?role=teacher`、`/register`：身份切换、可见标签、教师登录和学生免注册入口。
- `/teacher/home`、`/teacher/tools`、`/teacher/dashboard`：三步需求引导、演示工具、指标、七日趋势、排行榜、最近记录。
- `/student/guidance`：恰好三层选择、按钮选择态、实时进度、层级解锁。
- `/student/plaza`：分类、搜索、响应式卡片和工具路由。
- `/student/chat`：双栏/单栏切换；后端未启动时错误明确，输入“请解释勾股定理”仍保留，重试按钮可用。
- `/student/records`：指标与时间线。
- `/tool/1`：演示模式按路由 ID 读取工具；正常模式仍读取真实 `/api/tools/{id}`。

浏览器检查未发现页面脚本异常或横向溢出。首次 QA 发现旧 Vite 进程未带演示标记，以及演示工具详情仍请求后端；已重启为显式演示模式并修复工具详情的演示数据解析。

## 截图证据

- `screenshots/home-desktop.png`
- `screenshots/home-mobile.png`
- `screenshots/home-section.png`
- `screenshots/teacher-dashboard-desktop.png`
- `screenshots/teacher-dashboard-mobile.png`
- `screenshots/student-guidance-desktop.png`
- `screenshots/student-guidance-mobile.png`
- `screenshots/student-chat-desktop.png`
- `screenshots/student-chat-mobile.png`

## 后端限制

本轮目标是前端重设计。当前验收环境未启动 FastAPI 与 DeepSeek 服务，因此聊天提交会呈现真实错误态，不伪造 AI 回答。关闭 `VITE_DEMO_MODE` 后，广场、工具、推荐、统计、记录和聊天全部使用真实 API；API 失败不会静默替换为演示数据。
