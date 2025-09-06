"""
Data factory for generating test data.

This module provides factories for creating realistic test data that can
be used across tests. It supports generating both random and fixed data
sets, with utilities for cleaning up test data after use.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserData:
    """Container for user registration data."""
    email: str
    password: str
    title: str
    name: str
    birth_date: str
    birth_month: str
    birth_year: str
    newsletter: bool
    special_offers: bool
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: Optional[str]
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str


class UserFactory:
    """Factory for creating user test data."""

    _countries = ["United States", "Canada", "United Kingdom", "Australia"]
    _cities = {
        "United States": ["New York", "Los Angeles", "Chicago"],
        "Canada": ["Toronto", "Vancouver", "Montreal"],
        "United Kingdom": ["London", "Manchester", "Birmingham"],
        "Australia": ["Sydney", "Melbourne", "Brisbane"]
    }

    @classmethod
    def create_random_user(cls, email: Optional[str] = None) -> UserData:
        """Create a user with randomized but valid-looking data.

        Args:
            email: Optional email to use instead of generating one.

        Returns:
            UserData instance with all required fields populated.
        """
        country = random.choice(cls._countries)
        city = random.choice(cls._cities[country])
        
        return UserData(
            email=email or f"user_{random.randint(1000, 9999)}@example.com",
            password="Password123!",
            title=random.choice(["Mr", "Mrs", "Ms"]),
            name=f"Test User {random.randint(1, 1000)}",
            birth_date=str(random.randint(1, 28)),
            birth_month=random.choice(["January", "February", "March", "April"]),
            birth_year=str(random.randint(1970, 2000)),
            newsletter=random.choice([True, False]),
            special_offers=random.choice([True, False]),
            first_name=f"FirstName{random.randint(1, 100)}",
            last_name=f"LastName{random.randint(1, 100)}",
            company=f"Company{random.randint(1, 100)}",
            address1=f"{random.randint(1, 999)} Main Street",
            address2=None,
            country=country,
            state=f"State{random.randint(1, 50)}",
            city=city,
            zipcode=str(random.randint(10000, 99999)),
            mobile_number=f"+1{random.randint(1000000000, 9999999999)}"
        )