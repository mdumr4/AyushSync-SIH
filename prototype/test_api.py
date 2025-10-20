from fastapi.testclient import TestClient
from .main import app  # Use relative import

# This client allows us to make requests to our FastAPI app without a running server
client = TestClient(app)


def test_lookup_success():
    """Tests a successful lookup for the term 'Cough'"""
    print("--- Running test_lookup_success ---")
    response = client.get("/lookup?filter=Cough")
    # Check that the request was successful
    assert response.status_code == 200
    data = response.json()
    print(f"Response JSON: {data}")
    # Check that we got results
    assert len(data) > 0
    # CORRECTED: Use the correct, uppercase key 'TERM_NAME'
    assert any(item['TERM_NAME'] == 'Kasa' for item in data)
    print("test_lookup_success: PASSED")


def test_lookup_not_found():
    """Tests a search for a term that doesn't exist"""
    print("\n--- Running test_lookup_not_found ---")
    response = client.get("/lookup?filter=nonexistentterm")
    assert response.status_code == 200
    data = response.json()
    print(f"Response JSON: {data}")
    assert data["message"] == "No results found."
    print("test_lookup_not_found: PASSED")


def test_lookup_no_filter():
    """Tests calling the endpoint without the required 'filter' parameter"""
    print("\n--- Running test_lookup_no_filter ---")
    response = client.get("/lookup")
    # Expect a 422 Unprocessable Entity error for validation failure
    assert response.status_code == 422
    print("Received expected 422 Error for missing parameter.")
    print("test_lookup_no_filter: PASSED")


if __name__ == "__main__":
    test_lookup_success()
    test_lookup_not_found()
    test_lookup_no_filter()
    print("\nAll tests completed.")