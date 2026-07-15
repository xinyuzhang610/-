# Database operations

The production application account must not be MySQL root and must not have permissions to modify or delete `audit_logs`.

Create an encrypted/scheduled task which calls `backup_mysql.ps1` with the `DATABASE_URL` from a secure environment source. Run `verify_backup.ps1` immediately afterwards and restore every backup into an isolated temporary MySQL database before accepting it. Neither script prints a password.

Alembic is the only production schema upgrade mechanism. Do not use `init_db.py` or `Base.metadata.create_all()` to upgrade production data.
