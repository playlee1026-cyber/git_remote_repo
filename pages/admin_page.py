from pages.base_page import BasePage
# [클린 코드 1번 원칙] 타임아웃 매직 넘버 제거를 위한 중앙 상수 임포트
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class AdminPage(BasePage):
    # [클린 코드 1번 원칙] 매직 스트링(경로, 에러 메시지, 로케이터)을 클래스 상수로 캡슐화
    PATH_ADMIN_SETTINGS = "/admin/settings"
    TEXT_UNAUTHORIZED_WARNING = "관리자 권한이 없습니다."
    ROLE_BUTTON = "button"
    NAME_SAVE_SETTINGS_BUTTON = "시스템 설정 저장"

    # [클린 코드 2번 원칙 & 에러 해결] 이전 테스트 코드에서 호출한 목적 지향적인 이름으로 변경
    def attempt_unauthorized_access_to_admin_settings(self):
        """
        의도: 일반 사용자가 URL 조작을 통해 관리자 전용 설정 페이지에 강제 접속을 시도합니다.
        """
        target_admin_url = f"{URL_WEB_BASE}{self.PATH_ADMIN_SETTINGS}"
        
        # 이전 단계에서 리팩토링된 BasePage의 메서드로 변경
        self.navigate_to_target_url(target_admin_url, load_state="domcontentloaded")
        self.verify_current_url(target_admin_url)

    # [클린 코드 2번 원칙 & 에러 해결] 검증 목적이 뚜렷하게 드러나는 이름으로 변경
    def verify_access_denied_warning_is_displayed(self):
        """
        의도: 무단 접근 시 에러 토스트 메시지가 나타나고, 
        실제 관리자 전용 제어 요소(저장 버튼 등)는 노출되지 않는지 검증합니다.
        """
        # 1. 접근 권한 없음 에러 토스트 렌더링 확인 (매직 넘버 10000 대체)
        unauthorized_error_toast = self.page.get_by_text(self.TEXT_UNAUTHORIZED_WARNING)
        expect(unauthorized_error_toast).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)
        
        # 2. 관리자 전용 저장 버튼 미노출 확인 (매직 스트링 상수화)
        system_settings_save_button = self.page.get_by_role(
            self.ROLE_BUTTON, 
            name=self.NAME_SAVE_SETTINGS_BUTTON
        )
        expect(system_settings_save_button).not_to_be_visible()