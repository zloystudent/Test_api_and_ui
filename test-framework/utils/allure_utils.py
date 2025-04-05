import allure
import json
from typing import Dict, Any, Optional
import requests


def allure_request_logger(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
) -> None:
    """Log request details to Allure report"""
    with allure.step(f"Request: {method} {url}"):
        if headers:
            allure.attach(
                json.dumps(headers, indent=2), "Headers", allure.attachment_type.JSON
            )
        if data:
            allure.attach(
                json.dumps(data, indent=2) if isinstance(data, dict) else str(data),
                "Request Body",
                allure.attachment_type.JSON
                if isinstance(data, dict)
                else allure.attachment_type.TEXT,
            )


def allure_response_logger(response: requests.Response) -> None:
    """Log response details to Allure report"""
    with allure.step(f"Response: Status Code {response.status_code}"):
        try:
            # Try to parse as JSON
            response_body = response.json()
            allure.attach(
                json.dumps(response_body, indent=2),
                "Response Body",
                allure.attachment_type.JSON,
            )
        except Exception:
            # If not JSON, attach as text
            allure.attach(response.text, "Response Body", allure.attachment_type.TEXT)

        allure.attach(
            json.dumps(dict(response.headers), indent=2),
            "Response Headers",
            allure.attachment_type.JSON,
        )
