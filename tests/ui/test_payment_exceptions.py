import pytest
from playwright.sync_api import Page, Route
from config.settings import Config, CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

# 모킹 핸들러는 유틸리티 성격이므로 테스트 스크립트 상단 또는 별도 utils 파일에 유지
def mock_aml_limit_exceeded_response(route: Route) -> None:
    """AML 한도 초과 에러(403) 데이터를 강제로 반환하는 네트워크 인터셉터 핸들러"""
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )

def test_verify_aml_limit_error_handling_on_checkout(page: Page) -> None:
    """
    의도: 로그인 후 결제 진행 중 AML 규제 위반 에러 발생 시, 
    프론트엔드 UI가 해당 에러 메시지를 올바르게 렌더링하는지 검증합니다.
    """
    # 1. 페이지 객체 인스턴스화
    login_page = LoginPage(page)
    checkout_page = CheckoutPage(page)

    # 2. 사전 조건: 로그인 페이지 접속 및 사용자 인증 (캡슐화된 POM 사용, 하드코딩 제거)
    login_page.open_login_page()
    login_page.authenticate_user(CREDENTIAL_NORMAL_USER_ID, CREDENTIAL_NORMAL_USER_PASSWORD)

    # 3. 테스트 환경 세팅: 결제 페이지 진입 및 AML 에러 네트워크 인터셉트 적용
    checkout_page.open_checkout_final_step_page()
    checkout_page.setup_aml_limit_exceeded_network_interception(mock_aml_limit_exceeded_response)

    # 4. 테스트 액션: 결제 요청 제출
    checkout_page.submit_payment_information()

    # 5. 기대 결과 검증: 지정된 AML 에러 알럿 렌더링 확인
    checkout_page.verify_aml_compliance_error_alert_is_displayed(Config.EXPECTED_UI_AML_ERROR_TEXT)