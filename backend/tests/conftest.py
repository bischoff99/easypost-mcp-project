"""
Shared pytest fixtures and configuration
"""

import os

import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture
def easypost_api_key():
    """EasyPost API key from environment."""
    return os.getenv("EASYPOST_API_KEY")


@pytest.fixture
def sample_address_domestic():
    """Sample US domestic address."""
    return {
        "name": "Test User",
        "street1": "123 Main St",
        "city": "Los Angeles",
        "state": "CA",
        "zip": "90021",
        "country": "US",
    }


@pytest.fixture
def sample_address_international():
    """Sample international address."""
    return {
        "name": "Test User",
        "street1": "123 Test Street",
        "city": "London",
        "state": "",
        "zip": "SW1A 1AA",
        "country": "GB",
    }


@pytest.fixture
def sample_parcel():
    """Sample parcel dimensions."""
    return {
        "length": 10,
        "width": 10,
        "height": 5,
        "weight": 16,  # ounces
    }
