"""Released indicium records must name real SEPIO/RO/ECO terms.

ASB validation bridges before 0.2.0 wrote `sepio:credibility_status` with
SEPIO_0000338-0000341 / 0000301-0000303 and `eco:evidence_type`. In the SEPIO
release of 2023-06-13 none of those codes is a status (0000340 is an annotation
property, the others do not exist). The v1 records were migrated to
`sepio:0000183` (evidence direction) with 0000403 / 0000404 / 0000405 and
`ro:0002558` (has evidence) with ECO_0000501. This guard keeps every shipped
`indicium/*.jsonld` on those terms and checks each direction against the ASB
verdict the record still carries.
"""

import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).parent.parent
OBO = "http://purl.obolibrary.org/obo/"
FILES = sorted(ROOT.glob("collections/*/v*/indicium/*.jsonld"))
DIRECTION = {"yes": "0000403", "no": "0000404", "partial": "0000405", "null": "0000405"}
TRIAGE = {"promoted": "0000403", "critique": "0000404", "thin": "0000405", "degraded": "0000405"}


def _verdict(raw):
    if raw is True or raw == "yes":
        return "yes"
    if raw is False or raw == "no":
        return "no"
    return "partial" if raw == "partial" else "null"


def test_records_exist():
    assert FILES, "no indicium records found; the guard would pass over nothing"


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_validation_assertions_use_real_terms(path):
    text = path.read_text(encoding="utf-8")
    assert "credibility_status" not in text
    assert "eco:evidence_type" not in text
    doc = json.loads(text)
    nodes = [n for n in doc.get("@graph", []) if str(n.get("@type", "")).startswith("asbval:")]
    if not any("sepio:0000183" in n for n in nodes):
        return
    assert doc["@context"].get("ro") == {"@id": OBO + "RO_", "@prefix": True}
    bad = []
    for n in nodes:
        t = n["@type"]
        got = (n.get("sepio:0000183") or {}).get("@id", "")
        if t == "asbval:ClaimAssessment":
            want = DIRECTION[_verdict(n.get("asbval:supported_raw"))]
            if n.get("ro:0002558") != {"@id": OBO + "ECO_0000501"}:
                bad.append(f"{n['@id']}: evidence {n.get('ro:0002558')}")
        elif t == "asbval:SkillTriageAssertion":
            want = TRIAGE[n["asbval:triage_status"]]
        elif t == "asbval:ScopeDriftAssertion":
            want = "0000405"
        else:
            continue
        if got != f"{OBO}SEPIO_{want}":
            bad.append(f"{n['@id']}: direction {got}, expected SEPIO_{want}")
    assert not bad, "\n".join(bad[:20])
