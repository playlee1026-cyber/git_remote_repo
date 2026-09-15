from pages.base_page import BasePage
from config.settings import URL_WEB_BASE
from playwright.sync_api import expect

class CheckoutStepOnePage(BasePage):
    PATH_CHECKOUT_STEP_ONE = "/checkout-step-one.html"
    
    # 폼 입력 필드 로케이터 상수화
    SELECTOR_INPUT_FIRST_NAME = "[data-test='firstName']"
    SELECTOR_INPUT_LAST_NAME = "[data-test='lastName']"
    SELECTOR_INPUT_POSTAL_CODE = "[data-test='postalCode']"
    SELECTOR_BUTTON_CONTINUE = "[data-test='continue']"

    def verify_checkout_step_one_is_loaded(self):
        """배송지 정보를 입력하는 Checkout Step One 페이지 로딩을 검증합니다."""
        expected_step_one_url = f"{URL_WEB_BASE}{self.PATH_CHECKOUT_STEP_ONE}"
        self.verify_current_url(expected_step_one_url)

    # 입력값을 하드코딩하지 않고 매개변수(Parameter)로 외부에서 주입받음
    def submit_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        """
        의도: 외부에서 주입받은 배송지 정보(이름, 성, 우편번호)를 폼에 입력하고 다음 단계로 진행합니다.
        """
        # [Fail-Fast 방어 로직] 필수 입력 데이터가 None이거나 비어있으면 브라우저 조작 전 즉시 에러 발생
        self.ensure_configuration_is_valid("first_name", first_name)
        self.ensure_configuration_is_valid("last_name", last_name)
        self.ensure_configuration_is_valid("postal_code", postal_code)

        # 1. 폼 데이터 입력 (변수명을 직관적으로 사용하여 목적 명시)
        first_name_input_field = self.page.locator(self.SELECTOR_INPUT_FIRST_NAME)
        first_name_input_field.fill(first_name)

        last_name_input_field = self.page.locator(self.SELECTOR_INPUT_LAST_NAME)
        last_name_input_field.fill(last_name)

        postal_code_input_field = self.page.locator(self.SELECTOR_INPUT_POSTAL_CODE)
        postal_code_input_field.fill(postal_code)

        # 2. 다음 단계로 진행
        continue_submit_button = self.page.locator(self.SELECTOR_BUTTON_CONTINUE)
        continue_submit_button.click()