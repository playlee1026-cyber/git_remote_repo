from playwright.sync_api import Page, expect

class AutomationExerciseHomePage:
    def __init__(self, page: Page):
        self.page = page
        self.signup_login_menu_button = page.locator("a[href='/login']")
        
    def navigate_to_home(self, base_url: str) -> None:
        """설정된 Base URL을 기반으로 홈페이지로 이동합니다."""
        self.page.goto(base_url)
        
    def click_signup_login_menu(self) -> None:
        """상단 네비게이션에서 회원가입/로그인 메뉴를 클릭합니다."""
        self.signup_login_menu_button.click()