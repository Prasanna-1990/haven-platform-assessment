# Design Notes

## B2 - idempotency key

The idempotency key for `cost_tag_check.py` is the **SHA-256 hash of the canonical JSON of the
plan's `resource_changes`** (`json.dumps(..., sort_keys=True, separators=(",", ":"))`). It is
printed as the first line of every report. Idempotency comes from the check being a pure function
of the plan content: no state is persisted, findings are de-duplicated and sorted by resource
address, so an unchanged plan produces the same exit code and byte-identical output on every
run, and a changed plan produces a different key. I key on content, not on the file path or a
timestamp, because paths/timestamps change between identical plans (and stay the same between
different ones).

## Decisions with a real alternative

- **Access boundary = LandlordAccount, not tenant/property.** Per the README the manager is
  scoped to one landlord account, so the check walks report -> tenant -> property -> account.
  Comparing tenant ids would deny a manager their own other tenants.
- **Fail closed on ambiguity.** Missing tenant/property, blank account id, or duplicate ids
  return False rather than picking the first match.
- **Required tag is `landlord_account_id`**, not `tenant_id`, because it is the billing unit.
  A blank/whitespace value counts as missing. `tags_all` (provider default_tags) counts, with
  explicit `tags` winning.
- **"Taggable" is detected generically** by the presence of a `tags`/`tags_all` attribute in
  `change.after`, not a hardcoded type list. Trade-off: a taggable resource whose plan omits the
  attribute would be skipped; a provider-schema lookup would be stricter but heavier.
- **Skipped actions:** `no-op`, `read`, and delete-only. Replace (`delete`+`create`) is checked.
- **Exit codes:** 0 pass, 1 missing tags, 2 unreadable plan (fail closed).
- **No persisted "already reported" cache**: it adds stale-state risk for no benefit.
- **B0 fix is `for_each` + `moved` blocks**, chosen over `terraform state mv` alone because it
  is reviewable and reproducible in code.
