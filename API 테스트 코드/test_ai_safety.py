import pytest
import pandas as pd
import requests
import json

# 테스트 대상 서버의 기본 URL (실제 환경에 맞게 수정)
BASE_URL = "https://git-remote-repo.onrender.com"

# CSV 파일을 읽어 pytest에서 사용할 수 있는 딕셔너리 리스트로 변환하는 헬퍼 함수
def load_test_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    return df.to_dict(orient='records')

# 도메인별 테스트 데이터 로드
signup_data = load_test_data('signup_api_test.csv')
payment_data = load_test_data('payment_api_test.csv')
board_data = load_test_data('board_api_test.csv')

class TestBusinessAPI:
    
    @pytest.mark.parametrize("test_case", signup_data, ids=[tc["Test_Case_ID"] for tc in signup_data])
    def test_signup_api(self, test_case):
        self._execute_and_verify(test_case)

    @pytest.mark.parametrize("test_case", payment_data, ids=[tc["Test_Case_ID"] for tc in payment_data])
    def test_payment_api(self, test_case):
        self._execute_and_verify(test_case)

    @pytest.mark.parametrize("test_case", board_data, ids=[tc["Test_Case_ID"] for tc in board_data])
    def test_board_api(self, test_case):
        self._execute_and_verify(test_case)

    # API 요청 및 결과 검증을 수행하는 공통 메서드
    def _execute_and_verify(self, test_case):
        url = f"{BASE_URL}{test_case['Endpoint']}"
        method = test_case['Method']
        
        # 문자열로 저장된 JSON 페이로드를 파이썬 딕셔너리로 변환
        payload = json.loads(test_case['Request_Payload']) if pd.notna(test_case['Request_Payload']) else {}
        expected_status = int(test_case['Expected_Status_Code'])

        # HTTP 메서드에 따른 API 요청 실행
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            timeout=5 # Flaky test 방지를 위한 명시적 타임아웃 설정
        )

        # 상태 코드 검증
        assert response.status_code == expected_status, \
            f"[{test_case['Test_Case_ID']}] {test_case['Description']} - 실패: 예상 상태 코드 {expected_status}, 실제 응답 {response.status_code}"