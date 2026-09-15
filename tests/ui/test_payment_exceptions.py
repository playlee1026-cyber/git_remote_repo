import pytest
from playwright.sync_api import Page, Route, expect
from config.settings import Config


def mock_aml_limit_exceeded_response(route: Route) -> None:
    """
    [네트워크 인터셉터 핸들러]
    실제 백엔드 대신, 중앙 관리되는 AML 한도 초과 에러(403) 데이터를 강제로 반환합니다.
    """
    route.fulfill(
        status=Config.MOCK_AML_ERROR_STATUS_CODE,
        json=Config.MOCK_AML_ERROR_RESPONSE_JSON
    )