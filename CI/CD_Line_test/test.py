# def test_example_page_title(page: Page):
#     # 1. 브라우저로 특정 URL 이동 (Analogy: requests.get()으로 엔드포인트에 접속하는 것과 유사)
#     page.goto("https://example.com")
    
#     # 2. 웹페이지 타이틀 검증 (Analogy: Python assert문으로 응답값을 확인하는 것과 유사)
#     expect(page).to_have_title("Example Domain")
    
#     # 3. 특정 DOM 요소 텍스트 확인
#     heading = page.locator("h1")
#     expect(heading).to_contain_text("Example Domain")


# def test_form_login_action(page: Page):
#     # 1. 테스트용 로그인 페이지로 이동 (Analogy: API 엔드포인트에 접속)
#     page.goto("https://the-internet.herokuapp.com/login")
    
#     # 2. 아이디와 비밀번호 입력 (Analogy: 딕셔너리 변수에 값 세팅)
#     page.fill("#username", "tomsmith")
#     page.fill("#password", "SuperSecretPassword!")
    
#     # 3. 로그인 버튼 클릭 (Analogy: 이벤트 함수 트리거)
#     page.click("button[type='submit']")
    
#     # 4. 로그인 성공 페이지 URL 및 성공 메시지 검증 (Analogy: 응답 상태 코드 및 바디 검증)
#     expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    
#     success_banner = page.locator("#flash")
#     expect(success_banner).to_contain_text("You logged into a secure area!")


# import pytest
# from playwright.sync_api import Page, expect

# @pytest.mark.parametrize("username, password, expected_url, expected_message", [
#     # 1번 케이스: 정상 로그인 (Positive)
#     ("tomsmith", "SuperSecretPassword!", "https://the-internet.herokuapp.com/secure", "You logged into a secure area!"),
    
#     # 2번 케이스: 잘못된 아이디 (Negative)
#     ("invalid_user", "SuperSecretPassword!", "https://the-internet.herokuapp.com/login", "Your username is invalid!")
# ])
# def test_login_matrix(page: Page, username, password, expected_url, expected_message):
#     page.goto("https://the-internet.herokuapp.com/login")
    
#     # 파라미터로 받은 데이터를 입력
#     page.fill("#username", username)
#     page.fill("#password", password)
#     page.click("button[type='submit']")
    
#     # 결과 검증
#     expect(page).to_have_url(expected_url)
#     banner = page.locator("#flash")
#     expect(banner).to_contain_text(expected_message)

import pytest
from playwright.sync_api import Page, expect

# 테스트 대상 서버 URL (Render 등에 배포된 가상 서버 주소)
BASE_URL = "https://git-remote-repo.onrender.com"

def test_unauthorized_access_to_admin_page(page: Page):
    """
    [TC-SEC-01] 일반 사용자 계정의 관리자 페이지 접근 통제 검증
    - ISO/IEC 25010 품질 특성: 보안성 (Security) - 기밀성 및 권한 통제
    - 목적: 일반 권한의 세션으로 URL을 직접 조작하여 관리자 페이지 접근 시도시,
            프론트엔드 라우터가 이를 차단하고 적절한 예외 처리를 수행하는지 확인.
    """
    
    # 1. 일반 사용자(Normal User) 로그인 수행
    page.goto(f"{BASE_URL}/login")
    
    # 안정적인 요소 탐색을 위해 Role 또는 Placeholder 기반 탐색 사용
    page.get_by_placeholder("아이디").fill("normal_user")
    page.get_by_placeholder("비밀번호").fill("test_password123!")
    page.get_by_role("button", name="로그인").click()
    
    # 로그인 성공 및 대시보드 진입 대기 (Playwright의 Auto-waiting 활용)
    expect(page).to_have_url(f"{BASE_URL}/dashboard")
    expect(page.get_by_role("heading", name="보안 대시보드")).to_be_visible()

    # 2. 취약점 시나리오 시도: URL 강제 조작을 통한 관리자 페이지 접근
    page.goto(f"{BASE_URL}/admin/settings")

    # 3. 결과 검증 (백엔드 403 Forbidden 방어 로직 확인)
    
    # 검증 A: 관리자 전용 URL(/admin/settings) 접근이 유지되더라도 접근이 거부되었는지 확인 (URL 유지 또는 차단 확인)
    # (원하시는 경우 현재 URL이 유지되는지 체크할 수 있습니다)
    
    # 검증 B: 사용자에게 명확한 접근 불가 메시지("관리자 권한이 없습니다.")가 출력되는지 확인
    error_toast = page.get_by_text("관리자 권한이 없습니다.")
    expect(error_toast).to_be_visible()
    
    # 검증 C: 화면에 민감한 설정 버튼("시스템 설정 저장")이 노출되지 않았는지 교차 확인
    admin_save_button = page.get_by_role("button", name="시스템 설정 저장")
    expect(admin_save_button).not_to_be_visible()