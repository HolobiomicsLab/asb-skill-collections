import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import license_tier as lt


def test_spdx_exact_open():
    assert lt.tier_for_license("Apache-2.0") == "open"
    assert lt.tier_for_license("apache-2.0") == "open"          # case-insensitive

def test_copyleft_is_open():
    assert lt.tier_for_license("GPL-3.0-only") == "open"
    assert lt.tier_for_license("AGPL-3.0-or-later") == "open"

def test_noncommercial_spdx_and_keyword():
    assert lt.tier_for_license("CC-BY-NC-4.0") == "noncommercial"
    assert lt.tier_for_license(
        "Masster Noncommercial and Commercial Services License 1.0.0"
    ) == "noncommercial"

def test_restricted_fallback():
    assert lt.tier_for_license("") == "restricted"
    assert lt.tier_for_license("NOASSERTION") == "restricted"
    assert lt.tier_for_license("All Rights Reserved") == "restricted"

def test_ack_required():
    assert lt.ack_required("open") is False
    assert lt.ack_required("noncommercial") is True
    assert lt.ack_required("restricted") is True
