# pages/automation_exercise/cart_page.py
from playwright.sync_api import Page, expect

class AutomationExerciseCartPage:
    # 동적 로케이터 템플릿
    CART_ITEM_ROW_TEMPLATE = "tr:has(a[href*='/product_details/']:text-is('{target_name}'))"
    CART_ITEM_PRICE_LOCATOR = "td.cart_price p"
    CART_ITEM_QUANTITY_LOCATOR = "td.cart_quantity button"
    CART_ITEM_TOTAL_PRICE_LOCATOR = "td.cart_total p"

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