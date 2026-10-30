"""
Seeded domain data for the assessment. Do not modify — the assignment's "must work" checks
assume this data is unchanged.

Two landlord accounts (la-001, la-002), each with one property, one property manager, one
tenant, and one screening report. Use this to reason about and test the cross-account denial
case in B2, part 1: a PropertyManager scoped to la-001 must never be able to access the
screening report belonging to la-002's tenant, and vice versa.
"""
from app.models import LandlordAccount, Property, PropertyManager, ScreeningReport, Tenant

LANDLORD_ACCOUNTS = [
    LandlordAccount(id="la-001", name="Maple Grove Holdings"),
    LandlordAccount(id="la-002", name="Birchwood Properties"),
]

PROPERTIES = [
    Property(id="prop-001", landlord_account_id="la-001", address="12 Maple St"),
    Property(id="prop-002", landlord_account_id="la-002", address="88 Birch Ave"),
]

PROPERTY_MANAGERS = [
    PropertyManager(id="pm-001", name="Asha Rao", landlord_account_id="la-001"),
    PropertyManager(id="pm-002", name="Leo Fontaine", landlord_account_id="la-002"),
]

TENANTS = [
    Tenant(id="ten-001", name="J. Alvarez", property_id="prop-001"),
    Tenant(id="ten-002", name="S. Okafor", property_id="prop-002"),
]

SCREENING_REPORTS = [
    ScreeningReport(id="rep-001", tenant_id="ten-001", ssn_last4="1234", credit_score=710),
    ScreeningReport(id="rep-002", tenant_id="ten-002", ssn_last4="5678", credit_score=690),
]
