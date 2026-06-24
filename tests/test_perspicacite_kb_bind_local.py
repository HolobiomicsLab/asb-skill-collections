import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import perspicacite_kb_bind as kb


def test_unpaywall_oa_url_picks_best_oa():
    class R:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"best_oa_location": {"url_for_pdf": "http://x/oa.pdf"}}).encode()
    assert kb.unpaywall_oa_url("10.1/x", "e@e.com", _http=lambda req, timeout=0: R()) == "http://x/oa.pdf"

def test_unpaywall_oa_url_none_when_closed():
    class R:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"best_oa_location": None}).encode()
    assert kb.unpaywall_oa_url("10.1/x", "e@e.com", _http=lambda req, timeout=0: R()) is None

def test_clone_repo_invokes_git(tmp_path):
    calls = []
    def fake_run(cmd, **kw):
        calls.append(cmd)
        class P: returncode = 0
        return P()
    assert kb.clone_repo("https://github.com/a/b", tmp_path / "r", _run=fake_run) is True
    assert calls and calls[0][0] == "git" and "clone" in calls[0]
    assert "--" in calls[0]


def test_prepare_kb_graceful_when_server_unreachable(monkeypatch):
    import urllib.error
    def boom(*a, **k):
        raise urllib.error.URLError("Connection refused")
    monkeypatch.setattr(kb, "_http", boom)
    status = kb.prepare_kb("asb-paper-x", "10.x/y", "ASB grounding KB")
    assert isinstance(status, dict)
    assert status.get("created") is False
    assert "unreachable" in (status.get("error") or "")


def test_build_local_manifest_embeds_open(tmp_path):
    calls = []
    def fake_clone(url, dest, **kw):
        calls.append(url); return True
    rec = {"slug": "open-skill", "license_tier": "open",
           "repo_urls": ["https://github.com/a/b"], "dois": []}
    man = kb.build_local_manifest(rec, str(tmp_path), paper=False, email="e@e.com",
                                  _clone=fake_clone)
    assert man["mode"] == "embed"
    assert man["repos"][0]["cloned"] is True
    assert calls == ["https://github.com/a/b"]


def test_build_local_manifest_link_only_noncommercial(tmp_path):
    def fake_clone(url, dest, **kw):
        raise AssertionError("non-open tier must not clone/embed")
    rec = {"slug": "masster", "license_tier": "noncommercial",
           "repo_urls": ["https://github.com/zamboni-lab/masster-dist"], "dois": ["10.x/y"]}
    man = kb.build_local_manifest(rec, str(tmp_path), paper=True, email="e@e.com",
                                  _clone=fake_clone)
    assert man["mode"] == "link-only"
    assert man["repos"][0]["embedded"] is False
    assert man["paper"]["embedded"] is False


def test_link_only_predicate():
    assert kb.link_only({"license_tier": "restricted"}) is True
    assert kb.link_only({"license_tier": "open"}) is False
    assert kb.link_only({}) is False
