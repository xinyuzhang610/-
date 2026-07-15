## ADDED Requirements

### Requirement: Teacher analytics
The system SHALL provide teachers 7/30-day, tool-filtered analytics with distinct student counts, trends, rankings, recent records, percentages, and CSV export.

#### Scenario: Filtered thirty-day dashboard
- **WHEN** a teacher selects 30 days and one owned tool
- **THEN** all returned metrics and export rows are limited to that tool and range

### Requirement: Student learning statistics
The system SHALL provide total interactions, distinct tools, consecutive active days, and recent records to the authenticated student.

#### Scenario: Consecutive-day calculation
- **WHEN** a student has activity today and on adjacent previous calendar days
- **THEN** the response returns the correct uninterrupted-day count

### Requirement: Administrator governance and audit
The system SHALL let administrators manage users, plaza status, recommendation rules, and append-only audit logs.

#### Scenario: Administrator changes a role
- **WHEN** an administrator changes a user's role or account status
- **THEN** the change takes effect and an audit record identifies actor, time, target, and action
