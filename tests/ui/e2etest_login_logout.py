import pytest
from helpers.account_helper import (
    generate_unique_test_email,
    execute_complete_account_setup_flow,
    execute_complete_account_teardown_flow
)
from config.settings import AUTOMATION_EXERCISE_BASE_URL, E2E_DEFAULT_TEST_PASSWORD
# KeyError 방지를 위해 검증된 데이터 스키마 임포트
from data.automation_exercise_test_data import VALID_REGISTRATION_DATA_USER_A 

@pytest.mark.ui
@pytest.mark.login
def test_user_login_and_logout_lifecycle(
    ae_home_page, 
    ae_login_signup_page, 
    ae_signup_details_page,
    ae_system_message_page
):
    """
    Test Case 2 & 4: 신규 계정 생성 후 로그아웃, 그리고 올바른 자격 증명으로 로그인 후 계정 삭제까지의 흐름을 검증
    """
    # 1. 테스트 데이터 준비: 정적 데이터를 복사하여 고유 이메일과 공통 패스워드 주입
    dynamic_user_account_data = VALID_REGISTRATION_DATA_USER_A.copy()
    unique_user_email = generate_unique_test_email()
    
    dynamic_user_account_data["email"] = unique_user_email
    dynamic_user_account_data["password"] = E2E_DEFAULT_TEST_PASSWORD
    
    # 2. 전제 조건: 애플리케이션 진입 및 테스트용 신규 계정 셋업
    ae_home_page.navigate_to_home(AUTOMATION_EXERCISE_BASE_URL)
    execute_complete_account_setup_flow(
        home_page=ae_home_page,
        login_signup_page=ae_login_signup_page,
        signup_details_page=ae_signup_details_page,
        system_message_page=ae_system_message_page,
        user_account_data=dynamic_user_account_data
    )
    
    # 3. Action (TC4 사전 준비): 자동 로그인된 상태 해제를 위한 로그아웃 실행
    ae_home_page.click_logout_menu_button()
    
    # 4. Verification (TC4 검증): 정상적으로 로그아웃되어 로그인 폼이 노출되는지 확인
    ae_login_signup_page.verify_login_form_is_visible()
    
    # 5. Action (TC2 실행): 생성했던 유효한 계정 정보로 다시 로그인
    ae_login_signup_page.execute_login_with_credentials(
        target_email=unique_user_email,
        target_password=E2E_DEFAULT_TEST_PASSWORD
    )
    
    # 6. Verification (TC2 검증): 정상 로그인 완료 상태(사용자명 노출) 확인
    ae_home_page.verify_user_is_logged_in()
    
    # 7. Post-condition: 테스트 종료 후 계정 삭제 처리 (환경 정리)
    execute_complete_account_teardown_flow(
        home_page=ae_home_page,
        system_message_page=ae_system_message_page
    )