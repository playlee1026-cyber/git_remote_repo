from pages.base_page import BasePage
from config.settings import URL_WEB_BASE, TIMEOUT_ELEMENT_WAIT
from playwright.sync_api import expect

class InventoryPage(BasePage):
    # 페이지 전용 로케이터 및 경로를 상수화하여 매직 스트링 제거
    PATH_INVENTORY = "/inventory.html"
    SELECTOR_BUTTON_ADD_TO_CART = "button[data-test^='add-to-cart']"
    SELECTOR_LINK_SHOPPING_CART = ".shopping_cart_link"
    SELECTOR_TEXT_PAGE_TITLE = ".title"
    EXPECTED_TITLE_TEXT = "Products"

    # '검증'의 목적을 명확히 하는 네이밍
    def verify_inventory_page_is_fully_loaded(self):
        """로그인 후 상품 목록 페이지가 완전히 렌더링되었는지 검증합니다."""
        expected_inventory_url = f"{URL_WEB_BASE}{self.PATH_INVENTORY}"
        self.verify_current_url(expected_inventory_url)
        
        # 핵심 UI 요소(타이틀)가 렌더링되었는지 타임아웃 매개변수를 사용하여 확인
        page_title_element = self.page.locator(self.SELECTOR_TEXT_PAGE_TITLE)
        expect(page_title_element).to_be_visible(timeout=TIMEOUT_ELEMENT_WAIT)
        expect(page_title_element).to_have_text(self.EXPECTED_TITLE_TEXT)

    def add_first_available_item_to_cart(self):
        """목록에 있는 첫 번째 상품을 장바구니에 담습니다."""
        first_item_add_button = self.page.locator(self.SELECTOR_BUTTON_ADD_TO_CART).first
        first_item_add_button.click()

    def navigate_to_shopping_cart(self):
        """우측 상단의 장바구니 아이콘을 클릭하여 장바구니 페이지로 이동합니다."""
        shopping_cart_link_icon = self.page.locator(self.SELECTOR_LINK_SHOPPING_CART)
        shopping_cart_link_icon.click()