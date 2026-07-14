from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate
from utils.security import generate_token


def test_role_guard_rejects_student_for_teacher_operation():
    from api.dependencies import require_roles

    student = User(id=1, username="student", password_hash="hash", role="student")
    guard = require_roles("teacher")

    try:
        guard(student)
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("student must not pass a teacher role guard")


def test_public_registration_cannot_create_an_admin_account():
    from api.user import register

    request = UserCreate(username="not-an-admin", password="safe-password", role="admin")
    try:
        register(request, db=None)
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("the public registration route must reject the admin role")


def test_teacher_cannot_read_another_teachers_tool_usage():
    from api.usage import get_tool_usage

    class Query:
        def filter(self, *args):
            return self

        def first(self):
            return type("ToolOwner", (), {"creator_id": 99})()

    class Database:
        def query(self, *args):
            return Query()

    try:
        get_tool_usage(12, db=Database(), current_user=User(id=1, username="other", password_hash="hash", role="teacher"))
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("a teacher must not read another teacher's tool usage")
