# pages/automation_exercise/cart_page.py
from playwright.sync_api import Page, expect

class AutomationExerciseCartPage:
    # 동적 로케이터 템플릿
    CART_ITEM_ROW_TEMPLATE = "tr:has(a[href*='/product_details/']:text-is('{target_name}'))"
    CART_ITEM_PRICE_LOCATOR = "td.cart_price p"
    CART_ITEM_QUANTITY_LOCATOR = "td.cart_quantity button"
    CART_ITEM_TOTAL_PRICE_LOCATOR = "td.cart_total p"
    # --- [매직 스트링 배제 로케이터 상수] ---
    CART_PAGE_INDICATOR_LOCATOR = "li.active:has-text('Shopping Cart')"
    PROCEED_TO_CHECKOUT_BUTTON_LOCATOR = "a.check_out:has-text('Proceed To Checkout')"

    def __init__(self, page: Page):
        self.page = page

    def verify_specific_products_exist_in_cart(self, expected_product_names: list) -> None:
        for product_name in expected_product_names:
            target_row_locator_string = self.CART_ITEM_ROW_TEMPLATE.format(target_name=product_name)
            expect(self.page.locator(target_row_locator_string)).to_be_visible()

    def verify_cart_items_pricing_and_quantity(self, expected_details: list) -> None:
        """파라미터로 주입된 상세 데이터(가격, 수량, 총액)와 UI 상의 데이터를 교차 검증합니다."""
        for item_data in expected_details:
            target_row_locator_string = self.CART_ITEM_ROW_TEMPLATE.format(target_name=item_data["product_name"])
            target_row = self.page.locator(target_row_locator_string)
            
            expect(target_row.locator(self.CART_ITEM_PRICE_LOCATOR)).to_have_text(item_data["price"])
            expect(target_row.locator(self.CART_ITEM_QUANTITY_LOCATOR)).to_have_text(item_data["quantity"])
            expect(target_row.locator(self.CART_ITEM_TOTAL_PRICE_LOCATOR)).to_have_text(item_data["total_price"])

    def verify_cart_page_is_visible(self) -> None:
            """
            장바구니 페이지에 정상적으로 진입했음을 알리는 고유 UI 요소(브레드크럼 등)가 
            화면에 노출되었는지 검증합니다.
            """
            expect(self.page.locator(self.CART_PAGE_INDICATOR_LOCATOR)).to_be_visible()

    def click_proceed_to_checkout_button(self) -> None:
        """
        장바구니 내역 확인 후 결제 단계로 넘어가는 'Proceed To Checkout' 버튼을 클릭합니다.
        """
        self.page.click(self.PROCEED_TO_CHECKOUT_BUTTON_LOCATOR)