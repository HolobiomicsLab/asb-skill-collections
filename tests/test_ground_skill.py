import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from scripts import ground_skill as gs


# --- a mock http(method, path, body=None, timeout=...) matching kb._http ------


class MockHttp:
    """Records calls; returns canned bodies keyed by (method, path-substring)."""

    def __init__(self, chat_reply=None, raises=False):
        self.chat_reply = chat_reply
        self.raises = raises
        self.calls = []

    def __call__(self, method, path, body=None, timeout=1200):
        self.calls.append((method, path, body))
        if self.raises:
            raise OSError("Connection refused")
        if path.endswith("/stats"):
            # KB exists with chunks so prepare_kb short-circuits to "already present".
            return {"chunk_count": 7}
        if path == "/api/chat":
            return self.chat_reply
        # KB create / ingest endpoints
        return {}


SUPPORTIVE = (
    'VERDICT: SUPPORTED\n'
    'CONFIDENCE: high\n'
    'EVIDENCE: "The authors normalize features by median fold-change before '
    'differential testing." (Methods, p.4)'
)

NON_SUPPORTIVE = (
    "VERDICT: NOT_SUPPORTED\n"
    "CONFIDENCE: low\n"
    "EVIDENCE: The paper never discusses the claimed normalization step."
)


def test_supportive_reply_yields_supported_with_evidence():
    http = MockHttp(chat_reply={"answer": SUPPORTIVE})
    out = gs.verify_doi_support("skill claims median fold-change normalization",
                                "10.1/xyz", http=http)
    assert out["supported"] is True
    assert out["confidence"] == "high"
    assert out["doi"] == "10.1/xyz"
    assert "median fold-change" in out["evidence"]
    # it actually queried /api/chat scoped to the per-DOI KB slug
    chat = [c for c in http.calls if c[1] == "/api/chat"]
    assert chat, "expected a POST /api/chat"
    assert chat[0][2]["kb_names"] == ["asb-paper-10-1-xyz"]


def test_non_supportive_reply_yields_false():
    http = MockHttp(chat_reply={"answer": NON_SUPPORTIVE})
    out = gs.verify_doi_support("skill claims something unrelated",
                                "10.1/xyz", http=http)
    assert out["supported"] is False
    assert out["confidence"] == "low"
    assert out["doi"] == "10.1/xyz"


def test_http_that_raises_degrades_to_low_conf_false():
    http = MockHttp(raises=True)
    out = gs.verify_doi_support("anything", "10.1/down", http=http)
    assert out == {
        "supported": False,
        "confidence": "low",
        "evidence": "",
        "doi": "10.1/down",
    }


def test_malformed_chat_reply_never_raises():
    # chat returns something with no parseable verdict -> graceful False/low.
    http = MockHttp(chat_reply={"unexpected": "shape"})
    out = gs.verify_doi_support("x", "10.1/weird", http=http)
    assert out["supported"] is False
    assert out["confidence"] == "low"
    assert out["doi"] == "10.1/weird"


def test_prepare_false_skips_kb_creation():
    http = MockHttp(chat_reply={"answer": SUPPORTIVE})
    out = gs.verify_doi_support("x", "10.1/abc", http=http, prepare=False)
    assert out["supported"] is True
    # no KB create/ingest/stats calls when prepare=False — only the chat call.
    assert all(c[1] == "/api/chat" for c in http.calls)


def test_medium_confidence_supported():
    reply = {"answer": "VERDICT: SUPPORTED\nCONFIDENCE: medium\nEVIDENCE: see Fig 2."}
    http = MockHttp(chat_reply=reply)
    out = gs.verify_doi_support("x", "10.1/m", http=http)
    assert out["supported"] is True
    assert out["confidence"] == "medium"


def test_answer_under_response_or_content_key():
    for key in ("response", "content"):
        http = MockHttp(chat_reply={key: SUPPORTIVE})
        out = gs.verify_doi_support("x", "10.1/k", http=http)
        assert out["supported"] is True, key


def test_main_writes_json_for_skill_md(tmp_path, capsys):
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        "---\nname: My Skill\ndescription: Use when normalizing features.\n---\n"
        "Body: median fold-change normalization.\n",
        encoding="utf-8",
    )
    http = MockHttp(chat_reply={"answer": SUPPORTIVE})
    rc = gs.main(["--doi", "10.1/cli", "--skill-md", str(skill)], http=http)
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["supported"] is True
    assert out["doi"] == "10.1/cli"


def test_main_graceful_when_http_down(tmp_path, capsys):
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: S\ndescription: Use when x.\n---\nbody\n",
                     encoding="utf-8")
    http = MockHttp(raises=True)
    rc = gs.main(["--doi", "10.1/down", "--skill-md", str(skill)], http=http)
    # never raises; reports unsupported but exits cleanly (0) — grounding is best-effort.
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["supported"] is False
    assert out["confidence"] == "low"
