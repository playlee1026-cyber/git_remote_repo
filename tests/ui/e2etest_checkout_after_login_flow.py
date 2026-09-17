import pytest
from helpers.account_helper import (
    generate_unique_test_email,
    execute_complete_account_setup_flow,
    execute_complete_account_teardown_flow
)
from config.settings import AUTOMATION_EXERCISE_BASE_URL, E2E_DEFAULT_TEST_PASSWORD
from data.automation_exercise_test_data import VALID_REGISTRATION_DATA_USER_A 
from data.checkout_test_data import CHECKOUT_FLOW_TEST_DATA

@pytest.mark.ui
@pytest.mark.checkout
@pytest.mark.parametrize("checkout_data", [CHECKOUT_FLOW_TEST_DATA])
def test_place_order_login_before_checkout_lifecycle(
    ae_home_page, 
    ae_login_signup_page, 
    ae_signup_details_page,
    ae_system_message_page,
    ae_products_page,
    ae_cart_page,
    ae_checkout_page,
    ae_payment_page,
    checkout_data: dict
):
    """
    Test Case 16: Place Order: Login before Checkout
    결제 전 로그인을 수행하고, 장바구니에 상품을 담아 최종 결제 완료 및 계정 삭제까지 진행하는 흐름을 검증합니다.
    """
    
    # --- [Setup] 테스트 데이터 동적 생성 및 사전 계정 셋업 ---
    dynamic_user_account_data = VALID_REGISTRATION_DATA_USER_A.copy()
    unique_user_email = generate_unique_test_email()
    dynamic_user_account_data["email"] = unique_user_email
    dynamic_user_account_data["password"] = E2E_DEFAULT_TEST_PASSWORD
    
    # Step 1-6 (TC16 요구사항 충족을 위한 사전 환경 구성: 가입 및 자동 로그인 상태 획득)
    ae_home_page.navigate_to_home(AUTOMATION_EXERCISE_BASE_URL)
    execute_complete_account_setup_flow(
        home_page=ae_home_page,
        login_signup_page=ae_login_signup_page,
        signup_details_page=ae_signup_details_page,
        system_message_page=ae_system_message_page,
        user_account_data=dynamic_user_account_data
    )
    ae_home_page.verify_user_is_logged_in()
    
    # --- [Action & Verification] 메인 주문 흐름 시작 ---
    
    # Step 7: 상품 페이지로 이동하여 타겟 상품을 장바구니에 추가
    ae_home_page.click_products_menu_button()
    ae_products_page.hover_and_add_target_product_to_cart(
        product_name=checkout_data["target_product_name"]
    )
    ae_products_page.click_view_cart_link_on_modal()
    
    # Step 8-9: 장바구니 페이지 노출 검증
    ae_cart_page.verify_cart_page_is_visible()
    
    # Step 10: 결제 진행 버튼 클릭
    ae_cart_page.click_proceed_to_checkout_button()
    
    # Step 11: 주소 정보 및 주문 내역 노출 검증
    ae_checkout_page.verify_address_details_are_visible()
    ae_checkout_page.verify_order_review_is_visible()
    
    # Step 12: 주문 코멘트 입력 및 주문 버튼 클릭
    ae_checkout_page.enter_order_comment_and_place_order(
        comment_text=checkout_data["order_comment"]
    )
    
    # Step 13-14: 결제 정보 입력 및 결제 확인
    ae_payment_page.enter_payment_details_and_confirm(
        payment_data=checkout_data["payment_details"]
    )
    
    # Step 15: 주문 성공 메세지 검증
    ae_system_message_page.verify_message_is_visible("ORDER PLACED!")
    
    # --- [Teardown] 환경 정리 ---
    
    # Step 16-17: 테스트 계정 삭제 및 확인
    execute_complete_account_teardown_flow(
        home_page=ae_home_page,
        system_message_page=ae_system_message_page
    )