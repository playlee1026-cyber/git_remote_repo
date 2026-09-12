import pandas as pd

def get_api_test_data(file_path):
    """
    CSV 파일을 읽어 PyTest 파라미터라이징을 위한 딕셔너리 리스트로 반환합니다.
    결측치는 빈 문자열로 처리하여 에러를 방지합니다.
    """
    df = pd.read_csv(file_path).fillna("")
    return df.to_dict('records')