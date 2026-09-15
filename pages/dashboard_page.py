from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class DashboardPage(BasePage):
    # [클린 코드 1번 원칙] 매직 스트링(로케이터, 텍스트, 경로)을 클래스 상수로 분리하여 중앙 관리
    PATH_DASHBOARD = "/dashboard"
    ROLE_HEADING = "heading"
    TEXT_SECURITY_DASHBOARD = "보안 대시보드"

    # [클린 코드 2번 원칙] 단순 확인을 넘어 구체적인 목적을 명시하는 네이밍
    def verify_security_dashboard_is_fully_loaded(self):
        """
        의도: 로그인 성공 후 보안 대시보드 페이지로 URL이 정상 전환되었는지, 
        그리고 핵심 UI 요소인 헤딩(Heading)이 렌더링되었는지 검증합니다.
        """
        expected_dashboard_url = f"{URL_WEB_BASE}{self.PATH_DASHBOARD}"
        
        # 이전 단계에서 리팩토링한 BasePage의 명확한 검증 메서드 호출 (Fail-Fast 내장)
        self.verify_current_url(expected_dashboard_url)
        
        # UI 요소(DOM) 확보를 위한 직관적인 변수명 사용
        security_dashboard_heading = self.page.get_by_role(
            self.ROLE_HEADING, 
            name=self.TEXT_SECURITY_DASHBOARD
        )
        
        # [클린 코드 1번 원칙] 타임아웃 하드코딩 제거 및 중앙 설정 변수(TIMEOUT_ELEMENT_WAIT) 적용
        expect(security_dashboard_heading).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)