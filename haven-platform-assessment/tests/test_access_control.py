"""
B2 part 1 tests: cross-account is denied, same-account is allowed, and the check fails closed.
"""
from dataclasses import replace

from app.access_control import can_access_screening_report


def _pm(property_managers, pm_id):
    return next(p for p in property_managers if p.id == pm_id)


def _rep(screening_reports, rep_id):
    return next(r for r in screening_reports if r.id == rep_id)


def test_cross_account_denied(property_managers, properties, tenants, screening_reports):
    pm001 = _pm(property_managers, "pm-001")  # la-001
    rep002 = _rep(screening_reports, "rep-002")  # belongs to la-002's tenant
    assert can_access_screening_report(pm001, rep002, properties=properties, tenants=tenants) is False


def test_cross_account_denied_reverse(property_managers, properties, tenants, screening_reports):
    pm002 = _pm(property_managers, "pm-002")  # la-002
    rep001 = _rep(screening_reports, "rep-001")
    assert can_access_screening_report(pm002, rep001, properties=properties, tenants=tenants) is False


def test_same_account_allowed(property_managers, properties, tenants, screening_reports):
    pm001 = _pm(property_managers, "pm-001")
    rep001 = _rep(screening_reports, "rep-001")
    assert can_access_screening_report(pm001, rep001, properties=properties, tenants=tenants) is True


def test_same_account_allowed_second_account(property_managers, properties, tenants, screening_reports):
    pm002 = _pm(property_managers, "pm-002")
    rep002 = _rep(screening_reports, "rep-002")
    assert can_access_screening_report(pm002, rep002, properties=properties, tenants=tenants) is True


def test_fails_closed_when_tenant_missing(property_managers, properties, screening_reports):
    pm001 = _pm(property_managers, "pm-001")
    rep001 = _rep(screening_reports, "rep-001")
    assert can_access_screening_report(pm001, rep001, properties=properties, tenants=[]) is False


def test_fails_closed_when_property_missing(property_managers, tenants, screening_reports):
    pm001 = _pm(property_managers, "pm-001")
    rep001 = _rep(screening_reports, "rep-001")
    assert can_access_screening_report(pm001, rep001, properties=[], tenants=tenants) is False


def test_fails_closed_on_blank_actor_account(property_managers, properties, tenants, screening_reports):
    blank = replace(_pm(property_managers, "pm-001"), landlord_account_id="")
    rep001 = _rep(screening_reports, "rep-001")
    assert can_access_screening_report(blank, rep001, properties=properties, tenants=tenants) is False


def test_fails_closed_on_ambiguous_duplicate_property(property_managers, properties, tenants, screening_reports):
    pm001 = _pm(property_managers, "pm-001")
    rep001 = _rep(screening_reports, "rep-001")
    dup = properties + [replace(properties[0], landlord_account_id="la-002")]
    assert can_access_screening_report(pm001, rep001, properties=dup, tenants=tenants) is False
