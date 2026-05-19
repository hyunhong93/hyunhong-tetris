REGISTER_URL = "/register"
LOGIN_URL    = "/login"
SCORES_URL   = "/scores"
TOP_URL      = "/scores/top"
ME_URL       = "/scores/me"

USER_A = {"email": "a@example.com", "nickname": "유저A", "password": "pass1234"}
USER_B = {"email": "b@example.com", "nickname": "유저B", "password": "pass5678"}


def _token(client, user):
    client.post(REGISTER_URL, json=user)
    res = client.post(LOGIN_URL, json={"email": user["email"], "password": user["password"]})
    return res.json()["access_token"]


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_save_score_success(client):
    token = _token(client, USER_A)
    res = client.post(SCORES_URL, json={"score": 1000, "level": 3, "lines": 15}, headers=_auth(token))
    assert res.status_code == 201


def test_save_score_unauthorized(client):
    res = client.post(SCORES_URL, json={"score": 1000, "level": 3, "lines": 15})
    assert res.status_code == 401


def test_save_score_invalid_token(client):
    res = client.post(SCORES_URL, json={"score": 500, "level": 1, "lines": 5}, headers=_auth("invalid.token.here"))
    assert res.status_code == 401


def test_get_top_score_empty(client):
    res = client.get(TOP_URL)
    assert res.status_code == 200
    assert res.json() == {"nickname": "-", "score": 0}


def test_get_top_score_single(client):
    token = _token(client, USER_A)
    client.post(SCORES_URL, json={"score": 800, "level": 2, "lines": 10}, headers=_auth(token))
    res = client.get(TOP_URL)
    assert res.status_code == 200
    assert res.json()["score"] == 800
    assert res.json()["nickname"] == USER_A["nickname"]


def test_get_top_score_returns_highest(client):
    token = _token(client, USER_A)
    client.post(SCORES_URL, json={"score": 500,  "level": 1, "lines": 5},  headers=_auth(token))
    client.post(SCORES_URL, json={"score": 2000, "level": 6, "lines": 40}, headers=_auth(token))
    res = client.get(TOP_URL)
    assert res.json()["score"] == 2000


def test_get_top_score_across_users(client):
    token_a = _token(client, USER_A)
    token_b = _token(client, USER_B)
    client.post(SCORES_URL, json={"score": 1000, "level": 3, "lines": 15}, headers=_auth(token_a))
    client.post(SCORES_URL, json={"score": 3000, "level": 8, "lines": 60}, headers=_auth(token_b))
    res = client.get(TOP_URL)
    assert res.json()["score"] == 3000
    assert res.json()["nickname"] == USER_B["nickname"]


def test_get_my_scores_success(client):
    token = _token(client, USER_A)
    client.post(SCORES_URL, json={"score": 100, "level": 1, "lines": 1}, headers=_auth(token))
    client.post(SCORES_URL, json={"score": 200, "level": 2, "lines": 5}, headers=_auth(token))
    res = client.get(ME_URL, headers=_auth(token))
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_my_scores_only_own(client):
    token_a = _token(client, USER_A)
    token_b = _token(client, USER_B)
    client.post(SCORES_URL, json={"score": 999, "level": 2, "lines": 8}, headers=_auth(token_a))
    res = client.get(ME_URL, headers=_auth(token_b))
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_get_my_scores_unauthorized(client):
    res = client.get(ME_URL)
    assert res.status_code == 401
