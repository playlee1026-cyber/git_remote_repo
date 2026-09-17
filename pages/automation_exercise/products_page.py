# pages/automation_exercise/products_page.py
from playwright.sync_api import Page, expect

class AutomationExerciseProductsPage:
    # 매직 스트링 배제: 정적 로케이터
    ALL_PRODUCTS_HEADER_LOCATOR = "h2:has-text('All Products')"
    SEARCH_PRODUCT_INPUT_LOCATOR = "input#search_product"
    SEARCH_SUBMIT_BUTTON_LOCATOR = "button#submit_search"
    SEARCHED_PRODUCTS_HEADER_LOCATOR = "h2:has-text('Searched Products')"
    CONTINUE_SHOPPING_MODAL_BUTTON_LOCATOR = "button:has-text('Continue Shopping')"
    VIEW_CART_MODAL_LINK_LOCATOR = "a[href='/view_cart'] > u"
    # 검색 결과 화면에 테스트 목적(장바구니 담기)에 부합 로케이터 
    SPECIFIC_PRODUCT_NAME_IN_SEARCH_RESULT_TEMPLATE = "div.productinfo p:text-is('{target_name}')"
    # --- [신규 추가: 매직 스트링 배제용 상태 상수] ---
    NETWORK_IDLE_STATE_INDICATOR = "networkidle"
    
    # 동적 로케이터 템플릿 (파라미터 주입용)
    SPECIFIC_PRODUCT_CARD_TEMPLATE = "div.product-image-wrapper:has(p:text-is('{target_name}'))"
    ADD_TO_CART_BUTTON_INSIDE_CARD_LOCATOR = "a.add-to-cart"
    PRODUCT_NAME_IN_SEARCH_RESULT_LOCATOR = "div.productinfo p"

    def __init__(self, page: Page):
        self.page = page

    def verify_all_products_page_is_visible(self) -> None:
        expect(self.page.locator(self.ALL_PRODUCTS_HEADER_LOCATOR)).to_be_visible()

    def execute_product_search(self, target_product_name: str) -> None:
        """
        검색창에 타겟 상품명을 입력하고 검색 버튼을 클릭한 뒤,
        새로운 결과가 렌더링되도록 네트워크 통신이 완전히 종료(Idle)될 때까지 명시적으로 대기합니다.
        """
        self.page.fill(self.SEARCH_PRODUCT_INPUT_LOCATOR, target_product_name)
        self.page.click(self.SEARCH_SUBMIT_BUTTON_LOCATOR)
        
        # 초고속 실행(PWDEBUG=0) 시 Race Condition 방지를 위한 상태 동기화
        self.page.wait_for_load_state(self.NETWORK_IDLE_STATE_INDICATOR)

    def verify_searched_products_header_is_visible(self) -> None:
        expect(self.page.locator(self.SEARCHED_PRODUCTS_HEADER_LOCATOR)).to_be_visible()

    def verify_specific_target_products_are_visible_in_search_results(self, expected_product_names: list) -> None:
            """
            검색 결과 화면에 테스트 목적(장바구니 담기)에 부합하는 타겟 상품들이 정상적으로 노출되었는지 콕 집어서 검증합니다.
            """
            for product_name in expected_product_names:
                target_product_locator_string = self.SPECIFIC_PRODUCT_NAME_IN_SEARCH_RESULT_TEMPLATE.format(target_name=product_name)
                expect(self.page.locator(target_product_locator_string)).to_be_visible()

    def hover_and_add_target_product_to_cart(self, product_name: str) -> None:
        """특정 상품 카드를 찾아 마우스를 올린 후, 장바구니 추가 버튼을 클릭합니다."""
        target_card_locator_string = self.SPECIFIC_PRODUCT_CARD_TEMPLATE.format(target_name=product_name)
        target_product_card = self.page.locator(target_card_locator_string).first
        
        target_product_card.hover()
        # 카드 내부의 'Add to cart' 버튼 찾아서 클릭
        target_product_card.locator(self.ADD_TO_CART_BUTTON_INSIDE_CARD_LOCATOR).first.click()

    def click_continue_shopping_button_on_modal(self) -> None:
        self.page.click(self.CONTINUE_SHOPPING_MODAL_BUTTON_LOCATOR)

    def click_view_cart_link_on_modal(self) -> None:
        self.page.click(self.VIEW_CART_MODAL_LINK_LOCATOR)