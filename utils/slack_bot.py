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
    """
    테스트 실패 시 에러 로그와 스크린샷을 지정된 Slack 채널로 전송합니다.
    """
    if not bot_token or not channel_id:
        print("⚠️ Slack 토큰 또는 채널 ID가 설정되지 않아 알림을 생략합니다.")
        return

    # 설정된 길이만큼만 로그 슬라이싱
    truncated_log = error_log[:max_log_length]

    initial_comment = (
        f"🚨 *[UI Test Failed]* `{test_name}`\n"
        f"자세한 에러 로그는 아래를 확인해 주세요:\n"
        f"```\n{truncated_log}...\n```"
    )

    headers = {
        "Authorization": f"Bearer {bot_token}"
    }
    
    data = {
        "channels": channel_id,
        "initial_comment": initial_comment,
        "title": f"{test_name} - Error Screenshot"
    }

    try:
        with open(screenshot_path, 'rb') as file_content:
            files = {'file': file_content}
            response = requests.post(
                api_url,
                headers=headers,
                data=data,
                files=files
            )

        if response.status_code == 200 and response.json().get("ok"):
            print(f"✅ Slack으로 에러 리포트 전송 성공: {test_name}")
        else:
            print(f"❌ Slack 전송 실패: {response.text}")
            
    except FileNotFoundError:
        print(f"❌ 스크린샷 파일을 찾을 수 없습니다: {screenshot_path}")
    except Exception as e:
        print(f"❌ Slack API 호출 중 에러 발생: {e}")