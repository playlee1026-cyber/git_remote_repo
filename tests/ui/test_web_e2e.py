import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

from config.settings import CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD

@pytest.mark.ui
@pytest.mark.security
# [클린 코드 2번 원칙] 테스트 함수의 목적이 더 명확히 드러나도록 네이밍 변경
def test_normal_user_blocked_from_admin_settings(page: Page):
    """
    의도: 일반 권한의 사용자가 관리자 전용 설정 페이지에 강제 접근을 시도할 때, 
    정상적으로 접근이 차단되는지 검증.
    """
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    admin_page = AdminPage(page)

    # 1. 로그인 페이지 접속 (수정된 메서드명 적용)
    login_page.open_login_page()
    
    # 2. 인증 시도: 하드코딩 배제 및 수정된 메서드명 적용
    login_page.authenticate_user(CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD)
    
    # 3. 로그인 성공 및 대시보드 로드 검증 (수정된 메서드명 적용)
    dashboard_page.verify_security_dashboard_is_fully_loaded()
    
    # 4. 관리자 페이지 강제 접속 시도 (단순 force_navigate... 대신 목적을 명시)
    admin_page.attempt_unauthorized_access_to_admin_settings()
    
    # 5. 접근 차단 검증 (단순 verify...blocked 대신 무엇을 확인하는지 명시)
    admin_page.verify_access_denied_warning_is_displayed()