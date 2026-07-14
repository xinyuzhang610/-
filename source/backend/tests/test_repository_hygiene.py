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
