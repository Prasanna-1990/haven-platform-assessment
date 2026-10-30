"""
Haven's tenancy model. Read README.md for how these fit together before you touch
access_control.py or cost_tag_check.py.

    LandlordAccount (billing unit)
      -> Property
           -> Tenant
                -> ScreeningReport

    PropertyManager is scoped to exactly one LandlordAccount.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class LandlordAccount:
    id: str
    name: str


@dataclass(frozen=True)
class Property:
    id: str
    landlord_account_id: str
    address: str


@dataclass(frozen=True)
class PropertyManager:
    id: str
    name: str
    landlord_account_id: str


@dataclass(frozen=True)
class Tenant:
    id: str
    name: str
    property_id: str


@dataclass(frozen=True)
class ScreeningReport:
    id: str
    tenant_id: str
    ssn_last4: str
    credit_score: int
