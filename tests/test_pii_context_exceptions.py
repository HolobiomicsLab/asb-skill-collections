"""Two-sided tests for context-sensitive email false-positive classes."""

import re

import pytest

from scripts.pii_config import PII_CONFIG, _is_notation_not_email


EMAIL_RE = re.compile(PII_CONFIG["email_regex"])
REQUIRED_PUBLIC_SUFFIX_LAST_LABELS = {
    "com",
    "org",
    "net",
    "edu",
    "gov",
    "io",
    "fr",
    "de",
    "uk",
    "ch",
    "ca",
    "cn",
    "jp",
    "au",
    "nl",
    "se",
    "es",
    "it",
    "eu",
    "info",
    "dev",
    "ai",
}


def _is_context_exception(source_text: str) -> bool:
    """Classify the first email-shaped token with its source match context."""
    match = EMAIL_RE.search(source_text)
    assert match is not None, f"expected an email-shaped token in {source_text!r}"
    return _is_notation_not_email(match.group(0), match=match)


def test_public_suffix_last_label_config_has_required_bounded_coverage():
    configured = set(PII_CONFIG["email_public_suffix_last_labels"])
    assert REQUIRED_PUBLIC_SUFFIX_LAST_LABELS <= configured


def test_git_ssh_clone_syntax_is_a_context_exception():
    assert _is_context_exception(
        "git clone git@github.com:aitgon/vtam_benchmark.git"
    )


@pytest.mark.parametrize(
    "source_text",
    [
        "maintainer git@github.com answers questions",
        "clone git@github.com :group/project.git",
        "clone Git@github.com:group/project.git",
    ],
)
def test_git_address_without_exact_clone_context_remains_an_email(source_text):
    assert not _is_context_exception(source_text)


def test_r_slot_access_with_nonpublic_last_label_is_a_context_exception():
    assert _is_context_exception("metadata <- seurat_obj@meta.data")


@pytest.mark.parametrize(
    "source_text",
    [
        "owner <- name@lab.example.org",
        "owner <- name@institute.ac.uk",
        "owner <- name@university.edu.au",
        "owner <- name@example.invalid",
        "owner <- name@example.test",
        "value <- name-@meta.data",
    ],
)
def test_r_slot_class_does_not_mask_real_or_nonidentifier_emails(source_text):
    assert not _is_context_exception(source_text)


@pytest.mark.parametrize(
    "source_text",
    [
        "owner <- name@ulb.ac.be",
        "owner <- name@inserm.fr",
        "owner <- name@lab.bio",
        "owner <- name@group.science",
    ],
)
def test_country_code_and_listed_generic_last_labels_stay_emails(source_text):
    """Every country-code top-level domain is two letters; the list covers generic ones."""
    assert not _is_context_exception(source_text)


def test_non_email_r_slot_shape_stays_outside_the_email_recognizer():
    assert EMAIL_RE.search("value <- sce@int_colData$x") is None


def test_legacy_one_argument_notation_calls_remain_supported():
    assert _is_notation_not_email("peak@xxx.xx")
    assert _is_notation_not_email("loss@184.07")
    assert not _is_notation_not_email("researcher@example.org")
    assert not _is_notation_not_email("git@github.com")
    assert not _is_notation_not_email("researcher")
