from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class CartPage(BasePage):
    PATH_CART = "/cart.html"
    SELECTOR_BUTTON_CHECKOUT = "[data-test='checkout']"

    def verify_shopping_cart_page_is_loaded(self):
        """장바구니 페이지에 정상적으로 진입했는지 검증합니다."""
        expected_cart_url = f"{URL_WEB_BASE}{self.PATH_CART}"
        self.verify_current_url(expected_cart_url)
        
        checkout_proceed_button = self.page.locator(self.SELECTOR_BUTTON_CHECKOUT)
        expect(checkout_proceed_button).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)

    def proceed_to_checkout_step_one(self):
        """결제 진행(Checkout) 버튼을 클릭하여 배송지 입력 단계로 넘어갑니다."""
        checkout_proceed_button = self.page.locator(self.SELECTOR_BUTTON_CHECKOUT)
        checkout_proceed_button.click()