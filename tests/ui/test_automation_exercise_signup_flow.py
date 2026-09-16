import pytest
from config.settings import AUTOMATION_EXERCISE_BASE_URL
from data.automation_exercise_test_data import VALID_REGISTRATION_DATA_USER_A

@pytest.mark.ui
@pytest.mark.registration
@pytest.mark.parametrize("registration_data", [VALID_REGISTRATION_DATA_USER_A])
def test_user_registration_and_deletion_lifecycle(
    ae_home_page, 
    ae_login_signup_page, 
    ae_signup_details_page, 
    ae_system_message_page,
    registration_data: dict
):
    """
    Test Case 1: Register User
    신규 사용자 가입부터 생성 확인, 로그인 상태 검증, 그리고 계정 삭제까지의 전체 라이프사이클을 검증합니다.
    """
    
    # Steps 1-3: 브라우저 실행 및 홈페이지 진입 검증
    ae_home_page.navigate_to_home(AUTOMATION_EXERCISE_BASE_URL)
    ae_home_page.verify_home_page_is_visible()
    
    # Steps 4-5: 회원가입 화면 진입
    ae_home_page.click_signup_login_menu()
    ae_login_signup_page.verify_new_user_signup_is_visible()
    
    # Steps 6-7: 초기 이름/이메일 입력 후 진행
    ae_login_signup_page.initiate_signup_process(
        target_user_name=registration_data["name"],
        target_user_email=registration_data["email"]
    )
    
    # Steps 8-13: 상세 계정 정보 폼 검증 및 데이터 입력 후 계정 생성
    ae_signup_details_page.verify_account_information_form_is_visible()
    ae_signup_details_page.fill_account_details_and_submit(user_data=registration_data)
    
    # Steps 14-15: 계정 생성 성공 메시지 검증 및 계속 진행
    ae_system_message_page.verify_message_is_visible("ACCOUNT CREATED!")
    ae_system_message_page.click_continue_button()
    
    # Step 16: 로그인 상태 유지 검증
    ae_home_page.verify_logged_in_as_username(expected_username=registration_data["name"])
    
    # Steps 17-18: 계정 삭제 액션 및 삭제 성공 메시지 검증
    ae_home_page.click_delete_account_menu()
    ae_system_message_page.verify_message_is_visible("ACCOUNT DELETED!")
    ae_system_message_page.click_continue_button()