from pages.base_page import BasePage
from config.settings import URL_WEB_BASE
from playwright.sync_api import expect

class DashboardPage(BasePage):
    def verify_dashboard_loaded(self):
        self.wait_for_url(f"{URL_WEB_BASE}/dashboard")
        heading = self.page.get_by_role("heading", name="보안 대시보드")
        expect(heading).to_be_visible()