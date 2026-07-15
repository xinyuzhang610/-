## 1. Migration foundation

- [x] 1.1 Add Alembic configuration, baseline revision, MySQL schema verification and backup helpers
- [x] 1.2 Add lifecycle, session, conversation, audit, and indexed schema revisions
- [x] 1.3 Add migration upgrade/downgrade and legacy-data preservation tests

## 2. Security and administration

- [x] 2.1 Add password validation, captcha configuration, account lockout and active-state persistence
- [x] 2.2 Add JWT session tracking, inactivity expiry, logout and password-change revocation
- [x] 2.3 Add administrator user management and append-only audit logging

## 3. Tool and recommendation lifecycle

- [x] 3.1 Separate public tool DTOs, access checks, paging, search, soft deletion and restoration
- [x] 3.2 Add preset copy, independent plaza/share state, expiry and external-platform redirect context
- [x] 3.3 Replace hard-coded recommendation with prioritized rule matching and administrator rule CRUD
- [x] 3.4 Add student favorite APIs and weekly plaza rankings

## 4. Learning data and analytics

- [x] 4.1 Add owned conversation sessions, bounded history and correct non-stream usage accounting
- [x] 4.2 Add SSE DeepSeek response path with interruption handling
- [x] 4.3 Add student statistics, teacher filtered dashboard, CSV export and administrator audit export

## 5. Operations and client integration

- [x] 5.1 Add readiness, structured logging, safe integration scripts, backups and restore verification
- [x] 5.2 Add MySQL CI coverage and upgrade vulnerable frontend build/test dependencies
- [x] 5.3 Adapt frontend authentication, public preview, favorites, sharing and streaming clients without final visual redesign

## 6. Verification and delivery

- [x] 6.1 Run unit, migration, MySQL integration, frontend, build and API contract tests
- [ ] 6.2 Run real DeepSeek smoke test when local key is supplied and run load/backup verification
- [x] 6.3 Synchronize project documentation, review repository cleanliness, merge, push and launch services
