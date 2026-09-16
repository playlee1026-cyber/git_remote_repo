from playwright.sync_api import Page, expect

class AutomationExerciseSystemMessagePage:
    def __init__(self, page: Page):
        self.page = page
        
        # 🌟 의도 표출 네이밍: 해당 요소가 버튼 형태의 로케이터임을 명확히 명시합니다.
        self.continue_action_button = page.locator("[data-qa='continue-button']")

    def verify_message_is_visible(self, expected_system_message: str) -> None:
        """
        화면에 특정 시스템 결과 메시지가 노출되었는지 검증합니다.
        
        🌟 하드코딩 배제: 'ACCOUNT CREATED!' 와 같은 특정 문자열을 내부에 고정하지 않고,
        검증하고자 하는 대상 문자열을 외부(테스트 스크립트)에서 파라미터로 주입받아 동적으로 식별합니다.
        """
        # 주입받은 텍스트를 기반으로 동적 로케이터 생성
        dynamic_message_locator = self.page.locator(f"b:has-text('{expected_system_message}')")
        
        # 상태 기반 검증
        expect(dynamic_message_locator).to_be_visible()

    def click_continue_button(self) -> None:
        """
        결과 확인 후 다음 단계로 넘어가기 위한 계속(Continue) 버튼을 클릭합니다.
        """
        self.continue_action_button.click()