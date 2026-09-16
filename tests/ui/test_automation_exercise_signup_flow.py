import pytest
from config.settings import AUTOMATION_EXERCISE_BASE_URL
from pages.automation_exercise.home_page import AutomationExerciseHomePage
from pages.automation_exercise.login_signup_page import AutomationExerciseLoginSignupPage

# 🌟 하드코딩 배제: 테스트 케이스 파라미터화를 위한 데이터 분리
# (동치 분할 검증을 위해 User A, User B 등의 독립적인 페르소나 사용)
VALID_SIGNUP_TEST_DATA = [
    ("User A", "user.a.test.qa@automation.example.com"),
    ("User B", "user.b.test.qa@automation.example.com")
]

@pytest.mark.ui
@pytest.mark.signup
@pytest.mark.parametrize("target_user_name, target_user_email", VALID_SIGNUP_TEST_DATA)
def test_new_user_can_proceed_to_account_information_form(
    ae_home_page: AutomationExerciseHomePage, 
    ae_login_signup_page: AutomationExerciseLoginSignupPage,
    target_user_name: str,
    target_user_email: str
):
    """
    유효한 신규 사용자가 이름과 이메일을 입력했을 때,
    상세 계정 정보 입력 폼으로 정상적으로 전환되는지 검증합니다.
    """
    
    # 1. Arrange: 테스트 타겟 URL 진입
    ae_home_page.navigate_to_home(AUTOMATION_EXERCISE_BASE_URL)
    ae_home_page.click_signup_login_menu()
    
    # 2. Act: 주입받은 파라미터를 활용한 액션 수행
    ae_login_signup_page.initiate_signup_process(
        target_user_name=target_user_name, 
        target_user_email=target_user_email
    )
    
    # 3. Assert: 상태 기반 렌더링 검증 (견고한 대기)
    ae_login_signup_page.verify_account_information_form_is_visible()