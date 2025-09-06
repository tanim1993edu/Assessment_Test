"""
Tests for API account creation, including negative scenarios.
"""

import pytest
import requests
from utils.config import settings
from utils.test_data import generate_unique_email, get_test_user_details


def test_duplicate_account_creation():
    """Test that attempting to create a duplicate account returns an error."""
    # First create an account
    email = generate_unique_email()
    user_data = get_test_user_details()
    
    # First account creation should succeed
    response = requests.post(
        f"{settings.api_base_url}/createAccount",
        data={
            "name": user_data["name"],
            "email": email,
            "password": user_data["password"],
            "title": user_data["title"],
            "birth_date": user_data["birth_date"],
            "birth_month": user_data["birth_month"],
            "birth_year": user_data["birth_year"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"],
            "company": user_data["company"],
            "address1": user_data["address1"],
            "address2": user_data["address2"],
            "country": user_data["country"],
            "zipcode": user_data["zipcode"],
            "state": user_data["state"],
            "city": user_data["city"],
            "mobile_number": user_data["mobile_number"]
        }
    )
    
    assert response.status_code == 200, f"First account creation failed: {response.text}"
    response_data = response.json()
    assert response_data["responseCode"] == 201, f"Account creation failed: {response_data}"
    assert "User created!" in response_data.get("message", ""), f"Unexpected response: {response_data}"
    
    # Attempt to create account with same email
    response = requests.post(
        f"{settings.api_base_url}/createAccount",
        data={  # Using same email but different other details
            "name": "Different Name",
            "email": email,  # Same email as before
            "password": "DifferentPass123",
            "title": "Mrs",
            "birth_date": "15",
            "birth_month": "6",
            "birth_year": "1995",
            "firstname": "Jane",
            "lastname": "Doe",
            "company": "Test Corp",
            "address1": "456 Second St",
            "country": "United States",
            "zipcode": "54321",
            "state": "CA",
            "city": "Los Angeles",
            "mobile_number": "9876543210"
        }
    )
    
    # Verify the error response
    response_data = response.json()
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response_data["responseCode"] == 400, f"Expected error 400, got: {response_data}"
    assert "Email already exists!" in response_data.get("message", ""), \
        f"Unexpected error message: {response_data}"