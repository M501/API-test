import json
import pytest
import requests
import allure

# --------------------------------------
# Fixture to obtain auth token via API login
# --------------------------------------
@pytest.fixture(scope="session")
def auth_token():
    """
    Obtain bearer token by authenticating via API
    """
    with allure.step("1) Authenticate and retrieve token"):
        url = "https://stage-mgt.antisleep.ru/api/v1.00/public/login"
        creds = {"email": "demo@demo.ru", "password": "Demo1704@demo.ru"}
        resp = requests.post(url, json=creds)
        assert resp.status_code == 200, f"Login failed: {resp.status_code}"
        token = resp.json().get("token")
        assert token, "Token not found in login response"
    return token

# --------------------------------------
# Load update settings test cases from JSON
# --------------------------------------
def load_settings_cases(path="settings.json"):
    """
    Load JSON test data from settings.json in the script directory.
    """
    import os
    base = os.path.dirname(__file__)
    file_path = os.path.join(base, path)
    with allure.step(f"2) Load test cases from {path}"):
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    return data.get("positive_cases", []), data.get("negative_cases", [])

# Load test cases
positive_cases, negative_cases = load_settings_cases()

# --------------------------------------
# Positive tests for user settings
# --------------------------------------
@pytest.mark.parametrize("case", positive_cases)
def test_update_settings_positive(auth_token, case):
    allure.dynamic.feature("Antisleep API Tests")
    allure.dynamic.story("Update Settings - Positive Cases")

    with allure.step(f"3) Update user settings (positive): {case['description']}"):
        url = "https://stage-mgt.antisleep.ru/api/v1.00/public/user/settings"
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        payload = {k: v for k, v in case.items() if k != "description"}
        resp = requests.put(url, json=payload, headers=headers)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        body = resp.json()
        assert body.get("success") is True, f"Expected success true, got {body}"

# --------------------------------------
# Negative tests for user settings
# --------------------------------------
@pytest.mark.parametrize("case", negative_cases)
def test_update_settings_negative(auth_token, case):
    allure.dynamic.feature("Antisleep API Tests")
    allure.dynamic.story("Update Settings - Negative Cases")

    with allure.step(f"4) Update user settings (negative): {case['description']}"):
        url = "https://stage-mgt.antisleep.ru/api/v1.00/public/user/settings"
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        payload = {k: v for k, v in case.items() if k != "description"}
        resp = requests.put(url, json=payload, headers=headers)
        assert 400 <= resp.status_code < 500, f"Expected 4xx, got {resp.status_code}"
        body = resp.json()
        msg = body.get("message", "") or json.dumps(body.get("errors", {}))
        assert msg, "No error message returned"

if __name__ == "__main__":
    pytest.main(["-v", "--maxfail=1", "--disable-warnings"])
