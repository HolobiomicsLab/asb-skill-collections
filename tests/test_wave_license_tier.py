import pathlib, yaml

WAVE = pathlib.Path(__file__).parent.parent / "collections/metabolomics/proposals/wave-2026-06-community.yaml"

def _entries():
    return {p["name"]: p for p in yaml.safe_load(WAVE.read_text())["papers"]}

def test_every_entry_has_a_tier():
    for name, p in _entries().items():
        assert p.get("license_tier") in {"open", "noncommercial", "restricted"}, name

def test_tiers_are_correct():
    e = _entries()
    assert e["RforMassSpectrometry"]["license_tier"] == "open"
    assert e["Metabonaut"]["license_tier"] == "open"
    assert e["MetabolomicsHub"]["license_tier"] == "open"   # Apache-2.0 code
    assert e["Masster"]["license_tier"] == "noncommercial"

def test_masster_unblocked():
    assert _entries()["Masster"]["triage"]["decision"] == "accept"
