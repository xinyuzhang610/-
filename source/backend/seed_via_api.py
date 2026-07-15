"""Deprecated: intentionally does not modify any database.

Use Alembic migrations and environment-specific, reviewed seed fixtures instead.
The former script embedded database credentials and deleted user data.
"""
raise SystemExit("This legacy script was retired for safety. It cannot delete or seed any database.")
