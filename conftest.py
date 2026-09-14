import pytest
import os
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