# 后端与数据库运行手册

## 本地启动

1. 复制 `source/backend/.env.example` 为 `.env`，填入受限应用账号、随机 `SECRET_KEY` 和（可选）DeepSeek Key。
2. 在 `source/backend` 执行 `python -m alembic -c alembic.ini upgrade head`。
3. 执行 `python -m uvicorn main:app --host 127.0.0.1 --port 8000`。

`/api/health` 是存活检查；`/api/readiness` 会报告数据库和 AI 配置状态，且不会泄露密钥。

## 旧库升级

升级前先导出备份并记录 `users`、`tools`、`usage_logs`、`recommend_rules` 行数。若旧库已有原始表而未有 Alembic 版本记录，先核对 baseline 结构，再执行：

```powershell
python -m alembic -c alembic.ini stamp 20260715_01
python -m alembic -c alembic.ini upgrade head
```

新库直接执行 `upgrade head`。生产环境不得用 `init_db.py` 或 `Base.metadata.create_all()` 做升级。

## 备份和恢复验证

用单独的只读备份账号（不使用应用账号或 root）执行：

```powershell
.\scripts\backup_mysql.ps1 -DatabaseUrl $env:BACKUP_DATABASE_URL -BackupDirectory .\backups
.\scripts\verify_backup.ps1 -BackupFile .\backups\<file>.sql -DatabaseUrl $env:BACKUP_DATABASE_URL
```

每次备份应恢复到临时数据库，确认 `users`、`tools`、`usage_logs`、`recommend_rules`、`audit_logs` 都存在，并核对关键记录数后再删除临时库。

## 安全边界

- 学生可以注册；发送 AI、收藏和产生学习轨迹必须登录。
- 广场和分享预览仅返回公开展示字段；提示词和界面配置不公开。
- DeepSeek 仅用于文本问答；师大平台只接收白名单跳转上下文。
- 生产开启 Turnstile、HTTPS、`DEBUG=false`，并把 `.env` 和备份排除在 Git 外。
