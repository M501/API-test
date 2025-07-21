import json
import pytest
import requests

# JSON loading
def load_login_cases(path="authentication.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

login_cases = load_login_cases()

@pytest.mark.parametrize("case", login_cases)
def test_login(case):

#Testing by JSON data
    url = "https://stage-mgt.antisleep.ru/api/v1.00/public/login"
    payload = {"email": case["email"], "password": case["password"]}

    response = requests.post(url, json=payload)
    assert response.status_code == case["expected_status"], \
        f"Expected status {case['expected_status']}, got {response.status_code}"

    body = response.json()
    if case["expected_status"] == 200:
        # positive case: token must be present
        assert "token" in body and body["token"], "Token not returned or empty"
    else:
        # negative case: error message must contain expected_error
        message = body.get("message", "")
        assert case["expected_error"] in message, \
            f"Expected error '{case['expected_error']}' in message '{message}'"

if __name__ == "__main__":
    pytest.main(["-v", "--maxfail=1", "--disable-warnings"])
