import pytest
from playwright.sync_api import Page, Route
from config.settings import Config, CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD

# 시나리오 흐름에 필요한 모든 페이지 객체 임포트
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_page import CheckoutPage

# 모킹 핸들러: 테스트 스크립트 상단 또는 별도 utils 파일에 유지
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
    의도: 정상적인 구매 흐름(로그인 -> 대시보드 -> 상품 담기 -> 결제) 중 
    AML 규제 위반 에러가 발생했을 때, UI가 에러 메시지를 올바르게 렌더링하는지 검증합니다.
    """
    # 1. 시나리오에 필요한 모든 페이지 객체 인스턴스화
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_step_one_page = CheckoutStepOnePage(page)
    checkout_page = CheckoutPage(page)

    # 2. 사전 조건 1: 로그인 페이지 접속 및 인증 시도
    login_page.open_login_page()
    login_page.authenticate_user(CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD)

    # 3. 사전 조건 2 (에러 해결 지점): 로그인 완료 후 대시보드 진입 대기 및 상점 이동
    # 대시보드가 완전히 로딩될 때까지 기다림으로써 Race Condition(URL 불일치) 원천 차단
    dashboard_page.verify_security_dashboard_is_fully_loaded()
    
    # 💡 주의: dashboard_page.py 내부에 대시보드에서 상점(Inventory)으로 
    # 이동하는 클릭 이벤트를 구현한 아래 메서드가 추가되어야 합니다.
    dashboard_page.navigate_to_product_inventory()

    # 4. 비즈니스 흐름 1: 상점 진입 확인 및 장바구니에 상품 담기
    inventory_page.verify_inventory_page_is_fully_loaded()
    inventory_page.add_first_available_item_to_cart()
    inventory_page.navigate_to_shopping_cart()

    # 5. 비즈니스 흐름 2: 장바구니 확인 및 배송지 정보 입력 단계로 이동
    cart_page.verify_shopping_cart_page_is_loaded()
    cart_page.proceed_to_checkout_step_one()

    # 6. 비즈니스 흐름 3: 배송지 정보 입력 (중앙 환경 변수에서 더미 데이터 주입)
    checkout_step_one_page.verify_checkout_step_one_is_loaded()
    checkout_step_one_page.submit_shipping_information(
        first_name=Config.DUMMY_SHIPPING_FIRST_NAME,
        last_name=Config.DUMMY_SHIPPING_LAST_NAME,
        postal_code=Config.DUMMY_SHIPPING_POSTAL_CODE
    )

    # 7. 결제 환경 세팅: 최종 결제 단계 진입 확인 및 403 에러 네트워크 인터셉트 시작
    checkout_page.verify_checkout_final_step_is_loaded()
    checkout_page.setup_aml_limit_exceeded_network_interception(mock_aml_limit_exceeded_response)

    # 8. 테스트 액션 및 검증: 결제 요청 제출 후 AML 규제 위반 알럿 확인
    checkout_page.submit_payment_information()
    checkout_page.verify_aml_compliance_error_alert_is_displayed(Config.EXPECTED_UI_AML_ERROR_TEXT)