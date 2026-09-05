"""The dormant local skill-load counter (INT-ASB-010, R10).

`docs/design/skill-load-telemetry.md` specifies a network beacon, and that
beacon is blocked on a GDPR audit by CNRS legal counsel. The audit is the
reason to be careful, so the half that ships now is the half that transfers
nothing: an in-process counter that writes one local file, only when
`ASB_SKILLS_USAGE_PATH` names one.

A telemetry feature is only as trustworthy as the tests that pin what it does
*not* do, so most of this file is about absences — and an absence proves
nothing unless the check that looks for it can be shown to fire. Every negative
here is therefore two-sided: the same detector that finds no username, no
network call and no query string in the real artefact is run against a
deliberately contaminated one and must find it there.
"""

import json
import os
import platform
import re
import socket
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

server = pytest.importorskip(
    "asb_skill_collections.asb_mcp_server",
    reason="the MCP server needs the 'mcp' extra",
)

SLUG = "placeholder-procedure"
BODY = "---\nname: placeholder-procedure\n---\n\n# placeholder\n"


@pytest.fixture(autouse=True)
def _counter_off_unless_a_test_turns_it_on(monkeypatch):
    """No test inherits an enabled counter from the ambient environment."""
    monkeypatch.delenv(server.USAGE_PATH_ENV, raising=False)


@pytest.fixture
def usage_file(tmp_path, monkeypatch):
    path = tmp_path / "usage" / "usage.json"
    monkeypatch.setenv(server.USAGE_PATH_ENV, str(path))
    return path


@pytest.fixture
def found_skill(monkeypatch):
    """Serve a placeholder body, so no test depends on a shipped collection."""
    monkeypatch.setattr(server.idx, "get_item_text", lambda *a, **k: BODY)


def _records(path):
    return json.loads(path.read_text(encoding="utf-8"))["records"]


# --------------------------------------------------------------------------- #
# Off by default.                                                              #
# --------------------------------------------------------------------------- #
def test_the_counter_is_off_without_the_environment_variable(tmp_path):
    assert server.usage_path() is None
    assert server.record_skill_load(SLUG, "get_skill") is False
    assert list(tmp_path.iterdir()) == []


def test_an_empty_variable_is_still_off(monkeypatch):
    """`ASB_SKILLS_USAGE_PATH=` and `= ` are unset, not a file named ''."""
    for value in ("", "   "):
        monkeypatch.setenv(server.USAGE_PATH_ENV, value)
        assert server.usage_path() is None
        assert server.record_skill_load(SLUG, "get_skill") is False


def test_fetching_a_skill_writes_nothing_while_the_counter_is_off(tmp_path, found_skill):
    assert server.get_skill(SLUG, "placeholder/v1") == BODY
    assert list(tmp_path.iterdir()) == []


def test_the_switch_is_the_only_thing_between_off_and_on(usage_file, found_skill):
    """Two-sided: the same call that wrote nothing above writes a record here."""
    server.get_skill(SLUG, "placeholder/v1")
    assert usage_file.is_file()
    assert _records(usage_file)[0]["skill_slug"] == SLUG


# --------------------------------------------------------------------------- #
# The designed schema.                                                         #
# --------------------------------------------------------------------------- #
def test_a_record_carries_exactly_the_designed_fields(usage_file):
    assert server.record_skill_load(SLUG, "get_skill") is True
    doc = json.loads(usage_file.read_text(encoding="utf-8"))
    assert doc["schema_version"] == server.USAGE_SCHEMA_VERSION
    assert sorted(doc) == ["records", "schema_version"]
    (record,) = doc["records"]
    assert sorted(record) == sorted(server.USAGE_FIELDS)
    assert record == {
        "skill_slug": SLUG,
        "tool_name": "get_skill",
        "count": 1,
        "first_seen": record["last_seen"],
        "last_seen": record["last_seen"],
    }


def test_the_designed_field_list_is_the_five_the_spec_names(usage_file):
    assert set(server.USAGE_FIELDS) == {
        "skill_slug",
        "tool_name",
        "count",
        "first_seen",
        "last_seen",
    }


def test_repeated_loads_increment_one_record_and_move_last_seen(usage_file, monkeypatch):
    monkeypatch.setattr(server, "_utc_hour", lambda: "2026-09-05T09:00:00+00:00")
    server.record_skill_load(SLUG, "get_skill")
    monkeypatch.setattr(server, "_utc_hour", lambda: "2026-09-05T14:00:00+00:00")
    server.record_skill_load(SLUG, "get_skill")

    (record,) = _records(usage_file)
    assert record["count"] == 2
    assert record["first_seen"] == "2026-09-05T09:00:00+00:00"
    assert record["last_seen"] == "2026-09-05T14:00:00+00:00"


def test_records_are_keyed_by_skill_and_tool(usage_file):
    server.record_skill_load(SLUG, "get_skill")
    server.record_skill_load(SLUG, "get_workflow")
    server.record_skill_load("other-procedure", "get_skill")
    keys = {(r["skill_slug"], r["tool_name"]) for r in _records(usage_file)}
    assert keys == {
        (SLUG, "get_skill"),
        (SLUG, "get_workflow"),
        ("other-procedure", "get_skill"),
    }


def test_timestamps_are_hour_resolution(usage_file):
    """The design's privacy stance: a sequence of records must not rebuild a session."""
    server.record_skill_load(SLUG, "get_skill")
    (record,) = _records(usage_file)
    for field in ("first_seen", "last_seen"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:00:00\+00:00", record[field]), record[field]


# --------------------------------------------------------------------------- #
# What it counts, and what it refuses to.                                      #
# --------------------------------------------------------------------------- #
def test_a_missing_skill_is_not_a_load(usage_file, monkeypatch):
    monkeypatch.setattr(server.idx, "get_item_text", lambda *a, **k: None)
    assert server.get_skill(SLUG, "placeholder/v1").startswith("NOT FOUND")
    assert not usage_file.exists()


def test_get_workflow_counts_under_its_own_tool_name(usage_file, found_skill):
    server.get_workflow(SLUG, "placeholder/v1")
    (record,) = _records(usage_file)
    assert record["tool_name"] == "get_workflow"


def test_searching_records_nothing(usage_file, monkeypatch):
    """A search is distinguished only by the user's own words; those are not ours."""
    monkeypatch.setattr(server.idx, "search", lambda *a, **k: [{"slug": SLUG}])
    server.search_skills("a query with the user's own words in it")
    server.search_workflows("another query")
    server.search_tools("a third")
    assert not usage_file.exists()


# --------------------------------------------------------------------------- #
# No identifier — and the detector that says so can find one.                  #
# --------------------------------------------------------------------------- #
def _identifiers() -> dict:
    ids = {"pid": str(os.getpid()), "user": os.environ.get("USER") or ""}
    node = platform.node()
    if node:
        ids["host"] = node
    return {k: v for k, v in ids.items() if v}


def test_the_written_file_carries_no_identifier(usage_file, found_skill):
    server.get_skill(SLUG, "placeholder/v1")
    text = usage_file.read_text(encoding="utf-8")
    found = {k: v for k, v in _identifiers().items() if v in text}
    assert not found, f"the usage file leaks {found}"
    for banned in ("session", "user", "host", "pid", "ip", "query", "path"):
        assert banned not in text.lower(), f"the usage file mentions {banned!r}"


def test_the_identifier_detector_actually_detects(usage_file):
    """Two-sided: the same scan run over a contaminated file must fail."""
    ids = _identifiers()
    assert ids, "no identifier available to test the detector with"
    usage_file.parent.mkdir(parents=True, exist_ok=True)
    usage_file.write_text(json.dumps({"records": [{"host": v} for v in ids.values()]}))
    text = usage_file.read_text(encoding="utf-8")
    assert {k: v for k, v in ids.items() if v in text} == ids


# --------------------------------------------------------------------------- #
# No network — with the socket module monkeypatched to fail.                   #
# --------------------------------------------------------------------------- #
@pytest.fixture
def no_network(monkeypatch):
    """Any attempt to reach the network raises, loudly."""

    def _refuse(*args, **kwargs):
        raise AssertionError("the MCP server must make no network call")

    for name in ("socket", "create_connection", "getaddrinfo", "gethostbyname"):
        monkeypatch.setattr(socket, name, _refuse, raising=False)
    return _refuse


def test_the_counter_works_with_the_socket_module_broken(usage_file, found_skill, no_network):
    assert server.get_skill(SLUG, "placeholder/v1") == BODY
    assert server.record_skill_load(SLUG, "get_workflow") is True
    assert len(_records(usage_file)) == 2


def test_the_server_still_serves_with_the_socket_module_broken(found_skill, no_network):
    """Off as well as on: neither path reaches for the network."""
    assert server.get_skill(SLUG, "placeholder/v1") == BODY
    assert server.get_workflow(SLUG, "placeholder/v1") == BODY


def test_the_no_network_fixture_is_not_a_no_op(no_network):
    """Two-sided: prove the trap is armed before trusting the tests above."""
    with pytest.raises(AssertionError):
        socket.create_connection(("127.0.0.1", 9))


NETWORK_IMPORTS = ("urllib", "requests", "httpx", "http.client", "socket", "aiohttp")


def test_the_server_module_imports_nothing_that_can_reach_the_network():
    source = pathlib.Path(server.__file__).read_text(encoding="utf-8")
    imports = re.findall(r"^\s*(?:import|from)\s+([\w.]+)", source, flags=re.MULTILINE)
    offenders = [m for m in imports if m.split(".")[0] in {n.split(".")[0] for n in NETWORK_IMPORTS}]
    assert not offenders, f"the server imports {offenders}"


def test_the_import_scan_actually_detects(tmp_path):
    contaminated = "import json\nimport urllib.request\nfrom requests import post\n"
    imports = re.findall(r"^\s*(?:import|from)\s+([\w.]+)", contaminated, flags=re.MULTILINE)
    offenders = [m for m in imports if m.split(".")[0] in {n.split(".")[0] for n in NETWORK_IMPORTS}]
    assert offenders == ["urllib.request", "requests"]


URL_RE = re.compile(r"\b(?:https?|ws|wss)://\S+")


def test_no_endpoint_url_appears_anywhere_in_the_server():
    """The beacon is deferred; an endpoint sitting in the source is half of one."""
    source = pathlib.Path(server.__file__).read_text(encoding="utf-8")
    assert URL_RE.findall(source) == []


def test_the_url_scan_actually_detects():
    assert URL_RE.findall(
        "POST https://telemetry.example.invalid/v1/skill-load"
    ) == ["https://telemetry.example.invalid/v1/skill-load"]


# --------------------------------------------------------------------------- #
# A counter that can break a skill lookup is worse than no counter.            #
# --------------------------------------------------------------------------- #
def test_a_corrupt_usage_file_is_replaced_rather_than_raising(usage_file):
    usage_file.parent.mkdir(parents=True, exist_ok=True)
    usage_file.write_text("{not json")
    assert server.record_skill_load(SLUG, "get_skill") is True
    assert _records(usage_file)[0]["count"] == 1


def test_an_unwritable_path_is_reported_not_raised(tmp_path, monkeypatch, found_skill):
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory")
    monkeypatch.setenv(server.USAGE_PATH_ENV, str(blocker / "usage.json"))
    assert server.record_skill_load(SLUG, "get_skill") is False
    assert server.get_skill(SLUG, "placeholder/v1") == BODY


def test_the_design_document_records_the_deferral():
    doc = (REPO_ROOT / "docs" / "design" / "skill-load-telemetry.md").read_text(encoding="utf-8")
    assert "DEFERRED" in doc
    assert "GDPR" in doc and "CNRS legal counsel" in doc
    assert server.USAGE_PATH_ENV in doc


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
