# Terminal Log

## Setup
```
Python 3.12.3
pytest 9.2.0
```

## B2.1 access control tests
```
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/claude/haven-platform-assessment
collecting ... collected 8 items

tests/test_access_control.py::test_cross_account_denied PASSED           [ 12%]
tests/test_access_control.py::test_cross_account_denied_reverse PASSED   [ 25%]
tests/test_access_control.py::test_same_account_allowed PASSED           [ 37%]
tests/test_access_control.py::test_same_account_allowed_second_account PASSED [ 50%]
tests/test_access_control.py::test_fails_closed_when_tenant_missing PASSED [ 62%]
tests/test_access_control.py::test_fails_closed_when_property_missing PASSED [ 75%]
tests/test_access_control.py::test_fails_closed_on_blank_actor_account PASSED [ 87%]
tests/test_access_control.py::test_fails_closed_on_ambiguous_duplicate_property PASSED [100%]

============================== 8 passed in 0.01s ===============================
```

## B2.2 cost-tag check tests
```
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/claude/haven-platform-assessment
collecting ... collected 8 items

tests/test_cost_tag_check.py::test_fixture_flags_missing_and_passes_tagged PASSED [ 12%]
tests/test_cost_tag_check.py::test_idempotent_same_exit_code_and_output PASSED [ 25%]
tests/test_cost_tag_check.py::test_generic_across_resource_types PASSED  [ 37%]
tests/test_cost_tag_check.py::test_skips_noop_read_delete_and_untaggable PASSED [ 50%]
tests/test_cost_tag_check.py::test_replace_is_in_scope PASSED            [ 62%]
tests/test_cost_tag_check.py::test_blank_value_and_default_tags PASSED   [ 75%]
tests/test_cost_tag_check.py::test_idempotency_key_stable_and_order_insensitive_and_changes_with_plan PASSED [ 87%]
tests/test_cost_tag_check.py::test_unreadable_plan_fails_closed PASSED   [100%]

============================== 8 passed in 0.02s ===============================
```

## Cost-tag check, run 1
```
idempotency key: 5999178bac13c4fe5ce6a146b5548d306315c8fb485ddab1cb8313946550a576
FAIL: 2 resource(s) missing required tag 'landlord_account_id':
  - aws_lambda_function.mls_feed_sync
  - aws_s3_bucket.listing_media
exit=1
```

## Cost-tag check, run 2 (unchanged plan -> identical output)
```
idempotency key: 5999178bac13c4fe5ce6a146b5548d306315c8fb485ddab1cb8313946550a576
FAIL: 2 resource(s) missing required tag 'landlord_account_id':
  - aws_lambda_function.mls_feed_sync
  - aws_s3_bucket.listing_media
exit=1
```

Note: terraform was not available in this environment; B0 was reasoned from the seeded state.
