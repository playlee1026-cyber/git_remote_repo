import pytest
from playwright.sync_api import Page, Route
from config.settings import Config
from pages.payment_checkout_page import PaymentCheckoutPage

PAYMENT_API_URL_PATTERN = "**/api/payment"
PAYMENT_SUCCESS_MESSAGE = "결제가 완료되었습니다."


def mock_aml_limit_exceeded_response(route: Route) -> None:
    """
    [네트워크 인터셉터 핸들러]
    실제 백엔드 대신, 중앙 관리되는 AML 한도 초과 에러(403) 데이터를 강제로 반환합니다.
    """
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )


@pytest.mark.ui
@pytest.mark.payment
@pytest.mark.security
def test_verify_aml_limit_error_handling_on_checkout(page: Page) -> None:
    """
    [AML 예외 처리 시나리오]
    결제 요청 중 백엔드가 AML 한도 초과(403)를 반환했을 때,
    프론트엔드가 해당 메시지를 사용자에게 정확히 보여주는지 검증합니다.
    (실제 백엔드에는 AML 로직이 없으므로 Network Interception으로 응답을 목킹)
    """
    intercepted_requests = []

    def handler(route: Route) -> None:
        intercepted_requests.append(route.request.url)
        mock_aml_limit_exceeded_response(route)

    checkout_page = PaymentCheckoutPage(page)
    checkout_page.navigate_to_checkout()

    # 클릭 '전에' 라우트를 등록해야 요청이 가로채집니다.
    page.route(PAYMENT_API_URL_PATTERN, handler)
    checkout_page.click_pay_button()

    expected_message = Config.MOCK_AML_ERROR_RESPONSE_JSON["message"]
    checkout_page.verify_payment_result_message(expected_message)

    # 목킹이 실제로 적용됐는지(= 진짜 서버 응답이 아닌지) 증명
    assert len(intercepted_requests) == 1, "결제 API 요청이 인터셉트되지 않았습니다."


@pytest.mark.ui
@pytest.mark.payment
@pytest.mark.smoke
def test_payment_success_flow_without_mock(page: Page) -> None:
    """[대조군] 목킹 없이 실제 목 서버로 결제하면 성공 메시지가 노출됩니다."""
    checkout_page = PaymentCheckoutPage(page)
    checkout_page.navigate_to_checkout()
    checkout_page.click_pay_button()
    checkout_page.verify_payment_result_message(PAYMENT_SUCCESS_MESSAGE)
