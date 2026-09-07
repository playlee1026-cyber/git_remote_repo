import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://git-remote-repo.onrender.com"

def test_unauthorized_access_to_admin_page(page: Page):
    """
    [TC-SEC-01] 일반 사용자 계정의 관리자 페이지 접근 통제 검증
    - ISO/IEC 25010 품질 특성: 보안성 (Security) - 기밀성 및 권한 통제
    - 목적: 일반 권한의 세션으로 URL을 직접 조작하여 관리자 페이지 접근 시도시,
            프론트엔드 라우터가 이를 차단하고 적절한 예외 처리를 수행하는지 확인.
    """
    # 1. 로그인 페이지 이동 및 네트워크 안정화 대기 (중복 코드 제거)
    page.goto(f"{BASE_URL}/login", wait_until="networkidle")
    
    # 명시적 대기: 입력 필드가 화면에 렌더링되어 조작 가능한 상태인지 확인
    username_input = page.get_by_placeholder("아이디")
    expect(username_input).to_be_visible(timeout=10000)
    username_input.fill("normal_user")
    
    page.get_by_placeholder("비밀번호").fill("test_password123!")
    page.get_by_role("button", name="로그인").click()
    
    # 로그인 성공 및 대시보드 진입 대기 (URL 변경 및 DOM 요소 렌더링 동시 확인)
    expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=15000)
    expect(page.get_by_role("heading", name="보안 대시보드")).to_be_visible()

    # 2. 취약점 시나리오 시도: URL 강제 조작을 통한 관리자 페이지 접근 (DOM 로드 상태 대기)
    page.goto(f"{BASE_URL}/admin/settings", wait_until="domcontentloaded")

    # 3. 결과 검증 (백엔드 403 Forbidden 방어 로직 확인)
    expect(page).to_have_url(f"{BASE_URL}/admin/settings")
    
    # 검증 B: 차단 메시지가 DOM에 완전히 렌더링되었는지 명시적 대기 및 확인
    error_toast = page.get_by_text("관리자 권한이 없습니다.")
    expect(error_toast).to_be_visible(timeout=10000)
    
    # 검증 C: 화면에 민감한 설정 버튼이 노출되지 않았는지 교차 확인
    admin_save_button = page.get_by_role("button", name="시스템 설정 저장")
    expect(admin_save_button).not_to_be_visible()