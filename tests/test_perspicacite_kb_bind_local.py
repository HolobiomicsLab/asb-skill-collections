import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import perspicacite_kb_bind as kb


def test_unpaywall_oa_url_picks_best_oa(monkeypatch):
    class R:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"best_oa_location": {"url_for_pdf": "http://x/oa.pdf"}}).encode()
    assert kb.unpaywall_oa_url("10.1/x", "e@e.com", _http=lambda req, timeout=0: R()) == "http://x/oa.pdf"

def test_unpaywall_oa_url_none_when_closed(monkeypatch):
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
