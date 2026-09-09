from flask import Flask, session, request, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'ahnlab_portfolio_secret_key' # 세션 암호화를 위한 키

@app.route('/')
def home():
    return '안녕Hello안녕, Render CI/CD Deployment Success! 🚀'

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
    if 'role' not in session:
        return redirect(url_for('login'))     
    if session['role'] != 'admin':
        # 대시보드로 리다이렉트하는 대신 접근 거부 메시지 반환
        return '관리자 권한이 없습니다.', 403
        
    return '<h1>시스템 설정</h1><button>시스템 설정 저장</button>'


# --- 추가된 데이터 주도 테스트용 Mock API 엔드포인트 ---

# 4. 회원가입 API (Signup)
@app.route('/api/v1/signup', methods=['POST'])
def mock_signup():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    if data['email'] == "invalid-email-format":
        return jsonify({"error": "Invalid email format"}), 400
    if len(data.get('password', '')) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if data['email'] == "existing@example.com":
        return jsonify({"error": "Email already exists"}), 409
        
    return jsonify({"message": "User created successfully"}), 201

# 5. 기존 결제 API (TC_PAY_001 ~ 003 테스트용)
@app.route('/api/v1/payments', methods=['POST'])
def mock_payments():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    if data.get('amount', 0) <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400
    if data.get('card_token') == "invalid_token":
        return jsonify({"error": "Payment Required - Invalid Card"}), 402
    return jsonify({"status": "SUCCESS", "transaction_id": "txn_8899"}), 200

# 5-1. 고도화된 보안/결제 API (TC_PAY_004 ~ 010 테스트용)
# --- 신규 추가: 금융/보안 엣지 케이스 방어 로직이 적용된 결제 API ---
@app.route('/api/payment', methods=['POST'])
def secure_payment_mock():
    data = request.get_json()
    
    # JSON 바디가 없는 경우 방어
    if not data:
        return jsonify({"error": "Invalid request payload"}), 400

    tx_id = data.get('tx_id')
    user_id = data.get('user_id')
    amount = data.get('amount')
    auth_token = data.get('auth_token')

    # 1. 인증/인가 검증 (보안 엣지 케이스 방어)
    if not auth_token:
        # TC_PAY_008: 토큰 누락
        return jsonify({"error": "Unauthorized: Missing auth token"}), 401
        
    if auth_token == "expired_or_invalid_string":
        # TC_PAY_009: 만료/변조된 토큰
        return jsonify({"error": "Unauthorized: Invalid or expired token"}), 401
        
    if user_id == "U9999_OTHER" and auth_token == "valid_token_for_U1001":
        # TC_PAY_010: 타인의 계정으로 접근 시도 (권한 우회)
        return jsonify({"error": "Forbidden: Permission denied for this user_id"}), 403

    # 2. 결제 금액 검증 (비정상 금액 엣지 케이스 방어)
    if amount is not None:
        if amount <= 0:
            # TC_PAY_004, TC_PAY_005: 마이너스(-) 및 0원 결제 시도
            return jsonify({"error": "Bad Request: Amount must be greater than 0"}), 400
        
        if amount >= 99999999999:
            # TC_PAY_006: 1회 결제 한도 초과 (비상식적 고액)
            return jsonify({"error": "Bad Request: Amount exceeds maximum limit"}), 400

    # 3. 트랜잭션 동시성 및 중복 제어 (중복 결제 방어)
    if tx_id == "TX_DUPLICATE_01":
        # TC_PAY_007: 이미 처리 완료된 트랜잭션 ID 재요청
        return jsonify({"error": "Conflict: Transaction ID already processed"}), 409

    # 4. 모든 보안/예외 검증을 통과한 정상 결제 처리
    return jsonify({
        "status": "SUCCESS", 
        "transaction_id": tx_id,
        "message": "Payment processed securely"
    }), 200

# 6. 게시판 API (Board)
@app.route('/api/v1/posts', methods=['POST'])
def mock_create_post():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
        
    return jsonify({"post_id": 500, "status": "published"}), 201

@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def mock_delete_post(post_id):
    # 권한 거부(403) 시나리오 검증용 응답
    return jsonify({"error": "Forbidden: You do not have permission to delete this post"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)