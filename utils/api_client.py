import requests
import logging
from requests import Response

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        # 공통 헤더 중앙화
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logging.info(f"[API Request] {method} {url}")
        
        response = self.session.request(method, url, **kwargs)
        
        logging.info(f"[API Response] Status: {response.status_code}")
        return response

class SecurePaymentApiClient:
    """결제 API와의 HTTP 통신을 전담하는 클라이언트 객체입니다."""
    
    def __init__(self, target_base_url: str):
        self.target_base_url = target_base_url

    def execute_payment_request(self, endpoint_path: str, request_payload: dict) -> Response:
        """
        주어진 페이로드로 결제 엔드포인트에 POST 요청을 실행합니다.
        """
        full_endpoint_url = f"{self.target_base_url}{endpoint_path}"
        
        return requests.post(
            url=full_endpoint_url,
            json=request_payload
        )

class DynamicApiClient:
    """엔드포인트와 HTTP 메서드를 동적으로 처리하는 통신 클라이언트입니다."""
    
    def __init__(self, target_base_url: str):
        self.target_base_url = target_base_url

    def execute_request(
        self, 
        http_method: str, 
        endpoint_path: str, 
        request_payload: dict,
        request_timeout: int
    ) -> Response:
        """주어진 HTTP 메서드와 엔드포인트로 요청을 전송하고 응답을 반환합니다."""
        full_endpoint_url = f"{self.target_base_url}{endpoint_path}"
        
        return requests.request(
            method=http_method,
            url=full_endpoint_url,
            json=request_payload,
            timeout=request_timeout
        )