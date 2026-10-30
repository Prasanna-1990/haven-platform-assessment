import pytest

from app.seed_data import (
    LANDLORD_ACCOUNTS,
    PROPERTIES,
    PROPERTY_MANAGERS,
    SCREENING_REPORTS,
    TENANTS,
)


@pytest.fixture
def landlord_accounts():
    return LANDLORD_ACCOUNTS


@pytest.fixture
def properties():
    return PROPERTIES


@pytest.fixture
def property_managers():
    return PROPERTY_MANAGERS


@pytest.fixture
def tenants():
    return TENANTS


@pytest.fixture
def screening_reports():
    return SCREENING_REPORTS
