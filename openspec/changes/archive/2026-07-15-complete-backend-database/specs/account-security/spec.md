## ADDED Requirements

### Requirement: Protected login
The system SHALL require a valid captcha in production, lock an account for 15 minutes after five consecutive failed passwords, and reject disabled accounts.

#### Scenario: Fifth failed password
- **WHEN** an enabled account submits five invalid passwords
- **THEN** the account is locked and subsequent login attempts are rejected until the lock expires

### Requirement: Session invalidation
The system SHALL expire inactive sessions after 30 minutes and revoke existing sessions after password change or account disablement.

#### Scenario: Password changed
- **WHEN** a user successfully changes a password
- **THEN** every previous token for that user is rejected

### Requirement: Role and ownership enforcement
The system SHALL enforce teacher, student, and administrator roles server-side for every protected operation.

#### Scenario: Student accesses teacher resource
- **WHEN** a student requests a teacher-only endpoint
- **THEN** the endpoint returns 403 without exposing teacher data
