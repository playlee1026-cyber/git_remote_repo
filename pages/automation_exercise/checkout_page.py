from playwright.sync_api import Page, expect

class AutomationExerciseCheckoutPage:
    ADDRESS_DELIVERY_SECTION_LOCATOR = "ul#address_delivery"
    ORDER_REVIEW_SECTION_LOCATOR = "div#cart_info"
    ORDER_COMMENT_TEXTAREA_LOCATOR = "textarea[name='message']"
    PLACE_ORDER_BUTTON_LOCATOR = "a[href='/payment']"

    def __init__(self, page: Page):
        self.page = page

    def verify_address_details_are_visible(self) -> None:
        expect(self.page.locator(self.ADDRESS_DELIVERY_SECTION_LOCATOR)).to_be_visible()
        
    def verify_order_review_is_visible(self) -> None:
        expect(self.page.locator(self.ORDER_REVIEW_SECTION_LOCATOR)).to_be_visible()
        
    def enter_order_comment_and_place_order(self, comment_text: str) -> None:
        self.page.fill(self.ORDER_COMMENT_TEXTAREA_LOCATOR, comment_text)
        self.page.click(self.PLACE_ORDER_BUTTON_LOCATOR)