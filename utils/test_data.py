"""
Utilities for generating and managing test data.

This module centralises functions for creating unique email addresses,
reading and writing credentials files, and retrieving fixed user input
values used throughout the tests. Storing these utilities in one place
encourages reuse and makes it straightforward to adjust values for
different test scenarios or environments.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, Tuple

from automation.utils.config import settings


def generate_unique_email(prefix: str = "user", domain: str = "yopmail.com") -> str:
    """Generate a pseudo‑unique email address for account creation.

    The email will take the form ``<prefix>_<UUID>@<domain>`` where UUID is
    a short hexadecimal string.

    Args:
        prefix: Optional prefix to identify the user.
        domain: Email domain to use.

    Returns:
        A new email string guaranteed to be unique for the current test run.
    """
    suffix = uuid.uuid4().hex[:8]
    return f"{prefix}_{suffix}@{domain}"


def save_credentials(file_path: Path, email: str, password: str) -> None:
    """Persist generated credentials to disk for subsequent reuse.

    Args:
        file_path: Path to the JSON file where credentials will be stored.
        email: The email address to save.
        password: The password to save.
    """
    data = {"email": email, "password": password}
    file_path.write_text(json.dumps(data, indent=2))


def load_credentials(file_path: Path) -> Tuple[str, str]:
    """Load credentials from a JSON file.

    Args:
        file_path: Path to the file to read.

    Returns:
        Tuple of (email, password).
    """
    raw = json.loads(file_path.read_text())
    return raw["email"], raw["password"]


def get_test_user_details() -> Dict[str, str]:
    """Return a dictionary of static user details used for account creation.

    These values are intentionally realistic to simulate a genuine user and
    satisfy the API requirements. Modify them here if you wish to tailor
    the information (e.g. using different countries or addresses).
    """
    return {
        "name": "Tazeem",
        "password": "Password123",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "1990",
        "firstname": "Tazeem",
        "lastname": "Hossain",
        "company": "TestCorp",
        "address1": "123 Main St",
        "address2": "Suite 100",
        "country": "Canada",
        "zipcode": "12345",
        "state": "Ontario",
        "city": "Toronto",
        "mobile_number": "1234567890",
    }
