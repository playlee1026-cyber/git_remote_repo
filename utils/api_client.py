import requests
import logging

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