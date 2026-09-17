import uuid

# 여러 테스트에서 반복적으로 사용되는 공통 비즈니스 로직을 보관함

# 매직 스트링 배제를 위한 글로벌 상수 선언
TEST_EMAIL_PREFIX = "qa_tester_"
TEST_EMAIL_DOMAIN = "@example.com"
ACCOUNT_CREATED_MESSAGE = "ACCOUNT CREATED!"
ACCOUNT_DELETED_MESSAGE = "ACCOUNT DELETED!"

def generate_unique_test_email() -> str:
    """병렬 테스트 환경에서도 충돌하지 않도록 UUID 기반의 고유한 테스트 이메일을 생성합니다."""
    unique_identifier = uuid.uuid4().hex[:8]
    return f"{TEST_EMAIL_PREFIX}{unique_identifier}{TEST_EMAIL_DOMAIN}"

def execute_complete_account_setup_flow(
    home_page, 
    login_signup_page, 
    signup_details_page, 
    system_message_page, 
    user_account_data: dict
) -> None:
    """
    페이지 객체들과 완전한 형태의 사용자 데이터 딕셔너리를 주입받아 신규 계정 생성 전체 흐름을 수행합니다.
    """
    home_page.click_signup_login_menu()
    
    # 딕셔너리에서 이름과 이메일을 추출하여 초기 가입 진행
    login_signup_page.initiate_signup_process(
        target_user_name=user_account_data["name"],
        target_user_email=user_account_data["email"]
    )
    
    # 누락된 키 없이 완전한 데이터(title 포함)를 넘겨주어 KeyError 방지
    signup_details_page.verify_account_information_form_is_visible()
    signup_details_page.fill_account_details_and_submit(user_data=user_account_data)
    
    system_message_page.verify_message_is_visible(ACCOUNT_CREATED_MESSAGE)
    system_message_page.click_continue_button()

def execute_complete_account_teardown_flow(home_page, system_message_page) -> None:
    """로그인된 상태에서 계정을 삭제하고 초기화하는 전체 흐름을 수행합니다."""
    home_page.click_delete_account_menu()
    system_message_page.verify_message_is_visible(ACCOUNT_DELETED_MESSAGE)
    system_message_page.click_continue_button()