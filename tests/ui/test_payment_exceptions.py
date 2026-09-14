import pytest
from playwright.sync_api import Page, Route, expect
from config.settings import Config


def mock_aml_limit_exceeded_response(route: Route) -> None:
    """
    [네트워크 인터셉터 핸들러]
    실제 백엔드 대신, 중앙 관리되는 AML 한도 초과 에러(403) 데이터를 강제로 반환합니다.
    """
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )


def test_verify_aml_limit_error_handling_on_checkout(page: Page) -> None:
    """
    [결제 실패 예외 처리 시나리오]
    로그인 후 결제 진행 중 백엔드 API에서 AML 규제 위반 에러가 발생했을 때,
    프론트엔드 UI가 해당 에러 메시지를 사용자에게 정확히 렌더링하는지 검증합니다.
    """
    
    # 1. 로그인 필요 변수 로드
    base_url = Config.BASE_URL
    user_id = Config.TEST_USER_ID
    user_password = Config.TEST_USER_PASSWORD
    
    username_selector = Config.SELECTOR_INPUT_USERNAME
    password_selector = Config.SELECTOR_INPUT_PASSWORD
    login_button_selector = Config.SELECTOR_BUTTON_LOGIN

    # 2. AML 결제 검증 변수 로드
    checkout_page_url = Config.PAGE_URL_CHECKOUT_STEP
    target_api_pattern = Config.MOCK_PAYMENT_API_PATTERN
    submit_payment_button = Config.SELECTOR_BUTTON_SUBMIT_PAYMENT
    error_message_element = Config.SELECTOR_TEXT_ERROR_MESSAGE
    expected_error_text = Config.EXPECTED_UI_AML_ERROR_TEXT

    # 3. 사전 조건: 세션 획득을 위한 로그인 수행
    page.goto(base_url)
    page.fill(username_selector, user_id)
    page.fill(password_selector, user_password)
    page.click(login_button_selector)

    # 4. 테스트 진입: 결제 최종 페이지 이동 및 네트워크 인터셉트 시작
    page.goto(checkout_page_url)
    page.route(target_api_pattern, mock_aml_limit_exceeded_response)

    # 5. 테스트 액션: 결제 요청 (실제 서버 대신 403 에러가 프론트엔드로 전달됨)
    page.locator(submit_payment_button).click()

    # 6. 기대 결과 검증: 프론트엔드가 403 에러를 올바른 UI 알럿으로 처리하는지 확인
    ui_error_alert = page.locator(error_message_element)
    expect(ui_error_alert).to_be_visible()
    expect(ui_error_alert).to_have_text(expected_error_text)