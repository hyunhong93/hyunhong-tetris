REGISTER_URL = "/register"
LOGIN_URL = "/login"

USER = {"email": "test@example.com", "nickname": "테스터", "password": "pass1234"}


def test_register_success(client):
    res = client.post(REGISTER_URL, json=USER)
    assert res.status_code == 201


def test_register_duplicate_email(client):
    client.post(REGISTER_URL, json=USER)
    res = client.post(REGISTER_URL, json={**USER, "nickname": "다른닉네임"})
    assert res.status_code == 400
    assert "이메일" in res.json()["detail"]


def test_login_success(client):
    client.post(REGISTER_URL, json=USER)
    res = client.post(LOGIN_URL, json={"email": USER["email"], "password": USER["password"]})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["nickname"] == USER["nickname"]


def test_login_wrong_password(client):
    client.post(REGISTER_URL, json=USER)
    res = client.post(LOGIN_URL, json={"email": USER["email"], "password": "wrong"})
    assert res.status_code == 401


def test_login_nonexistent_email(client):
    res = client.post(LOGIN_URL, json={"email": "nobody@example.com", "password": "1234"})
    assert res.status_code == 401
