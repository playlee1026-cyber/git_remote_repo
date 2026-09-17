from playwright.sync_api import Page, expect

class AutomationExerciseHomePage:
    LOGOUT_MENU_BUTTON_LOCATOR = "a[href='/logout']"
    LOGGED_IN_STATUS_INDICATOR_LOCATOR = "text=Logged in as"
    
    def __init__(self, page: Page):
        self.page = page
        self.home_page_identifier = page.locator("a:has-text('Home')")
        self.signup_login_menu_button = page.locator("a[href='/login']")
        self.delete_account_menu_button = page.locator("a[href='/delete_account']")

    def navigate_to_home(self, base_url: str) -> None:
        self.page.goto(base_url)

    def verify_home_page_is_visible(self) -> None:
        """Step 3: 홈페이지가 정상적으로 로드되었는지 검증합니다."""
        expect(self.home_page_identifier).to_be_visible(timeout=5000)

    def click_signup_login_menu(self) -> None:
        """Step 4: 회원가입/로그인 메뉴로 이동합니다."""
        self.signup_login_menu_button.click()

    def verify_logged_in_as_username(self, expected_username: str) -> None:
        """Step 16: 로그인된 사용자 이름이 상단에 노출되는지 검증합니다."""
        logged_in_locator = self.page.locator(f"text=Logged in as {expected_username}")
        expect(logged_in_locator).to_be_visible()

    def click_delete_account_menu(self) -> None:
        """Step 17: 계정 삭제 메뉴를 클릭합니다."""
        self.delete_account_menu_button.click()

    def click_logout_menu_button(self) -> None:
        self.page.click(self.LOGOUT_MENU_BUTTON_LOCATOR)

    def verify_user_is_logged_in(self) -> None:
        expect(self.page.locator(self.LOGGED_IN_STATUS_INDICATOR_LOCATOR)).to_be_visible()