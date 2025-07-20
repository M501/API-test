import json
import pytest
import requests


# JSON loading
def load_settings_cases(path="b.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


settings_cases = load_settings_cases()


@pytest.fixture(scope="session")
def auth_token():
    # Load login credentials from A.JSON
    with open("c:\\.Py\\Anti_Sleep\\Anti_Sleep_B\\A.JSON", encoding="utf-8") as f:
        login_cases = json.load(f)
    # Find the successful login case (TC-A1)
    success_case = next((case for case in login_cases if case["case_id"] == "TC-A1"), None)
    assert success_case, "TC-A1 (successful login) not found in A.JSON"
    url = "https://stage-mgt.antisleep.ru/api/v1.00/public/login"
    payload = {"email": success_case["email"], "password": success_case["password"]}
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("token")
    assert token, "No token in login response"
    return token


@pytest.mark.parametrize("case", settings_cases['positive_cases'])
def test_update_settings_positive(case, auth_token):
    url = "https://stage-mgt.antisleep.ru/api/v1.00/public/user/settings"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(url, json=case, headers=headers)
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    body = response.json()
    assert 'success' in body and body['success'], "Success flag not returned or false"


@pytest.mark.parametrize("case", settings_cases['negative_cases'])
def test_update_settings_negative(case, auth_token):
    url = "https://stage-mgt.antisleep.ru/api/v1.00/public/user/settings"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(url, json=case, headers=headers)
    assert response.status_code == 422, \
        f"Expected status 422, got {response.status_code}"
    body = response.json()
    assert 'error' in body, "Error message not returned"


if __name__ == "__main__":
    pytest.main(["-v", "--maxfail=1", "--disable-warnings"])
