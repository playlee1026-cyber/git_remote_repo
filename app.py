from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ahnlab_portfolio_secret_key' # 세션 암호화를 위한 키

@app.route('/')
def home():
    return 'Hello, Render CI/CD Deployment Success! 🚀'

# 1. 로그인 엔드포인트 (테스트를 위한 로직)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('id')
        # 'normal_user'로 로그인 시 일반 권한(user) 부여
        if user_id == 'normal_user':
            session['role'] = 'user'
            return redirect(url_for('dashboard'))
        # 'admin_user'로 로그인 시 관리자 권한(admin) 부여
        elif user_id == 'admin_user':
            session['role'] = 'admin'
            return redirect(url_for('dashboard'))
        
    return '''
        <form method="post">
            <input type="text" name="id" placeholder="아이디">
            <input type="password" name="pw" placeholder="비밀번호">
            <button type="submit">로그인</button>
        </form>
    '''

# 2. 대시보드 (로그인한 사용자만 접근 가능)
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    return '<h1>보안 대시보드</h1><p>환영합니다.</p>'

# 3. 관리자 전용 페이지 (RBAC 방어 로직 핵심)
@app.route('/admin/settings')
def admin_settings():
    # 로그인을 안 한 경우
    if 'role' not in session:
        return redirect(url_for('login'))
    
    # 로그인은 했지만 관리자(admin)가 아닌 경우 -> 방어 로직 작동
    if session['role'] != 'admin':
        # 403 Forbidden 에러와 함께 경고 텍스트 반환
        return '<h1>접근 거부</h1><p>관리자 권한이 없습니다.</p>', 403
        
    return '<h1>시스템 설정</h1><button>시스템 설정 저장</button>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)