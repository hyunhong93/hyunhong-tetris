const API_BASE = 'http://localhost:8000';

function switchTab(tab) {
  document.getElementById('login-tab').style.display = tab === 'login' ? 'flex' : 'none';
  document.getElementById('register-tab').style.display = tab === 'register' ? 'flex' : 'none';
  document.querySelectorAll('.tab-btn').forEach((btn, i) => {
    btn.classList.toggle('active', (i === 0) === (tab === 'login'));
  });
}

async function doLogin() {
  const email = document.getElementById('login-email').value.trim();
  const pw    = document.getElementById('login-pw').value;
  const msg   = document.getElementById('login-msg');
  msg.textContent = '';
  try {
    const res  = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pw }),
    });
    const data = await res.json();
    if (!res.ok) { msg.textContent = data.detail; return; }
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('nickname', data.nickname);
    showPlayBox();
  } catch {
    msg.textContent = '서버에 연결할 수 없습니다 (백엔드를 실행하세요)';
  }
}

async function doRegister() {
  const email    = document.getElementById('reg-email').value.trim();
  const nickname = document.getElementById('reg-nickname').value.trim();
  const pw       = document.getElementById('reg-pw').value;
  const msg      = document.getElementById('reg-msg');
  msg.textContent = '';
  try {
    const res  = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, nickname, password: pw }),
    });
    const data = await res.json();
    if (!res.ok) { msg.textContent = data.detail; return; }
    msg.style.color = '#4caf50';
    msg.textContent = '가입 완료! 로그인해 주세요';
    switchTab('login');
  } catch {
    msg.textContent = '서버에 연결할 수 없습니다 (백엔드를 실행하세요)';
  }
}

function doLogout() {
  localStorage.removeItem('token');
  localStorage.removeItem('nickname');
  document.getElementById('play-box').style.display   = 'none';
  document.getElementById('auth-tabs').style.display  = 'flex';
  document.getElementById('login-tab').style.display  = 'flex';
  document.getElementById('register-tab').style.display = 'none';
  document.querySelectorAll('.tab-btn').forEach((b, i) => b.classList.toggle('active', i === 0));
}

function showPlayBox() {
  const nickname = localStorage.getItem('nickname');
  document.getElementById('auth-tabs').style.display     = 'none';
  document.getElementById('login-tab').style.display     = 'none';
  document.getElementById('register-tab').style.display  = 'none';
  document.getElementById('welcome-text').textContent    = `${nickname}님, 환영합니다!`;
  document.getElementById('play-box').style.display      = 'flex';
}

window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('token')) showPlayBox();
});
