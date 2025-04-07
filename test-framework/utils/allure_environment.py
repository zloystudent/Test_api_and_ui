import allure
import platform
import requests
import os


def generate_environment_file() -> None:
    """Generate environment.properties file for Allure report"""
    env_data: Dict[str, str] = {
        "Python Version": platform.python_version(),
        "Platform": platform.platform(),
        "API Base URL": "http://localhost:8080",
    }

    try:
        response: requests.Response = requests.get("http://localhost:8080/api/version")
        if response.status_code == 200:
            env_data["API Version"] = response.text
    except Exception:
        env_data["API Version"] = "Unknown"

    if not os.path.exists("allure-results"):
        os.makedirs("allure-results")

    with open("allure-results/environment.properties", "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")
