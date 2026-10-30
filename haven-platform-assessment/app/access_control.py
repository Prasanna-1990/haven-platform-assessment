"""
B2, part 1 - can_access_screening_report().

README domain model: LandlordAccount (billing unit) -> Property -> Tenant -> ScreeningReport.
A PropertyManager is scoped to exactly one LandlordAccount.

The boundary that gates a ScreeningReport is therefore the LandlordAccount, reached by walking
report -> tenant -> property -> landlord_account_id. The tenant's own id (or the property id)
is NOT the boundary: a manager legitimately sees many tenants and properties under one account.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Return True only if actor's landlord account owns the report's tenant's property.
    Fails closed: missing/ambiguous tenant or property, or a blank account id, returns False.
    """
    if not actor.landlord_account_id:
        return False

    matching_tenants = [t for t in tenants if t.id == report.tenant_id]
    if len(matching_tenants) != 1:  # not found, or duplicate ids -> ambiguous -> deny
        return False
    tenant = matching_tenants[0]

    matching_properties = [p for p in properties if p.id == tenant.property_id]
    if len(matching_properties) != 1:
        return False
    prop = matching_properties[0]

    if not prop.landlord_account_id:
        return False

    return prop.landlord_account_id == actor.landlord_account_id
