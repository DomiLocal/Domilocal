import sys
import os

# Add paths to make imports work from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from repository.order_repository import order_repository

client = TestClient(app)


def test_case_1_successful_update():
    print("Running Caso 1: Successful status update (in_preparation -> ready_for_pickup)...")
    
    # Precondition: PED-0789 is in state 'in_preparation'
    order_repository.set_db_availability(True)
    order = order_repository.get_by_id("PED-0789")
    order.status = "in_preparation"
    
    response = client.patch("/api/v1/orders/PED-0789/ready-for-pickup")
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    
    res_json = response.json()
    assert res_json["success"] is True
    assert res_json["message"] == "Order marked as ready for pickup."
    assert res_json["data"]["order_id"] == "PED-0789"
    assert res_json["data"]["status"] == "ready_for_pickup"
    assert "updated_at" in res_json["data"]
    print("Caso 1 Passed! ✅\n")


def test_case_2_incorrect_status_update():
    print("Running Caso 2: Incorrect status (received or ready_for_pickup)...")
    
    # Check PED-00002 which is in 'received' status
    response = client.patch("/api/v1/orders/PED-00002/ready-for-pickup")
    assert response.status_code == 400, f"Expected 400 but got {response.status_code}"
    res_json = response.json()
    assert res_json["success"] is False
    assert "Unable to update status" in res_json["message"]
    
    # Check PED-00003 which is in 'ready_for_pickup' status
    response = client.patch("/api/v1/orders/PED-00003/ready-for-pickup")
    assert response.status_code == 400, f"Expected 400 but got {response.status_code}"
    res_json = response.json()
    assert res_json["success"] is False
    assert "Unable to update status" in res_json["message"]
    print("Caso 2 Passed! ✅\n")


def test_case_3_non_existent_id():
    print("Running Caso 3: Non-existent order ID...")
    
    response = client.patch("/api/v1/orders/PED-NONEXISTENT/ready-for-pickup")
    assert response.status_code == 404, f"Expected 404 but got {response.status_code}"
    res_json = response.json()
    assert res_json["success"] is False
    assert "does not exist" in res_json["message"]
    print("Caso 3 Passed! ✅\n")


def test_case_4_database_unavailable():
    print("Running Caso 4: Database unavailable (503 Service Unavailable)...")
    
    # Simulate DB connection error
    order_repository.set_db_availability(False)
    try:
        response = client.patch("/api/v1/orders/PED-0789/ready-for-pickup")
        assert response.status_code == 503, f"Expected 503 but got {response.status_code}"
        res_json = response.json()
        assert res_json["success"] is False
        assert "Database connection failed" in res_json["message"]
    finally:
        # Reset database availability
        order_repository.set_db_availability(True)
    print("Caso 4 Passed! ✅\n")


if __name__ == "__main__":
    print("=== STARTING INTEGRATION TESTS FOR VENDEDOR ORDER STATUS UPDATE ===\n")
    try:
        test_case_1_successful_update()
        test_case_2_incorrect_status_update()
        test_case_3_non_existent_id()
        test_case_4_database_unavailable()
        print("==================================================================")
        print("ALL TESTS PASSED SUCCESSFULLY! 🎉")
        print("==================================================================")
    except AssertionError as e:
        print(f"Test failure occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error running tests: {e}")
        sys.exit(1)
