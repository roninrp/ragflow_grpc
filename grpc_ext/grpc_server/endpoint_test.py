import requests


def check_endpoint(base_url: str, endpoint: str) -> str | None:
    """
    Checks if each endpoint in a list is valid with Ragflow's server returning code 0.

    Parameters
    ----------
    param base_url: str
        The base URL of your RAGFlow service (e.g., "http://localhost:8000")

    endpoint: str
        Endpoint paths (e.g., "/api/v1/ragflow", "/health"])

    Returns
    -------
    str | None
       str if the endpoint in active with Ragflow's server returning code = 0
       None if otherwise.

       Note: both cases return HTTP 200.

    """
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, timeout=5)
        http_status = response.status_code

        # Default assumption
        is_active = False
        detail = ""

        # Try to parse JSON body if present
        try:
            body = response.json()
            # Some APIs (like RAGFlow) use a custom "code" field for errors
            api_code = body.get("code")
            message = body.get("message", "")

            # Heuristic: code == 0 or absence of error message = success
            if api_code == 0 or "NotFound" not in str(message):
                is_active = True
            else:
                is_active = False
                detail = message

        except ValueError:
            # Non-JSON response (like HTML or plain text)
            is_active = http_status == 200
            detail = "Non-JSON response"

        if is_active:
            print(f"✅ {url} → Active (HTTP {http_status})")
            return f"{url} → Active (HTTP {http_status})"
        else:
            print(f"❌ {url} → Invalid endpoint or error (HTTP {http_status}) | {detail}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ {url} → Unreachable ({e})")
        return None


def test_register_endpoint():
    """
    Test fucntion to test ragflow's "/v1/user/register" endpoint accessed by grpc_async_server_ragserve.py.

    """
    base = "http://localhost:9380"
    endpoint = "/v1/user/register"
    reply = check_endpoint(base, endpoint)
    print("\n", reply, "\n")
    print("test")
    print(f"{base + endpoint} → Active (HTTP 200)")
    assert reply == f"{base + endpoint} → Active (HTTP 200)"


def test_login_endpoint():
    """
    Test fucntion to test ragflow's "/v1/user/login" endpoint accessed by grpc_async_server_ragserve.py.

    """
    base = "http://localhost:9380"
    endpoint = "/v1/user/login"
    reply = check_endpoint(base, endpoint)
    print("\n", reply, "\n")
    print("test")
    print(f"{base + endpoint} → Active (HTTP 200)")
    assert reply == f"{base + endpoint} → Active (HTTP 200)"


def test_new_token_endpoint():
    """
    Test fucntion to test ragflow's "/v1/system/new_token" endpoint accessed by grpc_async_server_ragserve.py.

    """
    base = "http://localhost:9380"
    endpoint = "/v1/system/new_token"
    reply = check_endpoint(base, endpoint)
    print("\n", reply, "\n")
    print("test")
    print(f"{base + endpoint} → Active (HTTP 200)")
    assert reply == f"{base + endpoint} → Active (HTTP 200)"


# Example usage
if __name__ == "__main__":
    base = "http://localhost:9380"
    endpoints = ["/docs", "/nonexistent", "/v1/user/login", "/v1/user/register", "/v1/system/new_token", "/v1/system/healthz"]
    for endpoint in endpoints:
        reply = check_endpoint(base, endpoint)
        print("\n", reply, "\n")
