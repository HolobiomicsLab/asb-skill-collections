"""Tests for scripts/readme_license_precheck.py — written RED-first (TDD).

All side-effecting collaborators (network + LLM) are injected so these tests run
fully offline.
"""
from __future__ import annotations

import json
import pathlib

import pytest
import yaml


# ---------------------------------------------------------------------------
# Helpers / mini-corpus builders
# ---------------------------------------------------------------------------

def _corpus_with_candidate(tmp_path, **overrides) -> pathlib.Path:
    """Write a corpus with ONE entry that should be selected by candidates()."""
    paper = {
        "name": "ToolA",
        "doi": "10.1000/aaa",
        "repo_url": "https://github.com/owner1/repoA",
        "license_tier": "restricted",
        "license_detection": "none",
        "access": {"license": None},
        "status": "included",
    }
    paper.update(overrides)
    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [paper],
    }
    p = tmp_path / "corpus.yaml"
    p.write_text(yaml.safe_dump(corpus, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Test 1 — extract_license: JSON parsing robustness
# ---------------------------------------------------------------------------

class TestExtractLicense:
    def _make_chat(self, response_text: str):
        """Return a fake _chat callable that returns response_text."""
        return lambda prompt: response_text

    def test_parses_fenced_json(self):
        from scripts.readme_license_precheck import extract_license

        fenced = '```json\n{"license": "MIT", "confidence": "high", "evidence": "Licensed under the MIT License."}\n```'
        chat = self._make_chat(fenced)
        result = extract_license("some readme text", _chat=chat)

        assert result["license"] == "MIT"
        assert result["confidence"] == "high"
        assert result["evidence"] == "Licensed under the MIT License."

    def test_parses_bare_json(self):
        from scripts.readme_license_precheck import extract_license

        bare = '{"license": "Apache-2.0", "confidence": "medium", "evidence": "Apache 2.0 License"}'
        chat = self._make_chat(bare)
        result = extract_license("readme", _chat=chat)

        assert result["license"] == "Apache-2.0"
        assert result["confidence"] == "medium"

    def test_returns_null_dict_on_garbage(self):
        from scripts.readme_license_precheck import extract_license

        chat = self._make_chat("I cannot determine the license from this text.")
        result = extract_license("readme", _chat=chat)

        assert result == {"license": None, "confidence": "low", "evidence": None}

    def test_parses_json_with_surrounding_text(self):
        from scripts.readme_license_precheck import extract_license

        response = 'Based on my analysis: {"license": "GPL-3.0", "confidence": "high", "evidence": "GNU GPL v3"} That is all.'
        chat = self._make_chat(response)
        result = extract_license("readme", _chat=chat)

        assert result["license"] == "GPL-3.0"

    def test_null_license_in_json(self):
        from scripts.readme_license_precheck import extract_license

        bare = '{"license": null, "confidence": "low", "evidence": null}'
        chat = self._make_chat(bare)
        result = extract_license("readme", _chat=chat)

        assert result["license"] is None
        assert result["confidence"] == "low"
        assert result["evidence"] is None


# ---------------------------------------------------------------------------
# Test 2 — detected_tier: license string → tier mapping
# ---------------------------------------------------------------------------

class TestDetectedTier:
    def test_mit_is_open(self):
        from scripts.readme_license_precheck import detected_tier
        assert detected_tier("MIT") == "open"

    def test_noncommercial_cc(self):
        from scripts.readme_license_precheck import detected_tier
        # CC-BY-NC-4.0 SPDX id
        result = detected_tier("CC-BY-NC-4.0")
        assert result == "noncommercial"

    def test_noncommercial_long_name(self):
        from scripts.readme_license_precheck import detected_tier
        # This passes through classify_license_text (matches "cc by-nc" keyword)
        result = detected_tier("Creative Commons Attribution-NonCommercial 4.0")
        assert result == "noncommercial"

    def test_none_returns_none(self):
        from scripts.readme_license_precheck import detected_tier
        assert detected_tier(None) is None

    def test_empty_string_returns_none(self):
        from scripts.readme_license_precheck import detected_tier
        assert detected_tier("") is None

    def test_apache_is_open(self):
        from scripts.readme_license_precheck import detected_tier
        assert detected_tier("Apache-2.0") == "open"


# ---------------------------------------------------------------------------
# Test 3 — precheck_entry: action routing
# ---------------------------------------------------------------------------

class TestPrecheckEntry:
    def _entry(self, **overrides) -> dict:
        base = {
            "name": "ToolA",
            "doi": "10.1000/aaa",
            "repo_url": "https://github.com/owner1/repoA",
            "license_tier": "restricted",
            "license_detection": "none",
            "access": {"license": None},
            "status": "included",
        }
        base.update(overrides)
        return base

    def _readme_returning(self, text: str | None):
        return lambda owner, repo, token, _open=None: text

    def _chat_returning(self, payload: dict):
        return lambda prompt: json.dumps(payload)

    def test_high_confidence_mit_gives_retier(self):
        from scripts.readme_license_precheck import precheck_entry

        entry = self._entry()
        readme_fn = self._readme_returning("Licensed under the MIT License.")
        chat_fn = self._chat_returning(
            {"license": "MIT", "confidence": "high", "evidence": "Licensed under the MIT License."}
        )

        result = precheck_entry(
            entry, token="tok",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        assert result["action"] == "retier"
        assert result["tier"] == "open"
        assert result["detected_license"] == "MIT"
        assert result["repo"] == "owner1/repoA"
        assert result["evidence"] == "Licensed under the MIT License."

    def test_null_confidence_gives_file_issue(self):
        from scripts.readme_license_precheck import precheck_entry

        entry = self._entry()
        readme_fn = self._readme_returning("No license mentioned here.")
        chat_fn = self._chat_returning(
            {"license": None, "confidence": "low", "evidence": None}
        )

        result = precheck_entry(
            entry, token="tok",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        assert result["action"] == "file-issue"

    def test_low_confidence_with_license_gives_file_issue(self):
        from scripts.readme_license_precheck import precheck_entry

        entry = self._entry()
        readme_fn = self._readme_returning("Might be MIT-ish.")
        chat_fn = self._chat_returning(
            {"license": "MIT", "confidence": "low", "evidence": "Might be MIT-ish."}
        )

        result = precheck_entry(
            entry, token="tok",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        # low confidence → still file-issue
        assert result["action"] == "file-issue"

    def test_no_readme_gives_file_issue(self):
        from scripts.readme_license_precheck import precheck_entry

        entry = self._entry()
        readme_fn = self._readme_returning(None)  # 404 / empty
        chat_fn = self._chat_returning(
            {"license": "MIT", "confidence": "high", "evidence": "MIT"}
        )

        result = precheck_entry(
            entry, token="tok",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        # no README → no detection possible → file-issue
        assert result["action"] == "file-issue"

    def test_extract_injection(self):
        """_extract parameter replaces the entire extract_license function."""
        from scripts.readme_license_precheck import precheck_entry

        entry = self._entry()
        readme_fn = self._readme_returning("some text")

        # Inject an _extract that always returns high-confidence CC-BY-NC-4.0
        def fake_extract(readme_text, _chat):
            return {"license": "CC-BY-NC-4.0", "confidence": "high", "evidence": "CC-BY-NC-4.0"}

        result = precheck_entry(
            entry, token="tok",
            _readme=readme_fn,
            _extract=fake_extract,
            _chat=None,  # not used when _extract is injected
        )

        assert result["action"] == "retier"
        assert result["tier"] == "noncommercial"


# ---------------------------------------------------------------------------
# Test 4 — run_precheck: corpus mutation and summary
# ---------------------------------------------------------------------------

class TestRunPrecheck:
    def _make_corpus(self, tmp_path: pathlib.Path, **paper_overrides) -> pathlib.Path:
        """Build a corpus with one candidate paper."""
        return _corpus_with_candidate(tmp_path, **paper_overrides)

    def _readme_fn(self, text: str | None):
        return lambda owner, repo, token, _open=None: text

    def _chat_fn(self, payload: dict):
        return lambda prompt: json.dumps(payload)

    def test_high_confidence_mit_retieres_corpus(self, tmp_path):
        from scripts.readme_license_precheck import run_precheck

        corpus_path = self._make_corpus(tmp_path)
        chat_fn = self._chat_fn(
            {"license": "MIT", "confidence": "high", "evidence": "MIT License here."}
        )
        readme_fn = self._readme_fn("MIT License here.")

        summary = run_precheck(
            str(corpus_path),
            api_key="fake-key",
            token="fake-token",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        # Check summary counts
        assert summary["checked"] == 1
        assert summary["retiered"] == 1
        assert summary["still_file_issue"] == 0
        assert summary["by_tier"].get("open", 0) >= 1

        # Check the corpus was mutated
        doc = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))
        paper = doc["papers"][0]
        assert paper["license_tier"] == "open"
        assert paper["access"]["license"] == "MIT"
        assert paper["license_detection"] == "readme-llm"
        assert paper["license_evidence"] == "MIT License here."

    def test_null_detection_leaves_corpus_unchanged(self, tmp_path):
        from scripts.readme_license_precheck import run_precheck

        corpus_path = self._make_corpus(tmp_path)
        # Read original corpus to compare later
        original = corpus_path.read_text(encoding="utf-8")

        chat_fn = self._chat_fn(
            {"license": None, "confidence": "low", "evidence": None}
        )
        readme_fn = self._readme_fn("No license info.")

        summary = run_precheck(
            str(corpus_path),
            api_key="fake-key",
            token="fake-token",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        assert summary["checked"] == 1
        assert summary["retiered"] == 0
        assert summary["still_file_issue"] == 1

        # Corpus should be unchanged (license_tier still restricted, no license_evidence)
        doc = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))
        paper = doc["papers"][0]
        assert paper["license_tier"] == "restricted"
        assert not paper.get("license_evidence")
        assert paper.get("license_detection") != "readme-llm"

    def test_limit_caps_processing(self, tmp_path):
        """With limit=0, nothing is processed."""
        from scripts.readme_license_precheck import run_precheck

        corpus_path = self._make_corpus(tmp_path)
        chat_fn = self._chat_fn(
            {"license": "MIT", "confidence": "high", "evidence": "MIT"}
        )
        readme_fn = self._readme_fn("MIT License here.")

        summary = run_precheck(
            str(corpus_path),
            api_key="fake-key",
            token="fake-token",
            limit=0,
            _readme=readme_fn,
            _chat=chat_fn,
        )

        assert summary["checked"] == 0
        assert summary["retiered"] == 0

    def test_by_tier_counts_retiered(self, tmp_path):
        """by_tier in summary reflects actual tier assigned."""
        from scripts.readme_license_precheck import run_precheck

        corpus_path = self._make_corpus(tmp_path)
        chat_fn = self._chat_fn(
            {"license": "MIT", "confidence": "high", "evidence": "MIT License."}
        )
        readme_fn = self._readme_fn("MIT License.")

        summary = run_precheck(
            str(corpus_path),
            api_key="fake-key",
            token="fake-token",
            _readme=readme_fn,
            _chat=chat_fn,
        )

        assert "open" in summary["by_tier"]
        assert summary["by_tier"]["open"] == 1
