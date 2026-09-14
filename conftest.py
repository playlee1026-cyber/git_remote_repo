import pytest
import os
from config.settings import Config
from utils.slack_bot import notify_slack_on_test_failure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 다른 훅들이 먼저 실행되도록 양보하고 리포트 객체를 받습니다.
    outcome = yield
    report = outcome.get_result()

    # 테스트가 '실행(call)' 단계에서 '실패(failed)'했을 때만 작동
    if report.when == "call" and report.failed:
        test_name = item.name
        error_log = str(call.excinfo.getrepr(style="short"))

        page = item.funcargs.get("page")
        
        if page:
            # 1. 스크린샷 디렉토리 및 파일명 동적 할당
            os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
            screenshot_filename = f"{Config.SCREENSHOT_PREFIX}{test_name}.png"
            screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_filename)
            
            # 2. 실패 순간의 전체 화면 캡처
            page.screenshot(path=screenshot_path, full_page=True)

            # 3. Slack 전송 모듈 호출 (의존성 주입)
            notify_slack_on_test_failure(
                test_name=test_name,
                error_log=error_log,
                screenshot_path=screenshot_path,
                bot_token=Config.SLACK_BOT_TOKEN,
                channel_id=Config.SLACK_CHANNEL_ID,
                api_url=Config.SLACK_API_FILE_UPLOAD_URL,
                max_log_length=Config.SLACK_MAX_LOG_LENGTH
            )