import pytest
from config.settings import ApiTestConfiguration
from utils.api_client import DynamicApiClient
from utils.data_reader import extract_and_parse_api_test_data

# 도메인별 데이터 로드 (중앙 설정 객체에서 경로를 주입받음)
signup_test_dataset = extract_and_parse_api_test_data(ApiTestConfiguration.SIGNUP_TEST_DATA_CSV_PATH)
payment_test_dataset = extract_and_parse_api_test_data(ApiTestConfiguration.PAYMENT_TEST_DATA_CSV_PATH)
board_test_dataset = extract_and_parse_api_test_data(ApiTestConfiguration.BOARD_TEST_DATA_CSV_PATH)

class TestUnifiedBusinessAPI:
    """모든 비즈니스 도메인 API를 동적으로 통합 검증하는 테스트 클래스입니다."""

    def _execute_api_and_assert_results(self, test_case_metadata: dict) -> None:
        """API를 실행하고 상태 코드 및 응답 데이터를 공통으로 검증하는 핵심 로직입니다."""
        
        api_client = DynamicApiClient(target_base_url=ApiTestConfiguration.BASE_URL)
        
        test_case_id = test_case_metadata["Test_Case_ID"]
        description = test_case_metadata["Description"]
        endpoint = test_case_metadata["Endpoint"]
        method = test_case_metadata["Method"]
        payload = test_case_metadata["Request_Payload"]
        expected_status = test_case_metadata["Expected_Status_Code"]
        expected_response_data = test_case_metadata["Expected_Response_Data"]

        # 1. 동적 API 요청 실행
        response = api_client.execute_request(
            http_method=method,
            endpoint_path=endpoint,
            request_payload=payload,
            request_timeout=ApiTestConfiguration.REQUEST_TIMEOUT_SECONDS
        )

        # 2. HTTP 상태 코드 검증
        assert response.status_code == expected_status, \
            f"[{test_case_id}] {description} - 상태 코드 불일치. 예상: {expected_status}, 실제: {response.status_code}"

        # 3. 응답 본문(JSON) 부분 일치 검증
        if expected_response_data:
            actual_response_json = response.json()
            for expected_key, expected_value in expected_response_data.items():
                actual_value = actual_response_json.get(expected_key)
                assert actual_value == expected_value, \
                    f"[{test_case_id}] {description} - 응답 데이터 불일치 (Key: '{expected_key}'). 예상: '{expected_value}', 실제: '{actual_value}'"

    @pytest.mark.api
    @pytest.mark.parametrize("test_case", signup_test_dataset, ids=[case["Test_Case_ID"] for case in signup_test_dataset])
    def test_signup_domain_api(self, test_case: dict):
        self._execute_api_and_assert_results(test_case)

    @pytest.mark.api
    @pytest.mark.parametrize("test_case", payment_test_dataset, ids=[case["Test_Case_ID"] for case in payment_test_dataset])
    def test_payment_domain_api(self, test_case: dict):
        self._execute_api_and_assert_results(test_case)

    @pytest.mark.api
    @pytest.mark.parametrize("test_case", board_test_dataset, ids=[case["Test_Case_ID"] for case in board_test_dataset])
    def test_board_domain_api(self, test_case: dict):
        self._execute_api_and_assert_results(test_case)