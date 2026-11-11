import hashlib
import json
from pathlib import Path

import pytest
import yaml

from scripts import capsule_screen as screen
from scripts import pack_capsules


def context(retention):
    access = {
        "dropped": {"type": "closed", "license": "publisher"},
        "capped": {"type": "gold", "license": "CC-BY-NC-ND-4.0"},
        "full": {"type": "gold", "license": "CC-BY-SA-4.0"},
    }
    return screen.context_for("10.1234/synthetic", access[retention])


@pytest.mark.parametrize("prefix", ["", "asbval:", "another:", "https://example.org/vocab#", "https://example.org/vocab/"])
@pytest.mark.parametrize("key", sorted(screen.QUOTE_KEYS) + ["evidence_Quote"])
def test_quote_properties_resolve_to_local_names(prefix, key):
    source = {"@graph": [{prefix + key: "synthetic source", "note": "generated note"}]}
    result = screen.screen_text(json.dumps(source), "validation_assertions.jsonld", context("dropped"), screen.QuoteBudget())
    node = json.loads(result.text)["@graph"][0]
    assert node[prefix + key] == ""
    assert node["note"] == "generated note"
    anchor = node["_screen_redactions"][0]
    assert anchor["length"] == len("synthetic source")
    assert anchor["sha256"] == hashlib.sha256(b"synthetic source").hexdigest()
    assert anchor["redacted_reason"] == "access_closed"
    assert anchor["location"].startswith("validation_assertions.jsonld#/@graph/0/")
    assert result.quotes["count"] == result.quotes["characters"] == 0
    assert not result.failures


def test_jsonld_value_objects_and_quote_lists_keep_their_shape():
    payload = {"asbval:evidence_quote": {"@value": "synthetic source", "@language": "en"},
               "quote": ["first synthetic span", "second synthetic span"]}
    result = screen.screen_text(json.dumps(payload), "assertions.jsonld", context("dropped"), screen.QuoteBudget())
    output = json.loads(result.text)
    assert output["asbval:evidence_quote"]["@value"] == ""
    assert output["asbval:evidence_quote"]["@language"] == "en"
    assert set(output["asbval:evidence_quote"]) == {"@value", "@language"}
    assert output["quote"] == ["", ""]
    assert len(output["_screen_redactions"]) == 3
    assert not result.failures


@pytest.mark.parametrize("suffix", [".json", ".jsonld", ".jsonl", ".yaml", ".yml"])
def test_retrieved_passages_are_screened_by_position_and_documents_still_parse(suffix):
    payload = {"passages_used": [{"idx": 1, "text": "p" * 900, "is_substring_hit": False}],
               "substring_hits": [{"text": "retrieved synthetic source", "offset": 8}],
               "claims_checked": [{"claim_text": "generated claim", "note": "generated note"}],
               "text": "generated body", "value": "generated criterion",
               "other": [{"text": "dataset metadata"}], "asbval:target_claim_text": "generated claim"}
    text = yaml.safe_dump(payload) if suffix in {".yaml", ".yml"} else json.dumps(payload) + "\n"
    result = screen.screen_text(text, "capsules/task/validation" + suffix, context("dropped"), screen.QuoteBudget())
    output = yaml.safe_load(result.text) if suffix in {".yaml", ".yml"} else json.loads(result.text)
    assert output["passages_used"][0]["text"] == ""
    assert output["passages_used"][0]["idx"] == 1
    assert output["passages_used"][0]["is_substring_hit"] is False
    assert output["substring_hits"][0]["text"] == ""
    assert output["substring_hits"][0]["offset"] == 8
    assert output["text"] == payload["text"]
    assert output["other"] == payload["other"]
    assert output["value"] == payload["value"]
    assert output["claims_checked"] == payload["claims_checked"]
    assert output["asbval:target_claim_text"] == payload["asbval:target_claim_text"]
    assert len(output["passages_used"][0]["_screen_redactions"]) == 1
    assert not result.failures


def snippets(first, second):
    return ("# Evidence Snippets\n\n## ev_1\n\n- Source: document\n- Reason: generated reason\n\n"
            + first + "\n\n## ev_2\n\n- Source: document\n- Reason: generated reason\n\n" + second + "\n")


@pytest.mark.parametrize("retention,expected", [("dropped", 0), ("capped", 600), ("full", 1000)])
def test_plain_markdown_snippets_are_fields_with_anchors_and_preserved_metadata(retention, expected):
    text = snippets("a" * 400, "b" * 600)
    path = "capsules/task/evidence/source_snippets.md"
    result = screen.screen_text(text, path, context(retention), screen.QuoteBudget())
    assert result.quotes["characters"] == expected
    assert result.quotes["count"] == (0 if retention == "dropped" else 2)
    assert "- Reason: generated reason" in result.text
    assert "## ev_1" in result.text and "## ev_2" in result.text
    assert result.text.count("<!-- asb-redaction ") == (0 if retention == "full" else 2)
    assert not result.failures
    if retention == "full":
        assert result.text == text
    else:
        anchors = [json.loads(line.removeprefix("<!-- asb-redaction ").removesuffix(" -->"))
                   for line in result.text.splitlines() if line.startswith("<!-- asb-redaction ")]
        for anchor, original in zip(anchors, ("a" * 400, "b" * 600)):
            offsets = anchor["offsets"]
            assert text[offsets["start"]:offsets["end"]] == original
            assert anchor["sha256"] == hashlib.sha256(original.encode()).hexdigest()


def test_unstructured_source_snippet_member_is_screened_too():
    result = screen.screen_text("synthetic source paragraph", "evidence/source_snippets.md", context("dropped"), screen.QuoteBudget())
    assert "synthetic source paragraph" not in result.text
    assert "asb-redaction" in result.text
    assert result.quotes["characters"] == 0
    assert not result.failures


@pytest.mark.parametrize("paper_name", ["paper.md", "article_fulltext.md"])
@pytest.mark.parametrize("retention,expected", [("dropped", 0), ("capped", 300), ("full", 700)])
def test_paper_preview_fences_are_screened_while_dataset_previews_stay(retention, expected, paper_name):
    text = ("### `dataset.csv`\n```\ncolumn_a,column_b\n1,2\n```\n\n"
            f"### `{paper_name}`\n```\n" + "s" * 700 + "\n```\n\n"
            "### `paper_summary.md`\n```\nGenerated summary.\n```\n")
    result = screen.screen_text(text, "capsules/task/inputs/dataset_preview.md", context(retention), screen.QuoteBudget())
    assert result.quotes["characters"] == expected
    assert "column_a,column_b\n1,2" in result.text
    assert "Generated summary." in result.text
    assert result.text.count("```") == text.count("```")
    assert not result.failures
    if retention == "full":
        assert result.text == text
    else:
        assert result.text.count("<!-- asb-redaction ") == 1


def test_paper_preview_internal_fences_and_headings_do_not_end_the_source_field():
    body = ("Synthetic paper start.\n### `example.py`\n```python\ninternal example\n```\n"
            "### `term`\nSynthetic paper end.")
    text = "### `paper.md`\n```\n" + body + "\n```\n\n### `data.csv`\n```\nx,y\n```\n"
    relative = "inputs/dataset_preview.md"
    assert list(screen.source_text_values(text, relative)) == [body]
    result = screen.screen_text(text, relative, context("dropped"), screen.QuoteBudget())
    assert "Synthetic paper" not in result.text
    assert "internal example" not in result.text
    assert "x,y" in result.text
    assert result.quotes["characters"] == 0
    assert not result.failures


def test_dropped_markdown_blockquote_markers_are_not_counted_as_source_text():
    result = screen.screen_text("> synthetic source\n> continuation\n\nGenerated commentary\n",
                                "ledger/evidence.md", context("dropped"), screen.QuoteBudget())
    assert "> [redacted-quote]" in result.text
    assert "Generated commentary" in result.text
    assert result.quotes == {"count": 0, "characters": 0, "longest": 0, "truncated": 0, "dropped": 1}
    assert not result.failures


def test_one_doi_budget_is_shared_by_every_member_and_source_representation(tmp_path):
    members = {
        "capsules/task-a/evidence/source_snippets.md": snippets("a" * 500, "b" * 500),
        "capsules/task-a/validation.json": json.dumps({"passages_used": [{"text": "c" * 500}]}),
        "capsules/task-b/ledger/claims.yaml": yaml.safe_dump({"source_excerpt": "d" * 500}),
        "ledger/claims.jsonl": json.dumps({"quote": "e" * 500}) + "\n",
        "validation_assertions.jsonld": json.dumps({"@graph": [{"asbval:evidence_quote": "f" * 500}]}),
    }
    for relative, text in members.items():
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    paper = {"doi": "10.1234/synthetic", "access": {"type": "gold", "license": "CC-BY-NC-4.0"}}
    receipt, capsules = pack_capsules.screen_build(tmp_path, paper, {}, {"deny_patterns": (), "private_repositories": ()})
    assert receipt["failures"] == []
    assert receipt["quotes_after_screen"] == {"count": 5, "characters": 1500, "longest": 300, "truncated": 5, "dropped": 1}
    assert capsules["task-a"]["characters"] == 900
    assert capsules["task-b"]["characters"] == 300
    assert json.loads((tmp_path / "validation_assertions.jsonld").read_text())["@graph"][0]["asbval:evidence_quote"] == ""


@pytest.mark.parametrize("retention", ["capped", "full"])
def test_receipts_measure_the_output_after_privacy_replacements(retention):
    source = json.dumps({"quote": "a@b.co " * 80})
    budget = screen.QuoteBudget()
    result = screen.screen_text(source, "ledger/claims.json", context(retention), budget)
    actual = json.loads(result.text)["quote"]
    assert result.quotes["characters"] == result.quotes["longest"] == len(actual)
    if retention == "capped":
        assert len(actual) <= 300
        assert budget.retained == len(actual)
    assert not result.failures


def bypass_screen(text, relative_path, context, budget, capsule_dir=None):
    return screen.ScreenResult(text, screen.empty_counts(), screen.empty_quotes(), [])


def test_packer_leaves_out_a_build_when_post_screen_verification_finds_source_text(tmp_path, monkeypatch):
    monkeypatch.setattr(screen, "screen_text", bypass_screen)
    source = Path(__file__).parent / "fixtures/capsules/view/build__coll_closed"
    stage, out = tmp_path / "stage", tmp_path / "out"
    stage.mkdir()
    out.mkdir()
    paper = {"doi": "10.1234/synthetic", "access": {"type": "closed", "license": "publisher"}}
    entry, _, receipt = pack_capsules.pack_one(source, stage, out, paper, {},
                                              {"with_indicium": False, "deny_patterns": (), "private_repositories": ()})
    assert any("residual_source_text" in failure for failure in receipt["failures"])
    assert receipt["quotes_after_screen"]["characters"] > 0
    assert entry["sha256"] is None and entry["bytes"] == 0
    assert not list(out.rglob("*.zip"))


def test_post_screen_verification_checks_the_total_even_if_every_field_is_under_cap(tmp_path, monkeypatch):
    monkeypatch.setattr(screen, "screen_text", bypass_screen)
    for index in range(6):
        (tmp_path / f"{index}.json").write_text(json.dumps({"quote": "x" * 300}))
    paper = {"doi": "10.1234/synthetic", "access": {"type": "gold", "license": "other-oa"}}
    receipt, _ = pack_capsules.screen_build(tmp_path, paper, {}, {"deny_patterns": (), "private_repositories": ()})
    assert receipt["quotes_after_screen"]["characters"] == 1800
    assert any("quotation_doi_cap_exceeded" in failure for failure in receipt["failures"])


def test_post_screen_verification_checks_the_individual_field_cap():
    measured, failures = screen.verify_quote_policy(json.dumps({"quote": "x" * 301}), "ledger/x.json", context("capped"), screen.QuoteBudget())
    assert measured["characters"] == 301
    assert failures == ["ledger/x.json: quotation_field_cap_exceeded"]


@pytest.mark.parametrize("licence", [
    "CC-BY", "cc-by-1.0", "CC-BY-4.0", "CC-BY-SA", "CC-BY-SA-2.5", "CC BY SA 4.0",
    "CC0", "CC0-1.0", "public-domain", "public_domain",
    "https://creativecommons.org/licenses/by/4.0/", "https://creativecommons.org/licenses/by-sa/3.0/",
    "https://creativecommons.org/publicdomain/zero/1.0/",
])
def test_explicit_permissive_licence_classes(licence):
    assert screen.context_for("10.1234/synthetic", {"type": "gold", "license": licence}).retention == "full"


@pytest.mark.parametrize("licence", [
    "cc-by-nc", "CC-BY-NC-4.0", "cc-by-nd", "CC-BY-ND-4.0", "cc-by-nc-nd", "CC-BY-NC-ND-4.0",
    "cc-by-nc-sa", "CC-BY-NC-SA-3.0", "cc-by-unrecognised", "publisher", "other-oa",
    "https://creativecommons.org/licenses/by-nc/4.0/",
    "https://creativecommons.org/licenses/by-nd/4.0/",
])
def test_nonpermissive_open_licences_are_capped(licence):
    assert screen.context_for("10.1234/synthetic", {"type": "gold", "license": licence}).retention == "capped"


@pytest.mark.parametrize("value", [
    r"C:\Users\synthetic\file.txt", "C:/Users/synthetic/file.txt",
    r"D:\Documents and Settings\synthetic\file.txt", "D:/Documents and Settings/synthetic/file.txt",
    r"c:\users\synthetic\file.txt",
])
def test_only_home_directories_on_windows_drives_are_machine_paths(value):
    for text, relative in ((value, "note.txt"), (json.dumps({"value": value}), "note.json")):
        result = screen.screen_text(text, relative, context("full"), screen.QuoteBudget())
        assert "urn:asb:build:" in result.text
        assert result.counts["paths_rewritten"] == 1
        assert not result.failures


@pytest.mark.parametrize("value", [
    r"X:\mathbb{R}", r"x:\quad y = 2", r"C:\outputs\synthetic\file.txt", "D:/data/file.txt",
    'mydir="D:/ My Folder/data"', "a Windows D:/ path",
])
def test_nonhome_drive_paths_and_latex_are_left_as_written(value):
    for text, relative in ((value, "note.txt"), (json.dumps({"value": value}), "note.json")):
        result = screen.screen_text(text, relative, context("full"), screen.QuoteBudget())
        assert (json.loads(result.text)["value"] if relative.endswith("json") else result.text) == value
        assert result.counts["paths_rewritten"] == 0
        assert not result.failures
