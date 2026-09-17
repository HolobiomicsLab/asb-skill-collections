---
name: candidate-formula-ranking
description: Use when you have an observed m/z value from mass spectrometry imaging
  and need to assign a chemical formula with high confidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SMART
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment
  in mass spectrometry imaging
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Candidate-formula ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank molecular formula candidates for a given m/z value using a multiple linear regression model that scores formulae based on network connectivity, chemical edge evidence, and mass accuracy. This skill is essential when assigning chemical identities to thousands of m/z features in spatially-resolved metabolomics, where accurate annotation lags behind LC-MS approaches.

## When to use

You have an observed m/z value from mass spectrometry imaging and need to assign a chemical formula with high confidence. Apply this skill when you have access to a pre-built formula network database (KnownSet) and a trained MLR model, and you want to rank multiple plausible formula candidates rather than returning a single unvalidated assignment.

## When NOT to use

- Your m/z value is already annotated with high confidence from orthogonal methods (e.g., comparison to known standards or MS/MS fragmentation); ranking adds no new information.
- The KnownSet database is not available or is outdated; the ranking will be unreliable without comprehensive chemical space coverage.
- You require real-time single-formula assignment for high-throughput screening; ranking multiple candidates per m/z is slower than threshold-based filtering.

## Inputs

- m/z value (single numeric or file of m/z values in table format)
- SMART-Database file (smart.db; contains KnownSet with 2.8M formulae and edge annotations)
- trained MLR model file (e.g. lr_4f.pkl)
- ion polarity (+ or - or 0)
- PPM threshold for mass accuracy window (default 5 ppm)

## Outputs

- ranked list of candidate formulae with composite scores
- confidence metrics for each candidate
- evidence breakdown (linked formulae count, edge types, PPM accuracy) per candidate
- formula network structure for the m/z of interest

## How to apply

Load the KnownSet database containing 2.8 million formulae interconnected by DBEdges (from HMDB, ChEMBL, PubChem) and BioEdges (from KEGG). For your input m/z value, apply the multiple linear regression model to extract the associated formula network within a specified PPM tolerance (default 5 ppm). Score each candidate formula using three criteria: (1) the number and strength of linked formulae connections in the network, (2) the presence and type of chemical relationship edges (DBEdges/BioEdges), and (3) the observed mass accuracy (PPM deviation). Rank candidates by composite score and return the scored formula network with confidence metrics. The MLR model learns feature weights during training on reference datasets to optimize the balance among these three criteria.

## Related tools

- **SMART** (integrates the MLR model, KnownSet database, and scoring pipeline to extract and rank formula candidates for m/z values) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Ranked candidate formulae fall within the specified PPM tolerance of the input m/z value.
- Top-ranked candidates are validated against reference datasets or orthogonal annotations; precision metric should match or exceed benchmarks reported on reference data.
- Candidates with higher scores show stronger network connectivity (more linked formulae and DBEdges/BioEdges) than lower-ranked candidates.
- No duplicate formulae in the ranked output; each candidate appears once with a unique composite score.
- Score distribution reflects the three criteria appropriately: PPM accuracy, linked formula count, and edge evidence are all represented in the final ranking.

## Limitations

- Ranking depends on the completeness and accuracy of the KnownSet database; formulae not in HMDB, ChEMBL, PubChem, or KEGG will not be ranked.
- The MLR model assumes the three scoring criteria (linked formulae, DBEdges/BioEdges, PPM) are sufficient; novel chemical space or unexpected ionization behavior may produce misleading scores.
- Raw SMART-database exceeds 1 Terabyte; a temporary version with HMDB only is available; users requiring the full database must contact authors.
- Ranking quality degrades for m/z values with few candidate formulae in the network, where statistical power of the MLR model is limited.

## Evidence

- [intro] MLR model criteria: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [intro] KnownSet database construction: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [intro] MLR-based network extraction: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest"
- [readme] Application scope and motivation: "Despite significance, this profound technology generates thousands of features, the accurate annotation of which lags notably behind LC-MS based approaches"
- [readme] Database size limitation: "Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us"
