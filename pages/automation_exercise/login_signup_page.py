from playwright.sync_api import Page, expect

class AutomationExerciseLoginSignupPage:
    def __init__(self, page: Page):
        self.page = page
        # Signup Form Locators
        self.new_user_signup_title = page.locator("div.signup-form h2")
        self.signup_name_input = page.locator("[data-qa='signup-name']")
        self.signup_email_input = page.locator("[data-qa='signup-email']")
        self.signup_button = page.locator("[data-qa='signup-button']")
        
        # Account Information Form Locators (Next Step)
        self.account_information_form_title = page.locator("b:has-text('Enter Account Information')")

    def initiate_signup_process(self, target_user_name: str, target_user_email: str) -> None:
        """
        초기 이름과 이메일을 입력하여 회원가입 프로세스를 시작합니다.
        매직 스트링 대신 파라미터화된 데이터를 주입받아 동작합니다.
        """
        self.signup_name_input.fill(target_user_name)
        self.signup_email_input.fill(target_user_email)
        self.signup_button.click()
        
    def verify_account_information_form_is_visible(self) -> None:
        """
        네트워크 지연을 고려하여 다음 단계 폼이 안정적으로 렌더링되었는지 상태를 검증합니다.
        단순 노출 확인을 넘어 견고한 대기(Resilient Wait)를 수행합니다.
        """
        expect(self.account_information_form_title).to_be_visible(timeout=5000)