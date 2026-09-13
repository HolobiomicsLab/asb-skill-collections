"""The credential itself must be absent, not merely the whole matched string.

`tests/test_skill_feedback.py` asserts that the *entire* secret string it fed in
is missing from the redacted output. For an HTTP auth header that assertion is
satisfied by redacting the scheme alone: "Authorization: Bearer <tok>" became
"<redacted:authorization_header> <tok>", which published the credential under a
label claiming it had been removed. These cases assert the credential token.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import skill_feedback as sf  # noqa: E402


@pytest.mark.parametrize(
    "header,credential",
    [
        ("Authorization: Bearer aBcDeF0123456789", "aBcDeF0123456789"),
        ("Authorization: Basic dXNlcjpodW50ZXIy", "dXNlcjpodW50ZXIy"),
        ("authorization: bearer eyJhbGciOi.J9.sig", "eyJhbGciOi.J9.sig"),
        ("Authorization: Token 0123456789abcdef", "0123456789abcdef"),
        ("Authorization: abc123nocheme", "abc123nocheme"),
    ],
)
def test_the_credential_and_not_only_the_scheme_is_removed(header, credential):
    out, removed = sf.redact(f"the request failed on {header} during the run")
    assert credential not in out
    assert "authorization_header" in removed


@pytest.mark.parametrize(
    "text,secret,survivor",
    [
        ("token: s3cret and then it continued", "s3cret", "continued"),
        ("password: hunter2 was rejected", "hunter2", "rejected"),
        ("api_key: AKIAEXAMPLEKEY0 in the config", "AKIAEXAMPLEKEY0", "config"),
    ],
)
def test_an_assignment_still_consumes_one_token_only(text, secret, survivor):
    """Widening the header branch must not swallow the prose after a key=value."""
    out, _ = sf.redact(f"it failed on {text}")
    assert secret not in out
    assert survivor in out
