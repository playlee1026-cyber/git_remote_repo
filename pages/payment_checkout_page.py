from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect


class PaymentCheckoutPage(BasePage):
    """Flask 목 서버의 /checkout 결제 화면 페이지 객체입니다."""

    PAY_BUTTON_NAME = "결제하기"
    PAYMENT_RESULT_LOCATOR = "#payment-result"

    def navigate_to_checkout(self) -> None:
        self.navigate(f"{URL_WEB_BASE}/checkout", wait_until="domcontentloaded")

    def click_pay_button(self) -> None:
        self.page.get_by_role("button", name=self.PAY_BUTTON_NAME).click()

    def verify_payment_result_message(self, expected_message: str) -> None:
        result = self.page.locator(self.PAYMENT_RESULT_LOCATOR)
        expect(result).to_have_text(expected_message, timeout=TIMEOUT_ELEMENT_WAIT)
