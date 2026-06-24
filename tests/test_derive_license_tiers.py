import pathlib, sys, textwrap, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import derive_license_tiers as d


def test_parse_repo_variants():
    assert d.parse_repo("https://github.com/iomega/spec2vec") == ("iomega", "spec2vec")
    assert d.parse_repo("https://github.com/a/b.git") == ("a", "b")
    assert d.parse_repo("owner/repo") == ("owner", "repo")
    assert d.parse_repo("") is None
    assert d.parse_repo("https://example.org/x") is None

def test_parse_repo_tolerates_punctuation_and_paths():
    assert d.parse_repo("idrblab/NOREVA;") == ("idrblab", "NOREVA")
    assert d.parse_repo("https://github.com/a/b/tree/main") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b?tab=readme") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b#readme") == ("a", "b")
    assert d.parse_repo("https://github.com/a/b.git") == ("a", "b")   # still works

def test_tier_for_repo_maps_spdx():
    fetch = lambda o, r, t: {"iomega/spec2vec": "Apache-2.0"}.get(f"{o}/{r}")
    assert d.tier_for_repo("https://github.com/iomega/spec2vec", _fetch=fetch) == ("open", "Apache-2.0")

def test_tier_for_repo_noncommercial():
    fetch = lambda o, r, t: "CC-BY-NC-4.0"
    assert d.tier_for_repo("https://github.com/x/y", _fetch=fetch) == ("noncommercial", "CC-BY-NC-4.0")

def test_tier_for_repo_no_license_is_restricted():
    assert d.tier_for_repo("https://github.com/x/y", _fetch=lambda o, r, t: None) == ("restricted", None)
    assert d.tier_for_repo("not-a-repo", _fetch=lambda o, r, t: "MIT") == ("restricted", None)

def test_tier_for_repo_uses_cache(tmp_path):
    calls = []
    def fetch(o, r, t): calls.append((o, r)); return "MIT"
    cache = {}
    d.tier_for_repo("https://github.com/a/b", cache=cache, _fetch=fetch)
    d.tier_for_repo("https://github.com/a/b", cache=cache, _fetch=fetch)
    assert calls == [("a", "b")]            # second call served from cache
    assert cache == {"a/b": "MIT"}

def test_apply_to_corpus_writes_tiers(tmp_path):
    corpus = tmp_path / "corpus.yaml"
    corpus.write_text(textwrap.dedent('''
        schema: asb-corpus/1.0
        papers:
        - name: A
          doi: 10.1/a
          repo_url: https://github.com/a/open
          status: included
          access: {type: repo-oa, is_oa: true}
        - name: B
          doi: 10.1/b
          repo_url: https://github.com/b/nc
          status: included
          access: {type: repo-oa, is_oa: true}
    '''))
    fetch = lambda o, r, t: {"a/open": "MIT", "b/nc": "CC-BY-NC-4.0"}.get(f"{o}/{r}")
    summary = d.apply_to_corpus(str(corpus), token=None, _fetch=fetch)
    out = yaml.safe_load(corpus.read_text())["papers"]
    assert out[0]["license_tier"] == "open" and out[0]["access"]["license"] == "MIT"
    assert out[1]["license_tier"] == "noncommercial" and out[1]["access"]["license"] == "CC-BY-NC-4.0"
    assert out[0]["access"]["type"] == "repo-oa"
    assert out[1]["access"]["type"] == "repo-oa"
    assert summary == {"open": 1, "noncommercial": 1}
