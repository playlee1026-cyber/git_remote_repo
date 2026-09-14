import os
import requests

def notify_slack_on_test_failure(
    test_name: str, 
    error_log: str, 
    screenshot_path: str, 
    bot_token: str, 
    channel_id: str, 
    api_url: str, 
    max_log_length: int = 500
) -> None:
    if not bot_token or not channel_id:
        print("⚠️ Slack 토큰 또는 채널 ID가 설정되지 않아 알림을 생략합니다.")
        return

    truncated_log = error_log[:max_log_length]

    # API / UI 구분을 위해 타이틀 변경
    test_type = "UI" if screenshot_path else "API"
    message_text = (
        f"🚨 *[{test_type} Test Failed]* `{test_name}`\n"
        f"자세한 에러 로그는 아래를 확인해 주세요:\n"
        f"```\n{truncated_log}...\n```"
    )

    headers = {
        "Authorization": f"Bearer {bot_token}"
    }

    try:
        # 1. 스크린샷이 있는 경우 (UI 테스트)
        if screenshot_path and os.path.exists(screenshot_path):
            data = {
                "channels": channel_id,
                "initial_comment": message_text,
                "title": f"{test_name} - Error Screenshot"
            }
            with open(screenshot_path, 'rb') as file_content:
                files = {'file': file_content}
                response = requests.post(
                    api_url,
                    headers=headers,
                    data=data,
                    files=files
                )
        
        # 2. 스크린샷이 없는 경우 (API 테스트)
        else:
            data = {
                "channel": channel_id,
                "text": message_text
            }
            response = requests.post(
                "https://slack.com/api/chat.postMessage",
                headers=headers,
                json=data
            )

        if response.status_code == 200 and response.json().get("ok"):
            print(f"✅ Slack으로 에러 리포트 전송 성공: {test_name}")
        else:
            print(f"❌ Slack 전송 실패: {response.text}")
            
    except Exception as e:
        print(f"❌ Slack API 호출 중 에러 발생: {e}")