import pytest
from config.settings import AUTOMATION_EXERCISE_BASE_URL
# 하드코딩 배제를 위한 통합 테스트 데이터 딕셔너리 임포트 (가정)
from data.product_test_data import SEARCH_AND_CART_TEST_DATA

@pytest.mark.ui
@pytest.mark.products
@pytest.mark.parametrize("shopping_data", [SEARCH_AND_CART_TEST_DATA])
def test_product_search_and_cart_checkout_flow(
    ae_home_page,
    ae_products_page,
    ae_cart_page,
    shopping_data: dict
):
    """
    Test Case 9 & 12 통합 시나리오:
    사용자가 홈페이지에서 Products 메뉴로 진입 후, 특정 상품을 검색(TC9)하고
    검색된 상품들을 장바구니에 담은 뒤, 장바구니 페이지에서 최종 내역을 검증(TC12)합니다.
    """
    
    # 1. 전제 조건: 홈페이지 접속 및 상태 검증 (TC9, TC12 Step 1-3)
    ae_home_page.navigate_to_home(AUTOMATION_EXERCISE_BASE_URL)
    ae_home_page.verify_home_page_is_visible()

    # 2. Action & Verification: Products 페이지 이동 (TC9, TC12 Step 4-5)
    ae_home_page.click_products_menu_button()
    ae_products_page.verify_all_products_page_is_visible()

    # 3. Action & Verification (TC9): 상품 검색 및 검색 결과 확인
    target_search_keyword = shopping_data["search_keyword"]
    ae_products_page.execute_product_search(target_product_name=target_search_keyword)
    
    ae_products_page.verify_searched_products_header_is_visible()
    
    # [수정된 호출부] 딕셔너리에서 타겟 상품명만 리스트로 묶어 파라미터화(Parameterization) 주입
    target_products_to_verify = [
        shopping_data["first_product_name"],
        shopping_data["second_product_name"]
    ]
    ae_products_page.verify_specific_target_products_are_visible_in_search_results(
        expected_product_names=target_products_to_verify
    )

    # 4. Action (TC12): 첫 번째 대상 상품 마우스 오버 및 장바구니 추가
    first_target_product = shopping_data["first_product_name"]
    ae_products_page.hover_and_add_target_product_to_cart(product_name=first_target_product)
    ae_products_page.click_continue_shopping_button_on_modal()

    # 5. Action (TC12): 두 번째 대상 상품 마우스 오버 및 장바구니 추가
    second_target_product = shopping_data["second_product_name"]
    ae_products_page.hover_and_add_target_product_to_cart(product_name=second_target_product)
    
    # 6. Action (TC12): 모달창에서 장바구니 보기(View Cart) 클릭하여 이동
    ae_products_page.click_view_cart_link_on_modal()

    # 7. Verification (TC12): 장바구니에 두 상품이 정상적으로 담겼는지, 가격/수량/총액이 맞는지 검증
    ae_cart_page.verify_specific_products_exist_in_cart(
        expected_product_names=[first_target_product, second_target_product]
    )
    ae_cart_page.verify_cart_items_pricing_and_quantity(
        expected_details=shopping_data["expected_cart_details"]
    )