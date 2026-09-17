from playwright.sync_api import Page, expect

class AutomationExerciseLoginSignupPage:
    # 🌟 매직 스트링 배제: 특정 문자열을 함수 내부에 하드코딩하지 않고 클래스 상수로 분리하여 중앙 관리
    EXPECTED_SIGNUP_HEADING_TEXT = "New User Signup!"
    LOGIN_EMAIL_INPUT_LOCATOR = "input[data-qa='login-email']"
    LOGIN_PASSWORD_INPUT_LOCATOR = "input[data-qa='login-password']"
    LOGIN_SUBMIT_BUTTON_LOCATOR = "button[data-qa='login-button']"
    LOGIN_FORM_HEADER_LOCATOR = "h2:has-text('Login to your account')"
    
    def __init__(self, page: Page):
        self.page = page
        
        # 🌟 의도 표출 네이밍: 각 로케이터가 어떤 폼의 어떤 역할을 하는지 명확하게 작성
        self.new_user_signup_heading = page.locator(f"h2:has-text('{self.EXPECTED_SIGNUP_HEADING_TEXT}')")
        
        self.signup_name_input = page.locator("input[data-qa='signup-name']")
        self.signup_email_input = page.locator("input[data-qa='signup-email']")
        self.signup_submit_button = page.locator("button[data-qa='signup-button']")

    def verify_new_user_signup_is_visible(self) -> None:
        """
        Step 5: 'New User Signup!' 영역이 화면(DOM)에 안정적으로 렌더링되었는지 검증합니다.
        """
        expect(self.new_user_signup_heading).to_be_visible()

    def initiate_signup_process(self, target_user_name: str, target_user_email: str) -> None:
        """
        Step 6-7: 신규 사용자 가입을 위한 이름과 이메일을 폼에 입력하고 제출합니다.
        
        🌟 파라미터화: 이름과 이메일을 내부에서 하드코딩하지 않고, 테스트 스크립트에서 명시적으로 주입(전달)받아 처리합니다.
        """
        self.signup_name_input.fill(target_user_name)
        self.signup_email_input.fill(target_user_email)
        self.signup_submit_button.click()

    def verify_login_form_is_visible(self) -> None:
        expect(self.page.locator(self.LOGIN_FORM_HEADER_LOCATOR)).to_be_visible()

    def execute_login_with_credentials(self, target_email: str, target_password: str) -> None:
        self.page.fill(self.LOGIN_EMAIL_INPUT_LOCATOR, target_email)
        self.page.fill(self.LOGIN_PASSWORD_INPUT_LOCATOR, target_password)
        self.page.click(self.LOGIN_SUBMIT_BUTTON_LOCATOR)