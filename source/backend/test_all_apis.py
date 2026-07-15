"""Deprecated manual API test entry point.

Run `python -m pytest` for isolated API tests. Integration runs must use a
disposable database configured through DATABASE_URL; this script intentionally
performs no requests and no data mutations.
"""
raise SystemExit("Use pytest and the CI MySQL migration job instead of this legacy script.")
