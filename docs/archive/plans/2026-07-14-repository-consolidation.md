# Repository Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce one clear production tree on `main`, retain one indexed historical frontend archive, and remove all obsolete remote branches without losing unique project material.

**Architecture:** Treat the active router and `source/frontend` build as the production boundary. Move distinct but unused UI files outside that boundary, restore the earliest static page once from Git history, and enforce the boundary with a repository-hygiene pytest. Merge through a normal fast-forward or merge commit, then delete branches only after remote `main` and tests are verified.

**Tech Stack:** Git, GitHub, Vue 3/Vite/Vitest, Python 3.11/pytest, Markdown, PowerShell.

---

### Task 1: Add a failing repository-hygiene test

**Files:**
- Create: `source/backend/tests/test_repository_hygiene.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
LEGACY_ACTIVE_PATHS = (
    "source/frontend/src/layouts/StudentLayout.vue",
    "source/frontend/src/layouts/TeacherLayout.vue",
    "source/frontend/src/stores/user.js",
    "source/frontend/src/views/auth/Login.vue",
    "source/frontend/src/views/auth/Register.vue",
    "source/frontend/src/views/student/AIChat.vue",
    "source/frontend/src/views/teacher/MyTools.vue",
)


def test_only_one_frontend_application_is_active():
    package_files = {
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for path in REPOSITORY_ROOT.rglob("package.json")
        if "node_modules" not in path.parts and "archive" not in path.parts
    }
    assert package_files == {"source/frontend/package.json"}


def test_legacy_frontend_files_are_outside_the_active_source_tree():
    assert not [
        path
        for path in LEGACY_ACTIVE_PATHS
        if (REPOSITORY_ROOT / path).exists()
    ]


def test_legacy_frontend_archive_is_indexed():
    archive = REPOSITORY_ROOT / "docs/archive/legacy-frontend"
    assert (archive / "README.md").is_file()
    assert (archive / "static-landing/index.html").is_file()
```

- [ ] **Step 2: Run the test to verify it fails for the existing duplicate files**

Run: `py -3.11 -m pytest tests/test_repository_hygiene.py -q` from `source/backend`.

Expected: two failures because the legacy paths remain under `source/frontend/src` and the indexed archive does not exist.

- [ ] **Step 3: Commit the failing test**

```powershell
git add source/backend/tests/test_repository_hygiene.py
git commit -m "test: define active repository boundaries"
```

### Task 2: Consolidate historical frontend files

**Files:**
- Create: `docs/archive/legacy-frontend/README.md`
- Restore and move: historical `landing-page/` to `docs/archive/legacy-frontend/static-landing/`
- Move: `source/frontend/src/layouts/*.vue` to `docs/archive/legacy-frontend/vue-unused/layouts/`
- Move: `source/frontend/src/stores/user.js` to `docs/archive/legacy-frontend/vue-unused/stores/user.js`
- Move: `source/frontend/src/views/auth/*.vue` to `docs/archive/legacy-frontend/vue-unused/views/auth/`
- Move: `source/frontend/src/views/student/AIChat.vue` to `docs/archive/legacy-frontend/vue-unused/views/student/AIChat.vue`
- Move: `source/frontend/src/views/teacher/MyTools.vue` to `docs/archive/legacy-frontend/vue-unused/views/teacher/MyTools.vue`

- [ ] **Step 1: Restore the earliest static page from the merged historical commit**

```powershell
git restore --source=a517378 -- landing-page
New-Item -ItemType Directory -Force docs/archive/legacy-frontend | Out-Null
git mv landing-page docs/archive/legacy-frontend/static-landing
```

- [ ] **Step 2: Move distinct unreferenced Vue files out of production source**

Use `git mv` for each listed path so Git preserves file ancestry. Create destination directories before each move. Do not move `source/frontend/src/store/user.js`, `layout/index.vue`, `views/Login.vue`, `views/Register.vue`, `views/student/Chat.vue`, or `views/teacher/Tools.vue`; those are active replacements.

- [ ] **Step 3: Add the archive index**

The README must state:

```markdown
# 历史前端归档

这里保存已经退出正式构建的早期页面，仅用于设计追溯。

- `static-landing/`：最早的纯 HTML 展示页。
- `vue-unused/`：已被当前路由、布局或状态管理替代的 Vue 文件。
- 当前唯一正式前端：[`source/frontend`](../../../source/frontend/)。

归档代码不参与安装、路由、测试或生产构建。请勿直接在这里继续开发功能。
```

- [ ] **Step 4: Run the hygiene test to verify it passes**

Run: `py -3.11 -m pytest tests/test_repository_hygiene.py -q` from `source/backend`.

Expected: `3 passed`.

- [ ] **Step 5: Commit the archive consolidation**

```powershell
git add docs/archive/legacy-frontend source/frontend/src
git commit -m "refactor: archive superseded frontend files"
```

### Task 3: Clarify repository navigation

**Files:**
- Modify: `README.md`
- Modify: `docs/README.md`
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Update the root tree and active-source statement**

Add `docs/archive/legacy-frontend` to the displayed repository tree and state directly below it that only `source/frontend` and `source/backend` are production code. Historical pages are reference-only.

- [ ] **Step 2: Link the archive from the documentation center**

Change the archive navigation entry to link explicitly to `archive/legacy-frontend/` for historical UI and to `archive/plans/` for implementation plans.

- [ ] **Step 3: Add the archive boundary to contributing guidance**

State that contributors must not import from `docs/archive` and must not create a second frontend root.

- [ ] **Step 4: Verify Markdown relative links**

Run a Python standard-library link checker over tracked `*.md` files, ignoring external URLs and in-document anchors.

Expected: exit code `0` and no missing relative targets.

- [ ] **Step 5: Commit navigation updates**

```powershell
git add README.md docs/README.md CONTRIBUTING.md
git commit -m "docs: clarify active and archived project paths"
```

### Task 4: Run complete local verification

**Files:**
- No source changes expected.

- [ ] **Step 1: Run frontend tests**

Run: `npm test -- --run` from `source/frontend`.

Expected: 14 test files and 71 tests pass.

- [ ] **Step 2: Build the frontend**

Run: `npm run build` from `source/frontend`.

Expected: Vite exits with code `0` and produces `dist/`.

- [ ] **Step 3: Run the complete backend test suite**

Run: `py -3.11 -m pytest -q` from `source/backend`.

Expected: 9 tests pass, including the three repository-hygiene tests.

- [ ] **Step 4: Run repository checks**

Run `git diff origin/main...HEAD --check`, parse `.github/workflows/ci.yml` with Python and PyYAML, validate Markdown links, and verify `git status --short` contains no unexpected files.

- [ ] **Step 5: Review the branch diff**

Confirm that competition source files are unchanged, active router targets remain present, no second active `package.json` exists, and the only source removals are the seven approved legacy paths.

### Task 5: Publish and merge the consolidation

**Files:**
- Git refs only.

- [ ] **Step 1: Synchronize with the latest remote main**

```powershell
git fetch origin
git merge origin/main
```

Expected: already up to date or a normal conflict-free merge. Do not rebase or force push.

- [ ] **Step 2: Re-run frontend and backend tests after synchronization**

Run the commands from Task 4 again. Do not push if either suite fails.

- [ ] **Step 3: Push the consolidation branch**

```powershell
git push -u origin codex/repository-consolidation
```

- [ ] **Step 4: Create and merge a pull request**

Create a ready PR targeting `main`, wait for required checks, and merge it with a normal merge commit. If GitHub CLI authentication is unavailable, use the existing Git credential for push and the GitHub HTTPS/API surface available in the environment; do not bypass failed checks.

- [ ] **Step 5: Verify remote main contains the merge**

```powershell
git fetch origin
git merge-base --is-ancestor codex/repository-consolidation origin/main
```

Expected: exit code `0`.

### Task 6: Delete obsolete branches and normalize the local checkout

**Files:**
- Git refs and the duplicate untracked checkout at `D:/Download/mimo-code-clone`.

- [ ] **Step 1: Delete obsolete remote branches**

Only after Task 5 succeeds, delete:

```text
codex/eastern-future-ui-design
docs/比赛文档
feature/backend
feature/frontend
前端更改
codex/repository-consolidation
```

Use normal `git push origin --delete ...`; never use force push against `main`.

- [ ] **Step 2: Verify the final remote branch list**

Run: `git ls-remote --heads origin`.

Expected: exactly one line ending in `refs/heads/main`.

- [ ] **Step 3: Verify the untracked static checkout matches the committed archive**

Use `git hash-object` for `index.html`, `README.md`, `素材清单.md`, and every asset in `D:/Download/mimo-code-clone/assets`; compare them with the committed `docs/archive/legacy-frontend/static-landing` blobs. Confirm the local `backup/` copy is byte-identical.

- [ ] **Step 4: Remove verified duplicate working-tree files and attach the checkout to main**

After the hash comparison is exact, remove only the verified untracked legacy files from `D:/Download/mimo-code-clone`, fetch `origin/main`, and switch that checkout to a local `main` tracking branch. Preserve the linked application worktree until no process depends on it.

- [ ] **Step 5: Final verification**

Confirm the normalized checkout is clean on `main`, the frontend page still returns HTTP 200 if the dev server is running, and `git branch -a` contains no obsolete branches other than unavoidable stale local refs that are reported explicitly.
