# Operations Readiness

## Purpose

Make deployment, diagnostics, and verification safe and repeatable.

## Requirements

### Requirement: Honest readiness reporting

The system SHALL expose liveness separately from readiness and readiness SHALL report database and AI configuration availability without exposing secrets.

#### Scenario: Missing database configuration

- **WHEN** the application cannot connect to the configured database
- **THEN** liveness remains available and readiness reports a failed database component

### Requirement: Backup and restore verification

The system SHALL include automated database backup and a restore verification procedure.

#### Scenario: Backup restore rehearsal

- **WHEN** a scheduled backup is restored to a temporary database
- **THEN** the verification reports required table and key-record checks before accepting the backup

### Requirement: Repeatable integration verification

The project SHALL run MySQL migration and API integration tests in CI and SHALL run real DeepSeek smoke tests only when explicitly enabled with a secret.

#### Scenario: CI execution

- **WHEN** a pull request runs CI
- **THEN** unit tests, MySQL integration tests, migrations, frontend checks, and production build execute without requiring a real AI key
