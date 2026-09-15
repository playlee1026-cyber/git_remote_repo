import pytest
from playwright.sync_api import Page, Route
from config.settings import Config, CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD

# 새롭게 설계된 비즈니스 흐름(User Flow)을 위한 페이지 객체들 임포트
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_page import CheckoutPage


# 모킹 핸들러: 유틸리티 성격이므로 상단에 유지
def mock_aml_limit_exceeded_response(route: Route) -> None:
    """AML 한도 초과 에러(403) 데이터를 강제로 반환하는 네트워크 인터셉터 핸들러"""
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )

@pytest.mark.ui
@pytest.mark.payment
def test_verify_aml_limit_error_handling_on_checkout(page: Page) -> None:
    """
    의도: 정상적인 구매 흐름(상품 담기 -> 배송지 입력 -> 결제)을 거쳐 최종 결제를 진행할 때,
    AML 규제 위반 에러가 발생하면 UI가 해당 에러 메시지를 올바르게 렌더링하는지 검증합니다.
    """
    # 1. 시나리오에 필요한 모든 페이지 객체 인스턴스화
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_step_one_page = CheckoutStepOnePage(page)
    checkout_page = CheckoutPage(page)  # 결제 최종 단계(Step Two)

    # 2. 사전 조건: 로그인 페이지 접속 및 사용자 인증
    login_page.open_login_page()
    login_page.authenticate_user(CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD)

    # 3. 비즈니스 흐름 1: 로그인 직후 상품 목록 로딩 대기 및 장바구니에 상품 담기
    # (Race Condition 방지: 로그인이 완전히 끝날 때까지 기다립니다)
    inventory_page.verify_inventory_page_is_fully_loaded()
    inventory_page.add_first_available_item_to_cart()
    inventory_page.navigate_to_shopping_cart()

    # 4. 비즈니스 흐름 2: 장바구니 확인 및 체크아웃 1단계(배송지 정보) 진입
    cart_page.verify_shopping_cart_page_is_loaded()
    cart_page.proceed_to_checkout_step_one()

    # 5. 비즈니스 흐름 3: 배송지 정보 입력 후 최종 결제 단계로 이동
    # [클린 코드 1번 원칙] 배송지 더미 데이터 역시 하드코딩을 배제하고 Config에서 호출
    checkout_step_one_page.verify_checkout_step_one_is_loaded()
    checkout_step_one_page.submit_shipping_information(
        first_name=Config.DUMMY_SHIPPING_FIRST_NAME,
        last_name=Config.DUMMY_SHIPPING_LAST_NAME,
        postal_code=Config.DUMMY_SHIPPING_POSTAL_CODE
    )

    # 6. 테스트 환경 세팅: 강제 URL 이동(goto)을 제거하고, 자연스럽게 도달한 상태에서 인터셉트 적용
    checkout_page.verify_checkout_final_step_is_loaded()
    checkout_page.setup_aml_limit_exceeded_network_interception(mock_aml_limit_exceeded_response)

    # 7. 테스트 액션: 결제 요청 제출
    checkout_page.submit_payment_information()

    # 8. 기대 결과 검증: 지정된 AML 에러 알럿 렌더링 확인
    checkout_page.verify_aml_compliance_error_alert_is_displayed(Config.EXPECTED_UI_AML_ERROR_TEXT)