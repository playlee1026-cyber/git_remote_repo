from pages.base_page import BasePage
from config.settings import URL_WEB_BASE
from playwright.sync_api import expect

class LoginPage(BasePage):
    def navigate_to_login(self):
        self.navigate(f"{URL_WEB_BASE}/login")

    def login(self, username, password):
        username_input = self.page.get_by_placeholder("아이디")
        expect(username_input).to_be_visible(timeout=10000)
        username_input.fill(username)
        
        self.page.get_by_placeholder("비밀번호").fill(password)
        self.page.get_by_role("button", name="로그인").click()