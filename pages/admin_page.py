from pages.base_page import BasePage
from config.settings import URL_WEB_BASE
from playwright.sync_api import expect

class AdminPage(BasePage):
    def force_navigate_to_settings(self):
        self.navigate(f"{URL_WEB_BASE}/admin/settings", wait_until="domcontentloaded")
        self.wait_for_url(f"{URL_WEB_BASE}/admin/settings")

    def verify_unauthorized_access_blocked(self):
        error_toast = self.page.get_by_text("관리자 권한이 없습니다.")
        expect(error_toast).to_be_visible(timeout=10000)
        
        admin_save_button = self.page.get_by_role("button", name="시스템 설정 저장")
        expect(admin_save_button).not_to_be_visible()