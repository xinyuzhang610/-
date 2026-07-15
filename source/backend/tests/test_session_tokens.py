from utils.security import generate_token, verify_token


def test_session_token_carries_jti_and_token_version():
    token = generate_token(7, "student", "test-secret", jti="session-123", token_version=3, expires_minutes=30)

    payload = verify_token(token, "test-secret")

    assert payload["user_id"] == 7
    assert payload["jti"] == "session-123"
    assert payload["token_version"] == 3
