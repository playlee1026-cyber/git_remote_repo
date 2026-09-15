from pages.base_page import BasePage
from config.settings import Config, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class CheckoutPage(BasePage):
    # [클린 코드 1번 원칙] 로케이터 및 상수를 중앙 설정(Config)에서 주입받아 매개변수화
    PAGE_URL_CHECKOUT_STEP = Config.PAGE_URL_CHECKOUT_STEP
    SELECTOR_BUTTON_SUBMIT_PAYMENT = Config.SELECTOR_BUTTON_SUBMIT_PAYMENT
    SELECTOR_TEXT_ERROR_MESSAGE = Config.SELECTOR_TEXT_ERROR_MESSAGE
    MOCK_PAYMENT_API_PATTERN = Config.MOCK_PAYMENT_API_PATTERN

    # [클린 코드 2번 원칙] 행동과 목적이 뚜렷한 메서드 네이밍
    def open_checkout_final_step_page(self):
        """결제 최종 확인 페이지로 진입합니다."""
        self.navigate_to_target_url(self.PAGE_URL_CHECKOUT_STEP)

    def setup_aml_limit_exceeded_network_interception(self, mock_handler_function):
        """
        의도: 실제 결제 API 대신, 
        AML 한도 초과 에러(403)를 반환하는 모킹(Mocking) 핸들러를 네트워크에 설정합니다.
        """
        self.ensure_configuration_is_valid("mock_handler_function", mock_handler_function)
        self.page.route(self.MOCK_PAYMENT_API_PATTERN, mock_handler_function)

    def submit_payment_information(self):
        """결제 완료 버튼을 클릭하여 결제를 시도합니다."""
        submit_button = self.page.locator(self.SELECTOR_BUTTON_SUBMIT_PAYMENT)
        submit_button.click()

    def verify_aml_compliance_error_alert_is_displayed(self, expected_error_text: str):
        """AML 규제 위반 에러 메시지가 UI에 정확히 노출되는지 검증합니다."""
        self.ensure_configuration_is_valid("expected_error_text", expected_error_text)
        
        error_alert_element = self.page.locator(self.SELECTOR_TEXT_ERROR_MESSAGE)
        
        # BasePage 설계 원칙에 따라 타임아웃 매개변수화 적용
        expect(error_alert_element).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)
        expect(error_alert_element).to_have_text(expected_error_text)