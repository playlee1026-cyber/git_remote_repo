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

class Config:
    # [Test Environment]
    BASE_URL = os.getenv("TEST_BASE_URL", "https://www.saucedemo.com/")
    UI_TIMEOUT_MS = int(os.getenv("UI_TIMEOUT_MS", 3000))
    
    # [Screenshot Settings]
    SCREENSHOT_DIR = os.path.join(os.getcwd(), "test-results", "screenshots")
    SCREENSHOT_PREFIX = "FAIL_"

    # [Slack Bot Settings]
    SLACK_API_FILE_UPLOAD_URL = "https://slack.com/api/files.upload"
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
    SLACK_MAX_LOG_LENGTH = int(os.getenv("SLACK_MAX_LOG_LENGTH", 500))
    # [AML Network Mocking Settings] 가상자산/금융 규제 모킹용 데이터
    MOCK_PAYMENT_API_PATTERN = "**/api/v1/payments"
    MOCK_AML_ERROR_STATUS_CODE = 403
    MOCK_AML_ERROR_RESPONSE_JSON = {
        "error_code": "ERR_AML_LIMIT_EXCEEDED",
        "message": "자금세탁방지(AML) 규제에 따라 1일 최대 이체 한도를 초과하였습니다."
    }

    # [UI Elements Settings] UI 상호작용을 위한 엘리먼트 셀렉터 (SauceDemo 등 타겟 사이트에 맞게 수정 가능)
    PAGE_URL_CHECKOUT_STEP = os.getenv("TEST_CHECKOUT_URL", "https://www.saucedemo.com/checkout-step-two.html")
    SELECTOR_BUTTON_SUBMIT_PAYMENT = "button[data-test='finish']"
    SELECTOR_TEXT_ERROR_MESSAGE = "h3[data-test='error']"
    
    # [Expected Results] 프론트엔드에 노출되어야 할 기대 결과 텍스트
    EXPECTED_UI_AML_ERROR_TEXT = "자금세탁방지(AML) 규제에 따라 1일 최대 이체 한도를 초과하였습니다."