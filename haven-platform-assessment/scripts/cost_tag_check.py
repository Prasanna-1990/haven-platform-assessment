"""
B2, part 2 - cost-tagging check.

Fails (non-zero exit) if any taggable resource being created/updated in a `terraform show -json`
plan lacks a non-empty `landlord_account_id` tag. The billing unit is the LandlordAccount (see
README), so `tenant_id` or any other tag does not satisfy the check.

Idempotency: the check is a pure function of the plan's contents. It keeps no state between runs
and prints findings sorted by resource address, so re-running on an unchanged plan yields the
same exit code and byte-identical output. The report carries an idempotency key - the SHA-256 of
the canonicalised `resource_changes` - so two runs can be proven to have looked at the same plan.

Exit codes: 0 = all taggable resources tagged, 1 = at least one missing the tag,
            2 = plan could not be read/parsed (fail closed, never a silent pass).

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import hashlib
import json
import sys

REQUIRED_TAG = "landlord_account_id"
SKIPPED_ACTIONS = {"no-op", "read"}


def plan_idempotency_key(plan: dict) -> str:
    """SHA-256 over the canonical (sorted-keys, compact) JSON of resource_changes."""
    canonical = json.dumps(plan.get("resource_changes", []), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _is_in_scope(change: dict) -> bool:
    """Only resources being created or updated (incl. replace) with a known `after` state."""
    actions = set(change.get("actions") or [])
    if not actions or actions <= SKIPPED_ACTIONS:
        return False
    if actions == {"delete"}:  # nothing left to bill
        return False
    return isinstance(change.get("after"), dict)


def _effective_tags(after: dict):
    """
    Returns the tag dict for a taggable resource, or None if the resource has no tag attribute
    at all (generic: any resource type that exposes `tags` / `tags_all`). tags_all includes
    provider default_tags; explicit `tags` win on conflict.
    """
    if "tags" not in after and "tags_all" not in after:
        return None
    merged = {}
    for key in ("tags_all", "tags"):
        value = after.get(key)
        if isinstance(value, dict):
            merged.update(value)
    return merged


def find_missing(plan: dict) -> list[str]:
    """Sorted, de-duplicated addresses of in-scope taggable resources missing the billing tag."""
    missing = set()
    for rc in plan.get("resource_changes", []):
        change = rc.get("change") or {}
        if not _is_in_scope(change):
            continue
        tags = _effective_tags(change["after"])
        if tags is None:
            continue
        value = tags.get(REQUIRED_TAG)
        if not isinstance(value, str) or not value.strip():
            missing.add(rc.get("address", "<unknown address>"))
    return sorted(missing)


def evaluate_plan(plan: dict) -> tuple[int, str]:
    """Pure: returns (exit_code, report_text) for an in-memory plan."""
    key = plan_idempotency_key(plan)
    missing = find_missing(plan)
    lines = [f"idempotency key: {key}"]
    if missing:
        lines.append(f"FAIL: {len(missing)} resource(s) missing required tag '{REQUIRED_TAG}':")
        lines.extend(f"  - {addr}" for addr in missing)
        return 1, "\n".join(lines)
    lines.append(f"PASS: all taggable resources carry '{REQUIRED_TAG}'.")
    return 0, "\n".join(lines)


def check_plan(plan_path: str) -> int:
    """
    Returns an exit code: 0 if every taggable resource being created/changed has
    `landlord_account_id`, non-zero otherwise.
    """
    try:
        with open(plan_path, encoding="utf-8") as fh:
            plan = json.load(fh)
        if not isinstance(plan, dict):
            raise ValueError("plan root must be a JSON object")
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot read plan '{plan_path}': {exc}")
        return 2
    code, report = evaluate_plan(plan)
    print(report)
    return code


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
