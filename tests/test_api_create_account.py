"""
Tests for the Create Account API of Automation Exercise.

These tests exercise the API used to register a new user. They
validate that a user can be created with valid data and that the
service returns an appropriate error when attempting to create a user
with an existing email address. Upon successful account creation the
credentials are persisted to ``user_credentials.json`` for use by
the end‑to‑end UI test.
"""

import json
from pathlib import Path
import pytest
import requests

from automation.utils.config import settings
from automation.utils.test_data import generate_unique_email, save_credentials, get_test_user_details


API_URL = f"{settings.base_url}/api/createAccount"


def test_register_user_and_prevent_duplicate(credentials_file: Path) -> None:
    """Register a new user and ensure duplicate registration fails."""
    # Generate unique email for account creation
    email = generate_unique_email(prefix="tazeem")
    password = get_test_user_details()["password"]
    payload = get_test_user_details().copy()
    payload.update({"email": email})

    # First attempt should succeed with responseCode 201 and message "User created!"
    response = requests.post(API_URL, data=payload)
    assert response.status_code == 200, f"Unexpected HTTP status: {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data["responseCode"] == 201, f"Unexpected response code: {response_data.get('responseCode')}. Response: {response.text}"
    assert response_data["message"] == "User created!", f"Unexpected response message: {response_data.get('message')}"

    # Save credentials for UI login test
    save_credentials(credentials_file, email, password)

    # Second attempt using the same email should indicate that email already exists
    response_dup = requests.post(API_URL, data=payload)
    assert response_dup.status_code == 200, f"Unexpected HTTP status on duplicate: {response_dup.status_code}. Response: {response_dup.text}"
    response_dup_data = response_dup.json()
    assert response_dup_data["responseCode"] == 400, f"Unexpected response code on duplicate: {response_dup_data.get('responseCode')}. Response: {response_dup.text}"
    assert "Email already exists" in response_dup_data["message"], f"Unexpected duplicate response message: {response_dup_data.get('message')}"
