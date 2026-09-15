import pandas as pd
import json
from typing import List, Dict, Any

def extract_and_parse_api_test_data(
    target_csv_file_path: str, 
    fallback_string_for_missing_data: str = ""
) -> List[Dict[str, Any]]:
    """
    CSV 파일을 읽어 파이썬 딕셔너리 리스트로 변환하고, 
    내부의 JSON 문자열 필드들을 자동으로 파싱합니다.
    """
    loaded_dataframe = pd.read_csv(target_csv_file_path).fillna(fallback_string_for_missing_data)
    parsed_test_records = []
    
    for row in loaded_dataframe.itertuples(index=False):
        # 1. 요청 페이로드 JSON 파싱
        parsed_request_payload = json.loads(row.Request_Payload) if row.Request_Payload else {}
        
        # 2. 기대 응답 데이터 JSON 파싱
        try:
            parsed_expected_response = json.loads(row.Expected_Response_Data) if row.Expected_Response_Data else {}
        except (json.JSONDecodeError, AttributeError):
            parsed_expected_response = {}

        # 3. 정제된 데이터를 딕셔너리 형태로 재구성하여 적재
        parsed_test_records.append({
            "Test_Case_ID": row.Test_Case_ID,
            "Description": row.Description,
            "Endpoint": row.Endpoint,
            "Method": row.Method,
            "Request_Payload": parsed_request_payload,
            "Expected_Status_Code": int(row.Expected_Status_Code),
            "Expected_Response_Data": parsed_expected_response
        })
        
    return parsed_test_records