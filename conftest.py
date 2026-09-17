import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page


# ---------------------------------------------------------
# [로컬 환경 변수 초기화]
# 프로젝트 루트에 위치한 .env 파일을 찾아 로컬 메모리에 주입합니다.
# 클린 아키텍처 원칙에 따라, 환경 변수에 의존하는 내부 모듈(config.settings 등)을
# 임포트하기 '전'에 반드시 먼저 실행되어야 합니다.
# ---------------------------------------------------------
load_dotenv()

# 환경 변수가 안전하게 로드된 이후에 프로젝트 모듈을 임포트합니다.
from config.settings import Config
from utils.slack_bot import notify_slack_on_test_failure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        test_name = item.name
        error_log = str(call.excinfo.getrepr(style="short"))

        # UI 테스트인 경우(page 픽스처가 있는 경우)에만 스크린샷 경로 생성 및 촬영
        page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
        screenshot_path = None
        
        if page:
            os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
            screenshot_filename = f"{Config.SCREENSHOT_PREFIX}{test_name}.png"
            screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_filename)
            
            page.screenshot(path=screenshot_path, full_page=True)

        # API 테스트(스크린샷 없음)와 UI 테스트(스크린샷 있음) 모두 슬랙 전송
        notify_slack_on_test_failure(
            test_name=test_name,
            error_log=error_log,
            screenshot_path=screenshot_path,  # API 테스트면 None이 전달됨
            bot_token=Config.SLACK_BOT_TOKEN,
            channel_id=Config.SLACK_CHANNEL_ID,
            max_log_length=Config.SLACK_MAX_LOG_LENGTH
        )

        #####

from pages.automation_exercise.home_page import AutomationExerciseHomePage
from pages.automation_exercise.login_signup_page import AutomationExerciseLoginSignupPage
from pages.automation_exercise.signup_details_page import AutomationExerciseSignupDetailsPage
from pages.automation_exercise.system_message_page import AutomationExerciseSystemMessagePage

@pytest.fixture
def ae_home_page(page: Page) -> AutomationExerciseHomePage:
    """Automation Exercise의 홈 페이지 객체를 제공하는 픽스처입니다."""
    return AutomationExerciseHomePage(page)

@pytest.fixture
def ae_login_signup_page(page: Page) -> AutomationExerciseLoginSignupPage:
    """Automation Exercise의 초기 회원가입 및 로그인 폼 페이지 객체를 제공하는 픽스처입니다."""
    return AutomationExerciseLoginSignupPage(page)

# 🌟 [추가된 코드] 누락되었던 의존성(Fixture) 팩토리 등록
@pytest.fixture
def ae_signup_details_page(page: Page) -> AutomationExerciseSignupDetailsPage:
    """Automation Exercise의 상세 계정 정보 입력 페이지 객체를 제공하는 픽스처입니다."""
    return AutomationExerciseSignupDetailsPage(page)

@pytest.fixture
def ae_system_message_page(page: Page) -> AutomationExerciseSystemMessagePage:
    """Automation Exercise의 시스템 결과 메시지(계정 생성, 삭제 등) 확인 페이지 객체를 제공하는 픽스처입니다."""
    return AutomationExerciseSystemMessagePage(page)

#1. 새로 생성한 페이지 객체 클래스 임포트
from pages.automation_exercise.products_page import AutomationExerciseProductsPage
from pages.automation_exercise.cart_page import AutomationExerciseCartPage

# 2. 의도가 드러나는 네이밍을 적용한 픽스처 등록
@pytest.fixture
def ae_products_page(page: Page) -> AutomationExerciseProductsPage:
    """
    [Intention] Playwright의 기본 page 객체를 주입받아 ProductsPage 객체를 인스턴스화하여 반환합니다.
    테스트 모듈에서 ae_products_page 파라미터 호출 시 자동으로 주입됩니다.
    """
    return AutomationExerciseProductsPage(page=page)

@pytest.fixture
def ae_cart_page(page: Page) -> AutomationExerciseCartPage:
    """
    [Intention] Playwright의 기본 page 객체를 주입받아 CartPage 객체를 인스턴스화하여 반환합니다.
    테스트 모듈에서 ae_cart_page 파라미터 호출 시 자동으로 주입됩니다.
    """
    return AutomationExerciseCartPage(page=page)

import pytest
from playwright.sync_api import BrowserContext

# 매직 스트링 배제: 차단할 광고 서버 도메인 패턴 상수화
ADVERTISEMENT_NETWORK_PATTERNS = [
    "**/*googlesyndication.com**",
    "**/*doubleclick.net**",
    "**/*googleadservices.com**",
    "**/*adservice.google.com**"
]

@pytest.fixture(autouse=True)
def block_external_advertisement_networks(context: BrowserContext) -> None:
    """
    [Intention] 구글 비네트(Vignette) 등 E2E 테스트 흐름을 방해하는 
    외부 광고 스크립트의 네트워크 요청을 컨텍스트 레벨에서 원천 차단(Abort)합니다.
    """
    for target_pattern in ADVERTISEMENT_NETWORK_PATTERNS:
        context.route(target_pattern, lambda route: route.abort())
    
    yield