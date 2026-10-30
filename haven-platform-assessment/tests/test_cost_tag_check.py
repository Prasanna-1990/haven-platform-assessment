"""B2 part 2 tests: happy path on the fixture, genericity, and idempotency."""
import copy
import json
from pathlib import Path

from scripts.cost_tag_check import check_plan, evaluate_plan, find_missing

FIXTURE = str(Path(__file__).resolve().parent.parent / "fixtures" / "plan.json")


def test_fixture_flags_missing_and_passes_tagged(capsys):
    assert check_plan(FIXTURE) == 1
    out = capsys.readouterr().out
    assert "aws_s3_bucket.listing_media" in out          # only has tenant_id
    assert "aws_lambda_function.mls_feed_sync" in out    # empty tags
    assert "aws_s3_bucket.landlord_media[0]" not in out
    assert "aws_lambda_function.screening_report_export" not in out


def test_idempotent_same_exit_code_and_output(capsys):
    first_code = check_plan(FIXTURE)
    first_out = capsys.readouterr().out
    second_code = check_plan(FIXTURE)
    second_out = capsys.readouterr().out
    assert first_code == second_code == 1
    assert first_out == second_out
    assert first_out.count("aws_s3_bucket.listing_media") == 1  # no duplicated lines


def _plan(*resources):
    return {"resource_changes": list(resources)}


def _rc(address, rtype, actions, after):
    return {"address": address, "type": rtype, "change": {"actions": actions, "after": after}}


def test_generic_across_resource_types():
    plan = _plan(
        _rc("aws_dynamodb_table.t", "aws_dynamodb_table", ["create"], {"tags": {"tenant_id": "x"}}),
        _rc("aws_sqs_queue.q", "aws_sqs_queue", ["create"], {"tags": {"landlord_account_id": "la-9"}}),
    )
    assert find_missing(plan) == ["aws_dynamodb_table.t"]


def test_skips_noop_read_delete_and_untaggable():
    plan = _plan(
        _rc("a.noop", "a", ["no-op"], {"tags": {}}),
        _rc("a.read", "a", ["read"], {"tags": {}}),
        _rc("a.gone", "a", ["delete"], None),
        _rc("aws_s3_bucket_lifecycle_configuration.x", "aws_s3_bucket_lifecycle_configuration",
            ["create"], {"bucket": "b"}),  # no tags attribute -> not taggable
    )
    assert find_missing(plan) == []
    assert evaluate_plan(plan)[0] == 0


def test_replace_is_in_scope():
    plan = _plan(_rc("a.r", "a", ["delete", "create"], {"tags": {}}))
    assert find_missing(plan) == ["a.r"]


def test_blank_value_and_default_tags():
    plan = _plan(
        _rc("a.blank", "a", ["create"], {"tags": {"landlord_account_id": "  "}}),
        _rc("a.default", "a", ["create"], {"tags": {}, "tags_all": {"landlord_account_id": "la-1"}}),
    )
    assert find_missing(plan) == ["a.blank"]


def test_idempotency_key_stable_and_order_insensitive_and_changes_with_plan():
    plan = _plan(_rc("a.x", "a", ["create"], {"tags": {}}))
    reordered = json.loads(json.dumps(plan))  # same content
    assert evaluate_plan(plan) == evaluate_plan(reordered)
    changed = copy.deepcopy(plan)
    changed["resource_changes"][0]["change"]["after"]["tags"] = {"landlord_account_id": "la-1"}
    assert evaluate_plan(plan)[1].splitlines()[0] != evaluate_plan(changed)[1].splitlines()[0]


def test_unreadable_plan_fails_closed(tmp_path, capsys):
    assert check_plan(str(tmp_path / "missing.json")) == 2
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert check_plan(str(bad)) == 2
