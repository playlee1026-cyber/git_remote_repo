import pandas as pd
import json
from typing import List, Tuple, Any

def extract_and_parse_test_parameters(
    target_csv_file_path: str, 
    fallback_string_for_missing_data: str = ""
) -> List[Tuple[Any, ...]]:
    """
    CSV 파일을 읽어 PyTest 파라미터라이징을 위한 튜플 리스트로 반환합니다.
    JSON 문자열로 작성된 Request_Payload와 Expected_Response_Data를 딕셔너리로 파싱합니다.
    """
    loaded_dataframe = pd.read_csv(target_csv_file_path).fillna(fallback_string_for_missing_data)
    test_parameter_tuples = []
    
    for row in loaded_dataframe.itertuples(index=False):
        # 1. 요청 페이로드 JSON 파싱 (비어있을 경우 빈 딕셔너리 할당)
        parsed_request_payload = json.loads(row.Request_Payload) if row.Request_Payload else {}
        
        # 2. 기대 응답 페이로드 JSON 파싱 (일부 예외 케이스에서 응답 데이터 검증이 생략된 경우를 방어)
        try:
            parsed_expected_response = json.loads(row.Expected_Response_Data) if row.Expected_Response_Data else {}
        except (json.JSONDecodeError, AttributeError):
            parsed_expected_response = {}

        # 3. 테스트 함수 매개변수 순서에 맞게 튜플로 조립
        test_parameter_tuples.append((
            row.Test_Case_ID,
            row.Description,
            row.Endpoint,
            row.Method,
            parsed_request_payload,
            row.Expected_Status_Code,
            parsed_expected_response
        ))
        
    return test_parameter_tuples