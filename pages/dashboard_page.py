from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class DashboardPage(BasePage):
    # [클린 코드 1번 원칙] 대시보드 검증을 위한 매직 스트링 상수화
    PATH_DASHBOARD = "/dashboard"
    ROLE_HEADING = "heading"
    TEXT_SECURITY_DASHBOARD = "보안 대시보드"

    # [클린 코드 1번 원칙] 상점 이동 버튼/링크를 위한 로케이터 상수화 
    # (실제 프로젝트 UI에 맞춰 텍스트나 로케이터 방식을 Config 수준으로 조정할 수 있습니다)
    ROLE_NAVIGATION_LINK = "link"
    TEXT_NAVIGATE_TO_INVENTORY = "상품 목록으로 이동"

    def verify_security_dashboard_is_fully_loaded(self):
        """
        의도: 로그인 성공 후 보안 대시보드 페이지로 URL이 정상 전환되었는지, 
        그리고 핵심 UI 요소인 헤딩(Heading)이 렌더링되었는지 검증합니다.
        """
        expected_dashboard_url = f"{URL_WEB_BASE}{self.PATH_DASHBOARD}"
        self.verify_current_url(expected_dashboard_url)
        
        security_dashboard_heading = self.page.get_by_role(
            self.ROLE_HEADING, 
            name=self.TEXT_SECURITY_DASHBOARD
        )
        expect(security_dashboard_heading).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)

    # [클린 코드 2번 원칙] 상점 페이지로의 진입 의도를 명확히 하는 네이밍
    def navigate_to_product_inventory(self):
        """
        의도: 대시보드 화면에서 상점(상품 목록) 페이지로 이동하는 내비게이션 링크를 클릭합니다.
        """
        inventory_navigation_link = self.page.get_by_role(
            self.ROLE_NAVIGATION_LINK,
            name=self.TEXT_NAVIGATE_TO_INVENTORY
        )
        
        # 요소가 렌더링되지 않았는데 클릭을 시도하여 발생하는 에러를 방지 (Fail-Fast 및 상태 동기화)
        expect(inventory_navigation_link).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)
        inventory_navigation_link.click()