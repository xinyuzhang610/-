# Repository Consolidation Design

## Goal

Consolidate the repository around one authoritative `main` branch and one production application tree. Preserve genuinely useful historical material in a clearly marked archive without allowing legacy pages, duplicate components, or obsolete branches to compete with the current implementation.

## Target repository structure

```text
.
├── .github/                  # CI and collaboration templates
├── docs/
│   ├── archive/
│   │   ├── legacy-frontend/ # Historical UI snapshots, excluded from builds
│   │   ├── plans/           # Superseded implementation plans
│   │   └── reports/         # Historical environment reports
│   ├── competition/         # Required competition source and project documents
│   ├── design/              # Current design decisions
│   ├── guides/              # Current setup and development guides
│   └── quality/             # QA evidence and screenshots
├── source/
│   ├── backend/             # The only backend application
│   └── frontend/            # The only frontend application
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
└── SECURITY.md
```

`source/` contains only code that participates in the current application. Historical code may be consulted under `docs/archive/`, but it is not imported, routed, tested, or built.

## Frontend consolidation

The current router is the source of truth. The following unreferenced duplicates will leave `source/frontend/src`:

- `layouts/StudentLayout.vue` and `layouts/TeacherLayout.vue`, superseded by `layout/index.vue`.
- `views/auth/Login.vue` and `views/auth/Register.vue`, superseded by `views/Login.vue` and `views/Register.vue`.
- `views/student/AIChat.vue`, superseded by `views/student/Chat.vue`.
- `views/teacher/MyTools.vue`, superseded by `views/teacher/Tools.vue`.
- The unused duplicate user store after imports are verified against the active Pinia store.

One representative copy of the earliest static landing page will be restored from Git history to `docs/archive/legacy-frontend/static-landing/`. Unused Vue-era files that contain distinct work will be placed under `docs/archive/legacy-frontend/vue-unused/`; byte-identical duplicates will not be retained twice. An archive README will identify the active frontend and explain that archived pages are non-runnable references.

## Branch consolidation

The final remote branch set is only `main`.

- `codex/eastern-future-ui-design`, `docs/比赛文档`, `feature/frontend`, and `前端更改` are already ancestors of `main`; their work is already merged.
- `feature/backend` contains one unique commit whose sole effect is deleting frontend and documentation files. It adds no backend implementation, so merging it would damage the repository. Its valid backend state is already represented in `main`; the destructive deletion commit will be documented and the branch removed.
- The consolidation work will be merged into `main` only after tests and repository-hygiene checks pass.
- After the merged `main` is confirmed on GitHub, all five obsolete remote branches and their matching local branches will be deleted. No force push or history rewrite is required.

## Local legacy checkout

`D:/Download/mimo-code-clone` currently contains an unborn `master` checkout with an untracked static landing page and a byte-duplicate `backup/` directory. Before removing either copy, hashes will be compared with the archived static snapshot. Once equality is proven and the archive is committed on `main`, the duplicate local files can be removed and this checkout can be attached to `main` without data loss.

## Documentation and navigation

- Update the root README and `docs/README.md` so contributors can identify the active application in one glance.
- Add an archive index describing what was retained, why it is historical, and where its active replacement lives.
- Remove stale references to deleted branches, duplicate landing-page roots, and superseded source paths.
- Keep all competition notices, registration forms, and required project documents under `docs/competition/` unchanged unless a path link needs updating.

## Verification

The consolidation is accepted only when all of the following are true:

1. Frontend unit tests pass and the Vite production build succeeds.
2. Backend tests pass under Python 3.11.
3. A repository-hygiene check confirms there is one active frontend root and no legacy component is imported by production code.
4. Markdown links and CI YAML parse successfully.
5. `git status` is clean after the final merge.
6. `origin/main` contains the consolidation commit and `git ls-remote --heads origin` lists only `refs/heads/main`.

## Safety constraints

- Do not rewrite Git history or force push.
- Do not delete competition source documents.
- Do not merge the destructive `feature/backend` deletion commit.
- Do not delete a local duplicate until its content is verified against the committed archive.
- Do not claim completion until the remote branch list and both application test suites are freshly verified.
