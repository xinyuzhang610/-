# Database Migrations

## Purpose

Manage safe, versioned database evolution and query performance.

## Requirements

### Requirement: Versioned schema migration

The system SHALL manage production database schema changes through Alembic revisions and SHALL not use application startup `create_all` for production upgrades.

#### Scenario: Upgrade an existing installation

- **WHEN** a verified legacy database is upgraded
- **THEN** the database is stamped at the baseline and upgraded without deleting existing preset tools or usage records

### Requirement: Migration rollback verification

The system SHALL provide a repeatable upgrade, downgrade, and re-upgrade verification path.

#### Scenario: Failed migration rehearsal

- **WHEN** an upgrade rehearsal fails validation
- **THEN** the deployment procedure restores the previous schema and preserves the backup

### Requirement: Query indexes

The system SHALL index tool ownership and lifecycle state, share lookup, usage time filtering, session ownership, favorites, and audit filters.

#### Scenario: Filtered list query

- **WHEN** a paginated tool, usage, or audit list is queried
- **THEN** it uses indexed ownership and time/state fields without a full unbounded application-side scan
