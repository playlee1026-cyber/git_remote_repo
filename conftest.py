import os
import pytest
from dotenv import load_dotenv

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