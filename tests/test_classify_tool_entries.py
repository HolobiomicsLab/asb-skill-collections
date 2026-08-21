"""Not every catalogue entry is software. These tests hold the classification.

The over-firing direction is the dangerous one: a wrongly-classified vendor product
takes the `restricted` tier, which is a claim about an open-source tool. So the
calibrated negative corpus below is the real test, not the positive cases.
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import classify_tool_entries as c

ROOT = pathlib.Path(__file__).parent.parent
VOCAB = c.load_vocabulary()


def kind_of(name):
    return c.classify({"slug": "s", "name": name}, VOCAB)[0]


# --------------------------------------------------------------------------- #
# Fires -- across vendors, not one                                            #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", [
    "Agilent 6550 iFunnel Q-TOF mass spectrometer",
    "Bruker Solarix",
    "SCIEX Q-TOF UHPLC-HRMS/MS",
    "Thermo Xcalibur",
    "Waters Synapt G2-Si",
    "Shimadzu LCMS-8060",
])
def test_a_vendor_instrument_is_a_vendor_product(name):
    assert kind_of(name) == c.KIND_VENDOR


@pytest.mark.parametrize("name", [
    "Agilent MassHunter", "Compound Discoverer", "LipidSearch", "Sciex Multiquant",
    "MATLAB R2024a", "Q-Exactive orbitrap",
])
def test_a_proprietary_application_is_a_vendor_product(name):
    assert kind_of(name) == c.KIND_VENDOR


@pytest.mark.parametrize("name,shape", [
    ("massdash.peakPickers.MRMTransitionGroupPicker", "module_path"),
    ("scipy.signal.find_peaks", "module_path"),
    ("mzExacto()", "function_call"),
    ("github.com/HassounLab/ESP", "repository_path"),
    ("https://github.com/sdrogers/nplinker", "repository_path"),
    ("ipbhalle/metfragweb", "repository_path"),
    ("Pandas for tabular data manipulation and aggregation", "descriptive_phrase"),
])
def test_an_extraction_defect_is_an_artefact(name, shape):
    kind, reason = c.classify({"slug": "s", "name": name}, VOCAB)
    assert (kind, reason) == (c.KIND_ARTEFACT, shape)


# --------------------------------------------------------------------------- #
# Stays clean -- the side that matters                                        #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", [
    # A vendor name inside one token is not a vendor word. ThermoRawFileParser is
    # Apache-2.0; classifying it `restricted` would be a false claim about OSS.
    "ThermoRawFileParser",
    "ThermoFisherReader",
    # Open-source tools that live next to vendor formats.
    "ProteoWizard", "msconvert", "Skyline", "OpenMS", "MZmine",
    # Ordinary packages.
    "xcms", "matchms", "seaborn", "scikit-learn",
])
def test_open_source_is_never_a_vendor_product(name):
    assert kind_of(name) != c.KIND_VENDOR


@pytest.mark.parametrize("name", [
    # A name plus its expansion is a name, not prose.
    "PALS (Pathway Activity Level Scoring)",
    "COBRApy (for optGpSampler uniform sampling)",
    "MelonnPan (Elastic Net linear regression)",
    "t-SNE (t-distributed Stochastic Neighbor Embedding)",
    # Short real names.
    "xcms", "CAMERA", "MS-DIAL", "matchms",
])
def test_a_real_name_is_not_an_artefact(name):
    assert kind_of(name) != c.KIND_ARTEFACT


def test_the_gloss_strip_leaves_an_empty_call_alone():
    """`mzExacto()` must stay a function_call; only a gloss with content is removed."""
    assert c.without_gloss("mzExacto()") == "mzExacto()"
    assert c.without_gloss("PALS (Pathway Activity Level Scoring)") == "PALS"


def test_an_instrument_name_beats_the_phrase_shape():
    """Five words and a real machine: vendor_product, not a descriptive phrase."""
    assert kind_of("Agilent 1290 Infinity UHPLC system") == c.KIND_VENDOR


# --------------------------------------------------------------------------- #
# Calibrated negative corpus: the shipped catalogue                           #
# --------------------------------------------------------------------------- #

def _catalogue():
    path = ROOT / "collections" / "metabolomics" / "v2" / "tools_index.json"
    if not path.is_file():
        pytest.skip("collection not present in this checkout")
    return json.loads(path.read_text(encoding="utf-8"))


def test_no_tool_with_a_resolved_licence_is_called_a_vendor_product():
    """196 tools whose licence was resolved from their own repository or registry.

    Every one is real software with a real licence, so the classifier must leave
    all of them alone. This is the measurement that justifies the vocabulary; a
    term added carelessly to governance/tool_entry_kinds.yaml turns it red.
    """
    tools = _catalogue()
    kinds = c.classify_all(tools)
    resolved = [t for t in tools if t.get("license_subject") == "tool"
                and t.get("license")]
    assert len(resolved) > 100, "negative corpus vanished; the guard would pass vacuously"
    misfired = [t["name"] for t in resolved if kinds[t["slug"]]["kind"] != c.KIND_SOFTWARE]
    assert misfired == []


def test_every_classified_kind_is_in_the_declared_vocabulary():
    declared = set(VOCAB["kinds"])
    assert {r["kind"] for r in c.classify_all(_catalogue()).values()} <= declared


def test_the_catalogue_records_the_kind_it_classifies_to():
    """tools_index must carry the classification it was derived with."""
    tools = _catalogue()
    kinds = c.classify_all(tools)
    drifted = [t["slug"] for t in tools if t.get("entry_kind") != kinds[t["slug"]]["kind"]]
    assert drifted == [], "re-run enrich_tools_index"


def test_a_vendor_product_is_restricted_rather_than_unknown():
    """The tier says "use per your agreement", not "we failed to look it up"."""
    vendor = [t for t in _catalogue() if t.get("entry_kind") == c.KIND_VENDOR]
    assert vendor, "no vendor products in the catalogue"
    assert all(t["license_tier"] == "restricted" for t in vendor)
    assert all(t["license_subject"] == "tool" for t in vendor)
