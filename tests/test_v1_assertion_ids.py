"""Released v1 assertion IDs must identify their source paper without collisions.

The migration uses ASB's production DOI validator and scoping helper. This
standalone guard independently joins the shipped provenance, whose DOI fields
are already bare DOI labels (some contain uppercase letters). It deliberately
does not implement a general DOI normalizer or require ASB in collections CI.
"""

from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "asbval:assertion/paper/"
COLLECTIONS = ("epigenomics", "metabolomics", "transcriptomics")
# No workflow/build join exists for these four records. The caller confirmed
# their source papers against Crossref by title, journal and year, 2026-09-14.
CONFIRMED = {
    ("metabolomics", "featurefindermetab"): "10.1074/mcp.m113.031278",
    ("metabolomics", "mzmine2"): "10.1186/1471-2105-11-395",
    ("metabolomics", "np_analyst"): "10.1021/acscentsci.1c01108",
    ("metabolomics", "sirius"): "10.1038/s41592-019-0344-8",
}


def test_v1_assertions_have_unique_source_paper_ids():
    seen = {}
    counts = Counter()
    paper_records = {}
    for collection in COLLECTIONS:
        unit = ROOT / "collections" / collection / "v1"
        build_dois = defaultdict(set)
        for skill in sorted(unit.glob("skills/*/SKILL.md")):
            match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", skill.read_text(encoding="utf-8"), re.S)
            assert match, f"Missing frontmatter: {skill}"
            frontmatter = yaml.safe_load(match.group(1))
            for source in (frontmatter.get("provenance") or {}).get("sources") or []:
                if not isinstance(source, dict) or not source.get("build") or not source.get("doi"):
                    continue
                doi = source["doi"]
                assert isinstance(doi, str) and doi.startswith("10.") and doi == doi.strip(), skill
                build_dois[source["build"]].add(doi.lower())
        for path in sorted(unit.glob("indicium/*.jsonld")):
            counts["records"] += 1
            document = json.loads(path.read_bytes())
            graph = document.get("@graph", [])
            assertions = [node for node in graph
                          if str(node.get("@type", "")).startswith("asbval:")
                          or str(node.get("@id", "")).startswith("asbval:assertion/")]
            if not assertions:
                counts["records_without_assertions"] += 1
                continue
            counts["assertion_records"] += 1
            counts[collection] += len(assertions)
            candidates = set()
            for node in graph:
                if node.get("@type") == "asbext:WorkflowCharacterisation":
                    workflow_id = node["@id"]
                    assert workflow_id.endswith("#workflow-characterisation"), path
                    build = workflow_id.removesuffix("#workflow-characterisation")
                    candidates.update(build_dois[build])
            if (collection, path.stem) in CONFIRMED:
                confirmed = CONFIRMED[(collection, path.stem)]
                assert not candidates or candidates == {confirmed}, path
                candidates.add(confirmed)
                counts["confirmed_records"] += 1
            else:
                counts["joined_records"] += 1
            assert len(candidates) == 1, f"{path}: source DOI missing or ambiguous: {candidates}"
            doi = next(iter(candidates))
            assert doi not in paper_records, f"Repeated paper DOI: {path} and {paper_records.get(doi)}"
            paper_records[doi] = path
            expected_prefix = f"{PREFIX}{quote(doi, safe='')}/"
            for node in assertions:
                assertion_id = node.get("@id", "")
                assert assertion_id.startswith(expected_prefix), f"{path}: wrong paper scope: {assertion_id}"
                suffix = assertion_id[len(expected_prefix):]
                assert suffix.startswith(("card/", "skill/", "claim/")), f"{path}: wrong local suffix: {suffix}"
                assert assertion_id not in seen, f"Shared ID: {path} and {seen.get(assertion_id)}: {assertion_id}"
                seen[assertion_id] = path
    assert counts == {
        "records": 106, "assertion_records": 82, "records_without_assertions": 24,
        "joined_records": 78, "confirmed_records": 4,
        "epigenomics": 2614, "metabolomics": 11839, "transcriptomics": 2130,
    }
    assert len(seen) == 16583
