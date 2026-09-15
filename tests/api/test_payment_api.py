import pytest
from config.settings import ApiTestConfiguration
from utils.api_client import DynamicApiClient
from utils.data_reader import extract_and_parse_test_parameters

# 1. Test Data Layer 연동: CSV에서 파싱된 튜플 리스트를 로드합니다.
payment_integration_dataset = extract_and_parse_test_parameters(
    target_csv_file_path=ApiTestConfiguration.PAYMENT_TEST_DATA_CSV_PATH,
    fallback_string_for_missing_data=ApiTestConfiguration.FALLBACK_VALUE_FOR_MISSING_DATA
)

# 2. Parameterization: CSV 헤더와 정확히 일치하는 매개변수를 주입합니다.
@pytest.mark.parametrize(
    "test_case_id, scenario_description, endpoint_path, http_method, request_payload, expected_http_status_code, expected_response_data",
    payment_integration_dataset
)
def test_dynamic_payment_api_edge_cases(
    test_case_id: str,
    scenario_description: str,
    endpoint_path: str,
    http_method: str,
    request_payload: dict,
    expected_http_status_code: int,
    expected_response_data: dict
):
    """
    CSV에 정의된 동적 엔드포인트와 페이로드를 기반으로 API 통합 테스트를 수행합니다.
    """
    
    # Arrange: 동적 API 클라이언트 인스턴스화
    api_client = DynamicApiClient(target_base_url=ApiTestConfiguration.BASE_URL)

    # Act: 주입된 파라미터로 HTTP 요청 실행
    api_response = api_client.execute_dynamic_request(
        http_method=http_method,
        endpoint_path=endpoint_path,
        request_payload=request_payload
    )

    # Assert 1: HTTP 상태 코드 검증
    assert api_response.status_code == expected_http_status_code, \
        f"[{test_case_id}] {scenario_description} - 상태 코드 불일치. 예상: {expected_http_status_code}, 실제: {api_response.status_code}"

    # Assert 2: 예상 응답 데이터(JSON) 부분 일치 검증
    # Expected_Response_Data가 정의된 경우에만 검증을 수행합니다.
    if expected_response_data:
        actual_json_response = api_response.json()
        
        for expected_key, expected_value in expected_response_data.items():
            actual_value = actual_json_response.get(expected_key)
            assert actual_value == expected_value, \
                f"[{test_case_id}] {scenario_description} - 응답 데이터 불일치. Key: '{expected_key}', 예상: '{expected_value}', 실제: '{actual_value}'"