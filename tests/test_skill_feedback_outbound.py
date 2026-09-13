"""The feedback helper exposes one fully redacted submission payload."""

from __future__ import annotations

import json

from scripts import skill_feedback as sf


COLLECTION_ONE = "/Users/reporter-one/code/asb/collections/metabolomics/v2"
COLLECTION_TWO = "/home/reporter-two/code/asb/collections/metabolomics/v2"
INSIDE_TARGET_ONE = f"{COLLECTION_ONE}/leaves/spectral-library-match/SKILL.md"
INSIDE_TARGET_TWO = f"{COLLECTION_TWO}/leaves/spectral-library-match/SKILL.md"
OUTSIDE_TARGET = "/Users/reporter-one/SecretStudy/Patient-42"
HOME_PATH = "/Users/reporter-one/SecretStudy/Patient-42/run.mzML"
OPENAI_TOKEN = "sk-DUMMY00000000000000"
GITHUB_TOKEN = "ghp_DUMMY00000000000000"
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
EMAIL = "alice@example.invalid"


def _payload_text(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_synthetic_values_absent(text: str) -> None:
    for value in (
        "/Users/reporter-one",
        "reporter-one",
        "SecretStudy",
        "Patient-42",
        OPENAI_TOKEN,
        GITHUB_TOKEN,
        AWS_KEY,
        EMAIL,
    ):
        assert value not in text


def test_every_submission_field_and_preview_are_redacted() -> None:
    report = sf.render_issue(
        kind="defect",
        target=INSIDE_TARGET_ONE,
        symptom=f"failed while reading {HOME_PATH}; token={OPENAI_TOKEN}",
        expected=f"retry without {GITHUB_TOKEN}",
        context=f"credentials {AWS_KEY}; contact {EMAIL}",
        collection=COLLECTION_ONE,
    )

    payload = report["payload"]
    assert report["preview"] is payload
    assert payload == {key: report[key] for key in ("title", "labels", "body")}
    assert _payload_text(report["preview"]) == _payload_text(payload)
    _assert_synthetic_values_absent(_payload_text(payload))
    assert "metabolomics/v2/leaves/spectral-library-match/SKILL.md" in report["body"]
    assert "path_prefix" in report["redacted"]


def test_an_absolute_target_outside_the_collection_is_removed_completely() -> None:
    report = sf.render_issue(
        "defect",
        OUTSIDE_TARGET,
        symptom="the documented command failed",
        collection=COLLECTION_ONE,
    )

    _assert_synthetic_values_absent(_payload_text(report["payload"]))
    assert OUTSIDE_TARGET not in report["title"]
    assert OUTSIDE_TARGET not in report["body"]
    assert "absolute_path" in report["redacted"]


def test_fingerprint_is_stable_across_reporter_home_paths() -> None:
    first = sf.render_issue(
        "defect",
        INSIDE_TARGET_ONE,
        symptom=f"the command failed on {COLLECTION_ONE}/inputs/run.mzML",
        collection=COLLECTION_ONE,
    )
    second = sf.render_issue(
        "defect",
        INSIDE_TARGET_TWO,
        symptom=f"the command failed on {COLLECTION_TWO}/inputs/run.mzML",
        collection=COLLECTION_TWO,
    )

    direct_first = sf.fingerprint(
        "defect",
        INSIDE_TARGET_ONE,
        f"the command failed on {COLLECTION_ONE}/inputs/run.mzML",
        collection=COLLECTION_ONE,
    )
    direct_second = sf.fingerprint(
        "defect",
        INSIDE_TARGET_TWO,
        f"the command failed on {COLLECTION_TWO}/inputs/run.mzML",
        collection=COLLECTION_TWO,
    )

    assert (
        first["fingerprint"] == second["fingerprint"] == direct_first == direct_second
    )


def test_corroboration_redacts_all_of_its_inputs() -> None:
    comment = sf.corroboration(
        OPENAI_TOKEN,
        f"same crash under {HOME_PATH}; {GITHUB_TOKEN}",
        f"contact {EMAIL}; key {AWS_KEY}",
    )

    _assert_synthetic_values_absent(comment)


def test_scientific_notation_that_resembles_an_email_survives() -> None:
    text = "The spectrum encodes a fragment as peak@xxx.xx in the exported vector."

    clean, removed = sf.redact(text)

    assert clean == text
    assert "email" not in removed


def test_main_prints_the_exact_redacted_payload(capsys) -> None:
    result = sf.main(
        [
            "--kind",
            "defect",
            "--target",
            OUTSIDE_TARGET,
            "--symptom",
            f"failed at {HOME_PATH} with {OPENAI_TOKEN}",
            "--expected",
            f"no use of {GITHUB_TOKEN}",
            "--context",
            f"{AWS_KEY} {EMAIL}",
            "--collection",
            COLLECTION_ONE,
        ]
    )

    assert result == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["preview"] == printed["payload"]
    _assert_synthetic_values_absent(_payload_text(printed))
