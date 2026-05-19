# 테트리스 백엔드 연동 계획

## 개요

기존 순수 HTML/CSS/JS 테트리스에 FastAPI 백엔드를 붙인다.  
이메일 기반 회원가입/로그인, 플레이 기록 저장, 전체 사용자 최고점수 표시가 목표다.

---

## 배포 정보

- 프론트엔드(GitHub Pages): https://hyunhong93.github.io/hyunhong-tetris/landing.html
- 백엔드(FastAPI): 로컬 개발 기준 `http://localhost:8000`

---

## 추가될 파일 구조

```
tetris/
├── landing.html       # 기존 — 로그인/회원가입 UI 추가
├── landing.css        # 기존 — 로그인 폼 스타일 추가
├── landing.js         # 기존
├── index.html         # 기존 — 최고점수 패널 추가
├── game.css           # 기존
├── game.js            # 기존 — 게임 종료 시 점수 POST 추가
│
└── backend/
    ├── main.py        # FastAPI 앱 진입점
    ├── database.py    # SQLite 연결 (SQLAlchemy)
    ├── models.py      # ORM 모델 (User, GameRecord)
    ├── schemas.py     # Pydantic 스키마
    ├── auth.py        # JWT 발급/검증, 비밀번호 해싱
    ├── routers/
    │   ├── auth.py    # POST /register, POST /login
    │   └── scores.py  # POST /scores, GET /scores/top
    └── tetris.db      # SQLite 파일 (자동 생성)
```

---

## DB 스키마

### users
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동 증가 |
| email | TEXT UNIQUE | 로그인 ID |
| hashed_password | TEXT | bcrypt 해시 |
| nickname | TEXT | 화면 표시 이름 |
| created_at | DATETIME | 가입일시 |

### game_records
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동 증가 |
| user_id | INTEGER FK | users.id 참조 |
| score | INTEGER | 최종 점수 |
| level | INTEGER | 최종 레벨 |
| lines | INTEGER | 제거한 줄 수 |
| played_at | DATETIME | 플레이 종료 시각 |

---

## API 엔드포인트

### 인증
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/register` | 이메일·닉네임·비밀번호로 회원가입 |
| POST | `/login` | 이메일·비밀번호로 로그인 → JWT 반환 |

### 점수
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/scores` | 게임 종료 시 점수 저장 (JWT 필요) |
| GET | `/scores/top` | 전체 사용자 최고점수 1위 조회 |
| GET | `/scores/me` | 내 플레이 기록 조회 (JWT 필요) |

---

## 프론트엔드 변경 사항

### landing.html
- 로그인 폼 (이메일 + 비밀번호) 추가
- 회원가입 폼 (이메일 + 닉네임 + 비밀번호) 추가
- 로그인 성공 시 JWT를 `localStorage`에 저장 후 게임 페이지로 이동
- 비로그인 상태에서 PLAY 버튼 비활성화

### index.html
- 사이드바에 **전체 최고점수** 패널 추가 (`GET /scores/top`)
- 로그인한 사용자 닉네임 표시

### game.js
- 게임 오버 시 `POST /scores`로 점수·레벨·라인 수 전송
- 전송 후 최고점수 패널 갱신

---

## 인증 흐름

```
회원가입: 이메일 + 닉네임 + 비밀번호 → POST /register → 200 OK
로그인:   이메일 + 비밀번호 → POST /login → { access_token }
          → localStorage.setItem('token', access_token)
게임 종료: Authorization: Bearer <token> + 점수 → POST /scores
```

---

## 실행 방법 (로컬)

```bash
# 백엔드
cd backend
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography]
uvicorn main:app --reload --port 8000

# 프론트엔드 (별도 터미널)
cd ..
python3 -m http.server 8765
```

접속: `http://localhost:8765/landing.html`

---

## 구현 순서

1. `backend/` 디렉터리 및 기본 파일 생성
2. DB 모델 정의 (User, GameRecord)
3. 회원가입·로그인 API 구현 (JWT 발급)
4. 점수 저장·조회 API 구현
5. `landing.html` 로그인/회원가입 UI 추가
6. `game.js` 게임 종료 시 점수 POST 연동
7. `index.html` 최고점수 패널 추가
