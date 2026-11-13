import base64
import json
import pytest

from scripts import capsule_screen as screen
from scripts.release_gate import _build_email_allowlist


def context(access="gold", licence="other-oa", deny=()):
    result = screen.context_for("10.1234/example.open", {"type": access, "license": licence})
    result.email_allowlist, result.email_role = _build_email_allowlist({})
    result.deny_patterns = tuple(deny)
    return result


def test_open_quotes_under_a_non_permissive_licence_share_the_doi_budget_and_keep_anchors():
    source = json.dumps({"source_excerpt": "a" * 350, "nested": {"quote": "b" * 1400}})
    assert context().retention == "capped"
    result = screen.screen_text(source, "ledger/claims.json", context(), screen.QuoteBudget())
    payload = json.loads(result.text)
    assert len(payload["source_excerpt"]) == 300
    assert len(payload["nested"]["quote"]) == 300
    assert result.counts["spans_truncated"] == 2
    assert payload["_screen_redactions"][0]["redacted_reason"] == "quotation_cap"
    assert payload["nested"]["_screen_redactions"][0]["redacted_reason"] == "quotation_cap"
    assert screen.QuoteBudget(1500).allowance() == 0


@pytest.mark.parametrize(
    ("access", "licence"),
    [("gold", "CC-BY-4.0"), ("gold", "cc-by"), ("green", "cc-by-sa"), ("gold", "cc0"), ("diamond", "public-domain")],
)
def test_open_permissive_sources_keep_the_full_attributed_text(access, licence):
    rule = context(access, licence)
    assert rule.retention == "full"
    source = json.dumps({"source_excerpt": "a" * 350, "nested": {"quote": "b" * 1400}})
    budget = screen.QuoteBudget()
    result = screen.screen_text(source, "ledger/claims.json", rule, budget)
    payload = json.loads(result.text)
    assert len(payload["source_excerpt"]) == 350
    assert len(payload["nested"]["quote"]) == 1400
    assert "_screen_redactions" not in payload
    assert result.counts["spans_truncated"] == 0
    assert result.counts["spans_dropped"] == 0
    assert result.quotes == {"count": 2, "characters": 1750, "longest": 1400, "truncated": 0, "dropped": 0}
    assert budget.retained == 0


def test_explicit_reuse_grant_lifts_the_caps_and_a_missing_licence_still_drops():
    granted = screen.context_for("10.1234/example.open", {"type": "gold", "license": "other-oa", "reuse_grant": True})
    assert granted.retention == "full"
    assert screen.context_for("10.1234/example.open", {"type": "green", "license": None}).retention == "dropped"


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


@pytest.mark.parametrize("text", [
    "fragments at m/z 301.1410 303.1567 305.1723 were kept",
    "axis ticks 0 100 200 300 400 500",
    "knowledge base asb-paper-10-1101-2024-10-31-621429",
    "seasons 2019-2020-2021",
    "Anal. Chem. (2019) 91 4346-4356",
    "J. Sep. Sci. 44 (12) 2345-2356",
    "the phone line is described below\nvalues 100 200 300 400",
    "a telephone survey of 1200 households, then 100 200 300",
])
def test_digit_groups_without_a_phone_cue_are_numeric_data(text):
    for value, name in ((text, "evidence/note.txt"), (json.dumps({"v": text}), "ledger/note.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert "[redacted-phone]" not in result.text
        assert result.counts["phones_redacted"] == 0
        assert not result.failures


@pytest.mark.parametrize(("text", "expected"), [
    ("call +33 493 001 234 for access", 1),
    ("office (555) 123-4567", 1),
    ("office (01865) 270 000 or (020) 7946 0958", 2),
    ("Tel: 555-123-4567", 1),
    ("Tél. : 04 92 07 61 00", 1),
    ("Fax 0044 20 7946 0958", 1),
    ("Telephone number: 0123456789", 1),
    ("Phone: 555 123 4567, 555 987 6543", 2),
])
def test_a_phone_number_with_a_cue_is_redacted(text, expected):
    for value, name in ((text, "evidence/note.txt"), (json.dumps({"v": text}), "ledger/note.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert result.counts["phones_redacted"] == expected
        assert not any(character.isdigit() for character in result.text.replace("\\u00e9", ""))
        assert not result.failures


@pytest.mark.parametrize("path", [
    "/Users/example/outputs/demo/ledger/a.json",
    "/Volumes/data/outputs/demo/evidence/a.md",
    "/private/tmp/outputs/demo/input.txt",
    "/tmp/outputs/demo/input.txt",
    "/var/folders/ab/outputs/demo/input.txt",
    "file:///Users/example/outputs/demo/input.txt",
    r"C:\Users\example\outputs\demo\input.txt",
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


def test_a_bare_file_scheme_in_prose_is_not_a_residual_path():
    text = "Running locally from file:// requires modified browser settings."
    result = screen.screen_text(text, "workflow.yaml", context(), screen.QuoteBudget())
    assert result.text == text
    assert not result.failures
    hosted = screen.screen_text("see file://server/share/data.txt", "workflow.yaml", context(), screen.QuoteBudget())
    assert hosted.failures == ["workflow.yaml: residual_paths_rewritten"]


@pytest.mark.parametrize("text", [
    "Improved handling of local `file://` repositories in `install()`.",
    "Browsers restrict **file://** pages.",
    r"d.get(\'file://\' + os.path.abspath(page))",
    "an empty location is written file:///. in the example",
])
def test_a_file_scheme_closed_by_markup_or_quoting_is_not_a_residual_path(text):
    for value, name in ((text, "evidence/p.md"), (json.dumps({"v": text}), "ledger/p.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert json.loads(result.text)["v"] == text if name.endswith(".json") else result.text == text
        assert not result.failures


@pytest.mark.parametrize(("text", "locator"), [
    ("pyfaidx @ file:///opt/conda/conda-bld/pyfaidx_1728570107633/work Pygments", "urn:asb:build:work"),
    ("##reference=file:///data/ref/ref.fasta", "urn:asb:build:ref.fasta"),
    ('location="file:///C:/converters/ADH071030_002">', "urn:asb:build:ADH071030_002"),
])
def test_a_local_file_uri_is_rewritten_whatever_its_root(text, locator):
    for value, name in ((text, "evidence/p.txt"), (json.dumps({"v": text}), "ledger/p.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert locator in result.text
        assert "file:///" not in result.text and "/opt/" not in result.text and "/data/" not in result.text
        assert result.counts["paths_rewritten"] == 1
        assert not result.failures


@pytest.mark.parametrize("text", [
    "directory=/home/{USER_NAME}/{PATH_TO_FOLDER}/daemon",
    "sam=f'/tmp/{{ds}}_{{dec}}.sam'",
    'outdir = "/tmp/{task_id}_sirius"',
    "sras are downloaded to /home/[USER]/ncbi/public/sra/ by default",
    r"move the folder to C:\Users\[$UserName]\AppData\Local\R\win-library\ to install",
    'the folder "C:/Users/"username"/AppData/Roaming/" in windows, "/Users/"username"/Library/" on macOS',
])
def test_a_generic_placeholder_after_a_root_is_not_a_machine_path(text):
    for value, name in ((text, "evidence/p.md"), (json.dumps({"v": text}), "ledger/p.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert json.loads(result.text)["v"] == text if name.endswith(".json") else result.text == text
        assert result.counts["paths_rewritten"] == 0
        assert not result.failures


def test_a_descriptor_written_as_a_plain_file_is_repaired(tmp_path):
    from scripts.release_capsule_truth import crate_problems

    capsule = tmp_path / "capsule"
    capsule.mkdir()
    (capsule / "eval.json").write_text("{}\n")
    crate = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {"@id": "ro-crate-metadata.json", "@type": "File", "encodingFormat": "application/json",
             "name": "ro-crate-metadata.json"},
            {"@id": "./", "@type": "Dataset", "name": "capsule", "description": "d", "datePublished": "2026-11-09",
             "license": {"@id": "https://creativecommons.org/licenses/by/4.0/"}},
        ],
    }
    result = screen.screen_text(
        json.dumps(crate), "ro-crate-metadata.json", context(), screen.QuoteBudget(), capsule
    )
    descriptor = {entity["@id"]: entity for entity in json.loads(result.text)["@graph"]}["ro-crate-metadata.json"]
    assert descriptor["@type"] == "CreativeWork"
    assert descriptor["about"] == {"@id": "./"}
    assert "encodingFormat" not in descriptor
    assert not result.failures
    (capsule / "ro-crate-metadata.json").write_text(result.text)
    assert "the descriptor is not about ./" not in crate_problems(capsule)


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


def test_blockquotes_of_a_permissive_open_source_are_kept_whole():
    text = "> " + "x" * 350 + "\n> continuation\n"
    result = screen.screen_text(text, "evidence/span.md", context("gold", "CC-BY-4.0"), screen.QuoteBudget())
    assert result.text == text
    assert "asb-redaction" not in result.text
    assert result.quotes["characters"] == 363


def test_invalid_structured_text_is_a_failure():
    result = screen.screen_text("{bad", "ledger/bad.json", context(), screen.QuoteBudget())
    assert result.failures
    assert result.counts["failures"] == 1


@pytest.mark.parametrize(("value", "expected"), [
    ("line one\nperson@example.org", "line one\n[redacted-email]"),
    ('run "/Users/example/outputs/demo/a.txt" now', 'run "urn:asb:build:demo/a.txt" now'),
    ("/Users/example/outputs/demo/a.txt\nnext line", "urn:asb:build:demo/a.txt\nnext line"),
    ("x?b:\"\":c", "x?b:\"\":c"),
])
def test_json_strings_are_screened_decoded_so_escapes_survive(value, expected):
    result = screen.screen_text(json.dumps({"note": value}), "ledger/note.json", context(), screen.QuoteBudget())
    assert json.loads(result.text) == {"note": expected}
    assert not result.failures


def test_escaped_slashes_in_json_source_are_decoded_before_the_path_rewrite():
    source = '{"path": "\\/Users\\/example\\/outputs\\/demo\\/a.txt"}'
    result = screen.screen_text(source, "ledger/path.json", context(), screen.QuoteBudget())
    assert json.loads(result.text) == {"path": "urn:asb:build:demo/a.txt"}
    assert result.counts["paths_rewritten"] == 1
    assert not result.failures


def test_json_lines_are_screened_per_decoded_value():
    source = json.dumps({"a": "x\nperson@example.org"}) + "\n" + json.dumps({"b": "/tmp/abc123/file\nnext"}) + "\n"
    result = screen.screen_text(source, "ledger/rows.jsonl", context(), screen.QuoteBudget())
    rows = [json.loads(line) for line in result.text.splitlines()]
    assert rows == [{"a": "x\n[redacted-email]"}, {"b": "urn:asb:build:file\nnext"}]
    assert not result.failures


@pytest.mark.parametrize("suffix", [".json", ".yaml"])
def test_a_path_as_a_mapping_key_is_rewritten(suffix):
    payload = {"/Users/example/outputs/demo/a.txt": 1}
    text = json.dumps(payload) if suffix == ".json" else "/Users/example/outputs/demo/a.txt: 1\n"
    result = screen.screen_text(text, f"ledger/keys{suffix}", context(), screen.QuoteBudget())
    assert "urn:asb:build:demo/a.txt" in result.text
    assert "/Users/" not in result.text
    assert result.counts["paths_rewritten"] == 1
    assert not result.failures


def test_a_yaml_line_continuation_after_a_drive_shaped_token_is_kept():
    text = 'note: "the correlation r:\\\n  0.9 was high"\n'
    result = screen.screen_text(text, "workflow.yaml", context(), screen.QuoteBudget())
    assert result.text == text
    assert not result.failures


def test_a_yaml_comment_with_a_path_is_not_kept_verbatim():
    text = "# built in /Users/example/outputs/demo\nkey: value\n"
    result = screen.screen_text(text, "workflow.yaml", context(), screen.QuoteBudget())
    assert "/Users/" not in result.text
    assert not result.failures


@pytest.mark.parametrize("text", [
    "Write log-files in the /tmp/ directory.",
    "sort -T /tmp/<filename>.sorted input",
    "run with --errors_dir test/tmp/ set",
    "export TMPDIR=/scratch/tmp/run1",
    "files under data/home/run1 and the /home/ directory",
    'mydir="D:/ My Folder/data"',
    "a Windows D:/ path",
])
def test_text_that_names_no_machine_path_is_left_alone(text):
    for suffix in (".md", ".txt"):
        result = screen.screen_text(text, f"evidence/prose{suffix}", context(), screen.QuoteBudget())
        assert result.text == text
        assert result.counts["paths_rewritten"] == 0
        assert not result.failures
    structured = screen.screen_text(json.dumps({"v": text}), "ledger/prose.json", context(), screen.QuoteBudget())
    assert json.loads(structured.text) == {"v": text}
    assert not structured.failures


@pytest.mark.parametrize("path", [
    "/Users/example/a/b",
    "/private/tmp/x/y",
    "/tmp/abc123/file",
    "/home/example/run/out.txt",
    "/home/$USER/run/out.txt",
    "/var/folders/ab/cd/T/x",
    "file:///Users/example/x",
    r"C:\Users\n\file",
    "/System/Volumes/Data/Users/n/x",
])
def test_machine_paths_are_rewritten_in_text_and_in_json(path):
    for text, name in ((f"see {path} here", "evidence/p.txt"), (json.dumps({"v": f"see {path} here"}), "ledger/p.json")):
        result = screen.screen_text(text, name, context(), screen.QuoteBudget())
        assert "urn:asb:build:" in result.text
        assert not screen.RESIDUAL_PATH_RE.search(result.text.replace("\\\\", "\\"))
        assert result.counts["paths_rewritten"] == 1
        assert not result.failures


@pytest.mark.parametrize("text", [
    "/tmp/,secret",
    'cp /tmp/"private file"/x out',
    "/Users/[example]/secret",
    "/home/[alice]/secret",
    "/Users/person@example.org/out.txt",
])
def test_a_root_marker_the_rewrite_cannot_handle_leaves_the_build_out(text):
    for value, name in ((text, "evidence/p.txt"), (json.dumps({"v": text}), "ledger/p.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert f"{name}: residual_paths_rewritten" in result.failures


@pytest.mark.parametrize(("text", "rewrites"), [
    ("The path is **/tmp/abc123/note.txt**.", 1),
    ("<b>/tmp/abc123/note.txt</b>", 1),
    ("cc -I/home/example/include -L/tmp/abc123/lib", 2),
    ("open file:/tmp/abc123/note.txt now", 1),
    ("read /private/var/folders/ab/cd/T/note.txt", 1),
    ("read /root/run/note.txt", 1),
    ("read $(pwd)/tmp/abc123/note.txt", 1),
])
def test_a_machine_path_next_to_markup_or_an_option_is_rewritten(text, rewrites):
    for value, name in ((text, "evidence/p.md"), (json.dumps({"v": text}), "ledger/p.json")):
        result = screen.screen_text(value, name, context(), screen.QuoteBudget())
        assert result.counts["paths_rewritten"] == rewrites
        assert "abc123" not in result.text and "example" not in result.text and "/root/" not in result.text
        assert not result.failures


@pytest.mark.parametrize("text", [
    "profile://tmp is a scheme of its own",
    "data_C:/x is one word",
])
def test_a_scheme_or_drive_inside_a_longer_word_is_not_a_path(text):
    result = screen.screen_text(text, "evidence/p.txt", context(), screen.QuoteBudget())
    assert result.text == text
    assert not result.failures


def test_yaml_sets_and_pairs_are_screened_and_written_in_a_stable_order():
    text = (
        "paths: !!set\n  ? /Users/example/run/b.txt\n  ? zeta\n  ? alpha\n"
        "ordered: !!omap\n  - first: /Users/example/run/a.txt\n"
        "pairs: !!pairs\n  - contact: person@example.org\n"
    )
    result = screen.screen_text(text, "workflow.yaml", context(), screen.QuoteBudget())
    assert "/Users/" not in result.text and "person@example.org" not in result.text
    assert result.counts["paths_rewritten"] == 2
    assert result.counts["emails_redacted"] == 1
    assert not result.failures
    # A set is written as a list, in the order of its source values.
    assert screen.yaml.safe_load(result.text)["paths"] == ["urn:asb:build:b.txt", "alpha", "zeta"]


def test_a_yaml_binary_value_that_hides_a_path_leaves_the_build_out():
    blob = base64.b64encode(b"see /Users/example/run/a.txt").decode()
    result = screen.screen_text(f"blob: !!binary {blob}\n", "workflow.yaml", context(), screen.QuoteBudget())
    assert "workflow.yaml: residual_paths_rewritten" in result.failures


def test_two_keys_that_screen_to_the_same_key_fail_instead_of_losing_a_value():
    source = json.dumps({"a@example.org": 1, "b@example.org": 2})
    result = screen.screen_text(source, "ledger/x.json", context(), screen.QuoteBudget())
    assert "ledger/x.json: parse_RewrittenKeyCollision" in result.failures


@pytest.mark.parametrize(("text", "failure"), [
    ("1: one\n2: two\n", None),
    ("a: &a\n  b: *a\n", "workflow.yaml: parse_RecursionError"),
])
def test_unusual_yaml_is_screened_or_failed_never_raised(text, failure):
    result = screen.screen_text(text, "workflow.yaml", context(), screen.QuoteBudget())
    assert result.failures == ([failure] if failure else [])


def test_a_document_with_its_own_redaction_field_of_the_wrong_type_fails_instead_of_raising():
    source = json.dumps({"_screen_redactions": "text", "quote": "source words"})
    result = screen.screen_text(source, "evidence/claim.json", context("closed", "publisher"), screen.QuoteBudget())
    assert "evidence/claim.json: parse_AttributeError" in result.failures


@pytest.mark.parametrize("text", [
    "Email: jane.roe@inst.example.cat 2 Institute of Space Studies",
    "Contact: jroe@lab.example.club for the data",
    "Email:j.roe@stud.example-uni.deJane Roe Affiliation: Department of Physics",
    "Mastodon @tool@host.example.club",
    "write to a.person@group.example.science",
])
def test_an_address_at_a_root_zone_domain_is_redacted_whatever_follows_it(text):
    """The R slot exception must not keep an address because its top-level domain is not on a short list."""
    result = screen.screen_text(text, "anchor_corpus/article.txt", context(), screen.QuoteBudget())
    assert "[redacted-email]" in result.text
    assert result.counts["emails_redacted"] == 1


@pytest.mark.parametrize("text", [
    "metadata <- seurat_obj@meta.data",
    "name <- pbmc@project.name",
    "idents <- obj@active.ident",
    "git clone git@github.example.club:group/project.git",
    "template: your.name@lab.example.club",
    "peak@xxx.xx",
])
def test_slot_notation_and_documented_templates_are_still_left_alone(text):
    result = screen.screen_text(text, "anchor_corpus/repo.txt", context(), screen.QuoteBudget())
    assert result.text == text
    assert result.counts["emails_redacted"] == 0


def test_the_root_zone_file_holds_the_generic_labels_the_short_list_missed_and_not_the_slot_ones():
    labels = screen.root_zone_labels()
    assert {"cat", "club", "com", "de", "science", "tools"} <= labels
    assert not labels & screen.SLOT_LAST_LABELS
