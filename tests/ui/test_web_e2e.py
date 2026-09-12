import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage
# 중앙 설정에서 권한 계정 가져오기
from config.settings import CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD

@pytest.mark.ui
@pytest.mark.security
def test_unauthorized_access_to_admin_page(page: Page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    admin_page = AdminPage(page)

    login_page.navigate_to_login()
    
    # 🌟 하드코딩 배제: 중앙 관리되는 변수를 파라미터로 전달
    login_page.login(CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD)
    
    dashboard_page.verify_dashboard_loaded()
    admin_page.force_navigate_to_settings()
    admin_page.verify_unauthorized_access_blocked()