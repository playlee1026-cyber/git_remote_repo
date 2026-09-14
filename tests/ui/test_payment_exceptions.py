import pytest
from playwright.sync_api import Page, Route, expect
from config.settings import Config


def mock_aml_limit_exceeded_response(route: Route) -> None:
    """
    [네트워크 인터셉터 핸들러]
    실제 백엔드 서버로 요청을 보내지 않고, API 요청을 가로채어 
    중앙 관리되는 AML 한도 초과 에러(403) 데이터를 강제로 반환합니다.
    """
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )


def test_verify_aml_limit_error_handling_on_checkout(page: Page) -> None:
    """
    [결제 실패 예외 처리 시나리오] 
    결제 진행 중 백엔드 API에서 AML 규제 위반 에러가 발생했을 때,
    프론트엔드 UI가 사용자에게 해당 에러 메시지를 정확히 렌더링하는지 검증합니다.
    """
    
    # 1. 중앙 환경 설정(Config)에서 테스트에 필요한 파라미터 로드
    checkout_page_url = Config.PAGE_URL_CHECKOUT_STEP
    target_api_pattern = Config.MOCK_PAYMENT_API_PATTERN
    submit_payment_button = Config.SELECTOR_BUTTON_SUBMIT_PAYMENT
    error_message_element = Config.SELECTOR_TEXT_ERROR_MESSAGE
    expected_error_text = Config.EXPECTED_UI_AML_ERROR_TEXT

    # 2. 사전 조건: 결제 최종 확인 페이지로 이동
    page.goto(checkout_page_url)

    # 3. 네트워크 인터셉트 시작: 타겟 API 패턴 발견 시 'mock_aml_limit_exceeded_response' 함수 실행
    page.route(target_api_pattern, mock_aml_limit_exceeded_response)

    # 4. 테스트 액션: 결제 요청 버튼 클릭 (이때 실제 서버 대신 모킹된 403 에러가 프론트엔드로 전달됨)
    page.locator(submit_payment_button).click()

    # 5. 기대 결과 검증: 프론트엔드가 403 에러 코드를 파싱하여 화면에 올바른 에러 토스트/알럿을 띄우는지 확인
    ui_error_alert = page.locator(error_message_element)
    
    expect(ui_error_alert).to_be_visible()
    expect(ui_error_alert).to_have_text(expected_error_text)