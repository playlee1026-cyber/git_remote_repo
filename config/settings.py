import os

# ---------------------------------------------------------
# 1. API 테스트 설정
# ---------------------------------------------------------
URL_API_BASE = "https://git-remote-repo.onrender.com"

# API 데이터 주도 테스트(DDT)용 CSV 경로
PATH_SIGNUP_CSV = os.path.join("data", "signup_api_test.csv")
PATH_PAYMENT_CSV = os.path.join("data", "payment_api_test.csv")
PATH_BOARD_CSV = os.path.join("data", "board_api_test.csv")

# ---------------------------------------------------------
# 2. Web UI 테스트 설정
# ---------------------------------------------------------
URL_WEB_BASE = "https://git-remote-repo.onrender.com"

# 타임아웃(Timeout) 중앙 통제 (밀리초 단위)
# 네트워크 환경에 따라 대기 시간을 일괄 조정해야 할 때 이곳만 수정하면 됩니다.
TIMEOUT_DEFAULT = 5000
TIMEOUT_ELEMENT_WAIT = 10000  # 입력창, 에러 토스트 등 특정 DOM 요소 렌더링 대기용
TIMEOUT_PAGE_LOAD = 15000     # 로그인 후 대시보드 진입 등 페이지 전환 대기용

# 테스트 자격증명 (권한별 분리)
CREDENTIAL_NORMAL_USER_ID = "normal_user"
CREDENTIAL_NORMAL_USER_PASSWORD = "test_password123!"

# 추후 관리자 테스트가 추가될 경우를 대비한 플레이스홀더
# CREDENTIAL_ADMIN_USER_ID = "admin_user"
# CREDENTIAL_ADMIN_USER_PASSWORD = "admin_password123!"