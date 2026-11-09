import json
import pytest

from scripts import capsule_screen as screen
from scripts.release_gate import _build_email_allowlist


def context(access="gold", licence="CC-BY-4.0", deny=()):
    result = screen.context_for("10.1234/example.open", {"type": access, "license": licence})
    result.email_allowlist, result.email_role = _build_email_allowlist({})
    result.deny_patterns = tuple(deny)
    return result


def test_open_quotes_share_the_doi_budget_and_keep_anchors():
    source = json.dumps({"source_excerpt": "a" * 350, "nested": {"quote": "b" * 1400}})
    result = screen.screen_text(source, "ledger/claims.json", context(), screen.QuoteBudget())
    payload = json.loads(result.text)
    assert len(payload["source_excerpt"]) == 300
    assert len(payload["nested"]["quote"]) == 300
    assert result.counts["spans_truncated"] == 2
    assert payload["_screen_redactions"][0]["redacted_reason"] == "quotation_cap"
    assert payload["nested"]["_screen_redactions"][0]["redacted_reason"] == "quotation_cap"
    assert screen.QuoteBudget(1500).allowance() == 0


@pytest.mark.parametrize("access", ["closed", "hybrid", "bronze", "unknown", "gold"])
def test_closed_unknown_and_licence_less_sources_drop_quote_text(access):
    licence = None if access == "gold" else "publisher"
    result = screen.screen_text(
        json.dumps({"quote": "source words"}),
        "evidence/claim.json",
        context(access, licence),
        screen.QuoteBudget(),
    )
    payload = json.loads(result.text)
    assert payload["quote"] == ""
    assert payload["_screen_redactions"][0]["sha256"]
    assert result.counts["spans_dropped"] == 1


def test_preprint_without_reuse_grant_has_zero_text_budget():
    access = {"type": "preprint", "license": "publisher"}
    assert screen.context_for("10.1234/example.preprint", access).drop_quotes


def test_pii_rules_keep_notation_role_addresses_and_redact_phone():
    text = "person@example.org peak@123.45 info@lab.example.org +33 493 001 234"
    result = screen.screen_text(text, "evidence/note.txt", context(), screen.QuoteBudget())
    assert "[redacted-email]" in result.text
    assert "peak@123.45" in result.text
    assert "info@lab.example.org" in result.text
    assert "[redacted-phone]" in result.text
    assert result.counts["emails_redacted"] == 1
    assert result.counts["phones_redacted"] == 1


@pytest.mark.parametrize("path", [
    "/Users/example/outputs/demo/ledger/a.json",
    "/Volumes/data/outputs/demo/evidence/a.md",
    "/private/tmp/outputs/demo/input.txt",
    "/tmp/outputs/demo/input.txt",
    "/var/folders/ab/outputs/demo/input.txt",
    "file:///Users/example/outputs/demo/input.txt",
    r"C:\outputs\demo\input.txt",
    "/Users/ < user name > /Optimus/bin/python",
])
def test_every_absolute_path_form_becomes_a_build_locator(path):
    result = screen.screen_text(path, "ledger/path.txt", context(), screen.QuoteBudget())
    assert result.text.startswith("urn:asb:build:")
    assert result.counts["paths_rewritten"] == 1
    assert not result.failures


def test_crate_pruning_uses_the_release_rule(tmp_path):
    capsule = tmp_path / "capsule"
    capsule.mkdir()
    (capsule / "eval.json").write_text("{}\n")
    crate = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "about": {"@id": "./"}},
            {"@id": "./", "@type": "Dataset", "hasPart": [{"@id": "build-only.json"}]},
            {"@id": "build-only.json", "@type": "File"},
            {"@id": "tool", "@type": "SoftwareApplication", "path": "/Users/example/outputs/demo/tool"},
        ],
    }
    result = screen.screen_text(
        json.dumps(crate), "ro-crate-metadata.json", context(), screen.QuoteBudget(), capsule
    )
    graph = json.loads(result.text)["@graph"]
    assert result.counts["crates_pruned"] == 0
    assert "build-only.json" not in {entity["@id"] for entity in graph}
    assert "eval.json" in {entity["@id"] for entity in graph}
    assert not result.failures


def test_deny_hits_are_counted_without_returning_the_pattern():
    rule = context()
    rule.deny_patterns = ("synthetic-secret",)
    result = screen.screen_text("SYNTHETIC-SECRET", "note.txt", rule, screen.QuoteBudget())
    assert result.counts["deny_hits"] == 1
    assert "synthetic-secret" not in " ".join(result.failures)


def test_blockquotes_are_screened_and_anchored():
    result = screen.screen_text(
        "> " + "x" * 350 + "\n> continuation\n", "evidence/span.md", context(), screen.QuoteBudget()
    )
    assert "asb-redaction" in result.text
    assert result.quotes["characters"] == 300


def test_invalid_structured_text_is_a_failure():
    result = screen.screen_text("{bad", "ledger/bad.json", context(), screen.QuoteBudget())
    assert result.failures
    assert result.counts["failures"] == 1
