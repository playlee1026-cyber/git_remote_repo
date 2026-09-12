import pytest
import json
from config.settings import URL_API_BASE, PATH_SIGNUP_CSV, PATH_PAYMENT_CSV, PATH_BOARD_CSV
from utils.api_client import BaseAPI
from utils.data_reader import get_api_test_data

# 1. 중앙화된 환경 변수를 사용하여 BaseAPI 인스턴스 초기화
api = BaseAPI(URL_API_BASE)

# 2. utils 모듈을 활용하여 도메인별 테스트 데이터 로드
signup_data = get_api_test_data(PATH_SIGNUP_CSV)
payment_data = get_api_test_data(PATH_PAYMENT_CSV)
board_data = get_api_test_data(PATH_BOARD_CSV)

class TestBusinessAPI:
    
    # 공통 검증 메서드
    def _execute_and_verify(self, test_case):
        endpoint = test_case['Endpoint']
        method = test_case['Method']
        expected_status = int(test_case['Expected_Status_Code'])
        
        # utils.data_reader에서 빈 값을 ""로 처리했으므로 단순 조건문으로 평가 가능
        raw_payload = test_case['Request_Payload']
        payload = json.loads(raw_payload) if raw_payload else {}

        # 3. 직접 requests를 호출하지 않고 래퍼 클래스인 BaseAPI를 통해 요청 실행
        response = api.request(
            method=method,
            endpoint=endpoint,
            json=payload,
            timeout=5
        )

        # 상태 코드 검증
        assert response.status_code == expected_status, \
            f"[{test_case['Test_Case_ID']}] {test_case['Description']} - 실패: 예상 상태 {expected_status}, 실제 응답 {response.status_code}"

    # 4. PyTest 파라미터라이징 및 테스트 케이스 ID 매핑
    @pytest.mark.api
    @pytest.mark.parametrize("test_case", signup_data, ids=[tc["Test_Case_ID"] for tc in signup_data])
    def test_signup_api(self, test_case):
        self._execute_and_verify(test_case)

    @pytest.mark.api
    @pytest.mark.parametrize("test_case", payment_data, ids=[tc["Test_Case_ID"] for tc in payment_data])
    def test_payment_api(self, test_case):
        self._execute_and_verify(test_case)

    @pytest.mark.api
    @pytest.mark.parametrize("test_case", board_data, ids=[tc["Test_Case_ID"] for tc in board_data])
    def test_board_api(self, test_case):
        self._execute_and_verify(test_case)