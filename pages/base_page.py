from playwright.sync_api import Page, expect

# [클린 코드 1번 원칙] 매직 넘버(15000)를 제거하기 위해 중앙 설정에서 타임아웃 상수를 임포트합니다.
from config.settings import TIMEOUT_PAGE_LOAD

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # [4번 항목 적용] 환경 변수/설정값 누락 시 즉시 중단(Fail-Fast)하는 공통 검증 메서드
    def ensure_configuration_is_valid(self, config_key: str, config_value: str | None) -> None:
        """
        의도: 환경 변수나 필수 설정값이 None이거나 비어있을 경우,
        나중에 모호한 에러가 터지기 전에 즉시 명확한 메시지와 함께 테스트를 중단
        """
        if not config_value:
            raise ValueError(
                f"[환경 설정 오류] 필수 환경 변수 또는 설정값 '{config_key}'가 누락되었습니다. "
                f".env 파일이나 GitHub Secrets 설정을 확인해주세요."
            )

    def navigate_to_target_url(self, target_url: str, load_state: str = "networkidle"):
        # 이동하려는 URL 값이 비어있지 않은지 우선 검증 (Fail-Fast)
        self.ensure_configuration_is_valid("target_url", target_url)
        self.page.goto(target_url, wait_until=load_state)

    def verify_current_url(self, expected_url: str, timeout_ms: int = TIMEOUT_PAGE_LOAD):
        self.ensure_configuration_is_valid("expected_url", expected_url)        
       
        expect(self.page).to_have_url(expected_url, timeout=timeout_ms)