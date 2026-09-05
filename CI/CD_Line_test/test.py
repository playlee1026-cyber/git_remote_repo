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


import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("username, password, expected_url, expected_message", [
    # 1번 케이스: 정상 로그인 (Positive)
    ("tomsmith", "SuperSecretPassword!", "https://the-internet.herokuapp.com/secure", "You logged into a secure area!"),
    
    # 2번 케이스: 잘못된 아이디 (Negative)
    ("invalid_user", "SuperSecretPassword!", "https://the-internet.herokuapp.com/login", "Your username is invalid!")
])
def test_login_matrix(page: Page, username, password, expected_url, expected_message):
    page.goto("https://the-internet.herokuapp.com/login")
    
    # 파라미터로 받은 데이터를 입력
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")
    
    # 결과 검증
    expect(page).to_have_url(expected_url)
    banner = page.locator("#flash")
    expect(banner).to_contain_text(expected_message)