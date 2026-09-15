import os

# ---------------------------------------------------------
# 1. API 테스트 설정
# ---------------------------------------------------------
# 환경 변수에서 URL을 주입받아 다양한 환경(Dev, Stg, Prod)에서 테스트 가능하게 분리
# (환경 변수가 없을 경우를 대비해 기존 URL을 기본값으로 설정하여 하위 호환성 유지)
URL_API_BASE = os.getenv("API_BASE_URL", "https://git-remote-repo.onrender.com")

# # API 데이터 주도 테스트(DDT)용 CSV 경로
# PATH_SIGNUP_CSV = os.path.join("data", "signup_api_test.csv")
# PATH_PAYMENT_CSV = os.path.join("data", "payment_api_test.csv")
# PATH_BOARD_CSV = os.path.join("data", "board_api_test.csv")

# ---------------------------------------------------------
# 2. Web UI 테스트 설정
# ---------------------------------------------------------
URL_WEB_BASE = os.getenv("WEB_BASE_URL", "https://git-remote-repo.onrender.com")

# 타임아웃(Timeout) 중앙 통제 (밀리초 단위)
TIMEOUT_DEFAULT = 5000
TIMEOUT_ELEMENT_WAIT = 10000  # 입력창, 에러 토스트 등 특정 DOM 요소 렌더링 대기용
TIMEOUT_PAGE_LOAD = 15000     # 로그인 후 대시보드 진입 등 페이지 전환 대기용
API_REQUEST_TIMEOUT_SECONDS = 5 # 네트워크 환경에 따른  전체 API 테스트의 기본 대기 시간

# 테스트 자격증명 (권한별 분리)
# 평문 하드코딩을 제거하고 환경 변수에서 안전하게 호출하도록 100% 매개변수화 적용
CREDENTIAL_NORMAL_USER_ID = os.getenv("NORMAL_USER_ID")
CREDENTIAL_NORMAL_USER_PASSWORD = os.getenv("NORMAL_USER_PASSWORD")

# 추후 관리자 테스트가 추가될 경우를 대비한 플레이스홀더
# CREDENTIAL_ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
# CREDENTIAL_ADMIN_USER_PASSWORD = os.getenv("ADMIN_USER_PASSWORD")

class Config:
    # [AML Network Mocking Settings]
    MOCK_AML_ERROR_STATUS_CODE = 403
    MOCK_AML_ERROR_RESPONSE_JSON = {
        "error_code": "ERR_AML_LIMIT_EXCEEDED",
        "message": "자금세탁방지(AML) 규제에 따라 1일 최대 이체 한도를 초과하였습니다."
    }

    # [Slack Bot Settings]
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
    SLACK_MAX_LOG_LENGTH = int(os.getenv("SLACK_MAX_LOG_LENGTH", 500))
    SCREENSHOT_DIR = os.path.join(os.getcwd(), "test-results", "screenshots")
    SCREENSHOT_PREFIX = "FAIL_"

class ApiTestConfiguration:
    """API 테스트를 위한 설정 및 상수를 관리하는 객체입니다."""
    
    BASE_URL = "https://git-remote-repo.onrender.com"
    REQUEST_TIMEOUT_SECONDS = 5
    
    # 도메인별 테스트 데이터 CSV 파일 경로 상수
    SIGNUP_TEST_DATA_CSV_PATH = "data/signup_api_test.csv"
    PAYMENT_TEST_DATA_CSV_PATH = "data/payment_api_test.csv"
    BOARD_TEST_DATA_CSV_PATH = "data/board_api_test.csv"
    
    FALLBACK_VALUE_FOR_MISSING_DATA = ""