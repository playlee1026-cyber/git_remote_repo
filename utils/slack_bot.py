import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def notify_slack_on_test_failure(
    test_name: str, 
    error_log: str, 
    bot_token: str, 
    channel_id: str, 
    screenshot_path: str = None, 
    max_log_length: int = 500
) -> None:
    """
    테스트 실패 시 Slack SDK를 활용하여 에러 로그 및 스크린샷(존재 시)을 전송합니다.
    """
    if not bot_token or not channel_id:
        print("⚠️ Slack 토큰 또는 채널 ID가 설정되지 않아 알림을 생략합니다.")
        return

    client = WebClient(token=bot_token)
    truncated_log = error_log[:max_log_length]
    test_type = "UI" if screenshot_path else "API"
    
    message_text = (
        f"🚨 *[{test_type} Test Failed]* `{test_name}`\n"
        f"자세한 에러 로그는 아래를 확인해 주세요:\n"
        f"```\n{truncated_log}...\n```"
    )

    try:
        # 스크린샷 파일이 유효한 경우 v2 업로드 방식 사용
        if screenshot_path and os.path.exists(screenshot_path):
            client.files_upload_v2(
                channel=channel_id,
                initial_comment=message_text,
                file=screenshot_path,
                title=f"{test_name} - Error Screenshot"
            )
        # API 테스트 등 스크린샷이 없는 경우 텍스트 메시지만 전송
        else:
            client.chat_postMessage(
                channel=channel_id,
                text=message_text
            )
        print(f"✅ Slack으로 에러 리포트 전송 성공: {test_name}")
        
    except SlackApiError as api_error:
        print(f"❌ Slack API 에러: {api_error.response['error']}")
    except Exception as system_error:
        print(f"❌ Slack 알림 전송 중 시스템 에러 발생: {system_error}")