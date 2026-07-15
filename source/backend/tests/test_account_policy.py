from datetime import datetime, timedelta

import pytest

from models.user import User
from services.user_service import is_user_locked, register_failed_login, validate_password_strength


def test_password_must_have_eight_characters_letters_and_digits():
    with pytest.raises(ValueError):
        validate_password_strength("short1")
    with pytest.raises(ValueError):
        validate_password_strength("onlyletters")
    with pytest.raises(ValueError):
        validate_password_strength("12345678")

    validate_password_strength("Teacher2026")


def test_fifth_failed_login_locks_account_for_fifteen_minutes():
    user = User(username="locked", password_hash="hash", role="student")
    for _ in range(5):
        register_failed_login(user)

    assert user.failed_login_attempts == 5
    assert is_user_locked(user)
    assert user.locked_until >= datetime.utcnow() + timedelta(minutes=14)
