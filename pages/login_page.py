from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class LoginPage(BasePage):
    # [클린 코드 1번 원칙] 로케이터(매직 스트링)를 클래스 상수로 분리하여 중앙 관리
    PLACEHOLDER_USERNAME = "아이디"
    PLACEHOLDER_PASSWORD = "비밀번호"
    ROLE_LOGIN_BUTTON = "로그인"

    def open_login_page(self):
        """로그인 페이지로 접속합니다."""
        target_url = f"{URL_WEB_BASE}/login"
        # 이전 단계에서 리팩토링한 BasePage의 메서드 호출
        self.navigate_to_target_url(target_url)

    def authenticate_user(self, username, password):
        """
        의도: 사용자 인증 정보(아이디, 비밀번호)를 입력하고 로그인 버튼을 클릭하여 인증을 시도합니다.
        """
        # [Fail-Fast 적용] 자격증명 값 누락 시 브라우저가 멈추기 전에 즉시 에러 발생 (BasePage의 검증 메서드 활용)
        self.ensure_configuration_is_valid("username", username)
        self.ensure_configuration_is_valid("password", password)

        # 1. 아이디 입력 필드 확보 및 렌더링 대기
        username_input_field = self.page.get_by_placeholder(self.PLACEHOLDER_USERNAME)
        
        # [클린 코드 1번 원칙] 매직 넘버(10000)를 중앙 설정 상수(TIMEOUT_ELEMENT_WAIT)로 대체
        expect(username_input_field).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)
        username_input_field.fill(username)
        
        # 2. 비밀번호 입력
        password_input_field = self.page.get_by_placeholder(self.PLACEHOLDER_PASSWORD)
        password_input_field.fill(password)
        
        # 3. 로그인 버튼 클릭
        login_submit_button = self.page.get_by_role("button", name=self.ROLE_LOGIN_BUTTON)
        login_submit_button.click()