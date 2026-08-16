---
name: ppm-tolerance-scoring-and-ranking
description: Use when you have extracted a list of candidate molecular formulae for a given m/z value and need to rank them by plausibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - SMART
  techniques:
  - LC-MS
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment in mass spectrometry imaging
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

# ppm-tolerance-scoring-and-ranking

## Summary

Score and rank candidate molecular formulae for mass spectrometry peaks by computing mass accuracy (parts per million error) against a reference database, then filtering and sorting by PPM threshold to identify the most likely formula assignments. This skill is essential in spatially-resolved metabolomics where formula annotation precision directly impacts downstream biological interpretation.

## When to use

You have extracted a list of candidate molecular formulae for a given m/z value and need to rank them by plausibility. Use this skill when you have observed m/z values from mass spectrometry imaging and a set of candidate formulae sourced from HMDB, ChEMBL, PubChem, or KEGG—particularly when working in spatially-resolved metabolomics where annotation lags behind LC-MS approaches and you need to suppress false positives via strict mass accuracy filtering.

## When NOT to use

- You already have high-confidence, manually verified formula assignments and do not need computational ranking.
- Your mass spectrometer has poor mass calibration or drift; recalibrate and reprocess raw data before applying this skill.
- You are working with low-resolution MS (e.g. unit mass, >100 ppm baseline error); PPM-based filtering assumes at least 5–10 ppm instrumental accuracy.

## Inputs

- observed m/z value (numeric, e.g. 185.9934)
- candidate formula list with theoretical m/z values
- KnownSet database with 2.8 million formulae, DBEdges, and BioEdges
- polarity setting (+ or −)

## Outputs

- ranked formula candidates table (columns: formula, theoretical_m/z, observed_m/z, PPM_error, database_source, linked_formula_count, DBEdge_count, BioEdge_count, combined_score)
- accepted formulae passing PPM threshold
- rejected candidates (PPM > threshold)

## How to apply

For each candidate formula, calculate the theoretical m/z and compute PPM error as |(observed_mz − theoretical_mz) / theoretical_mz| × 10⁶. Apply a user-configurable PPM threshold (default 5 ppm; adjust based on instrument resolution) to exclude candidates exceeding tolerance. Among remaining candidates, integrate secondary scoring criteria: count and weight linked formulae from the KnownSet database, prioritize candidates with supporting DBEdges (chemical transformations) and BioEdges (metabolic reactant pairs from KEGG), and rank by cumulative score. Return ranked list with PPM values, source database provenance (H/E/P for HMDB/ChEMBL/PubChem), and confidence metrics. The rationale is that mass accuracy combined with biological network evidence (linked metabolites and reactions) substantially reduces ambiguous assignments.

## Related tools

- **SMART** (Implements PPM-based scoring within a multiple linear regression framework; loads KnownSet database, computes formula networks, and ranks candidates by PPM and network linkage criteria.) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Precision metric on reference datasets: verify that formulae predicted within the PPM threshold match ground truth with >80% accuracy (article reports 'desirable precision').
- PPM distribution histogram: check that accepted candidates cluster tightly around 0 ppm error and rejected candidates fall outside the threshold boundary.
- Database provenance consistency: confirm that top-ranked formulae come from reliable sources (HMDB, ChEMBL, PubChem) and have supporting DBEdges/BioEdges.
- Rank stability: rerun with ±1 ppm threshold variation and verify that top-5 formulae remain stable (if not, investigate borderline cases).
- Cross-validation on held-out m/z values: measure precision/recall as a function of PPM threshold and confirm threshold=5 ppm balances specificity against sensitivity.

## Limitations

- PPM tolerance alone cannot resolve isobaric or near-isobaric formulae; DBEdges and BioEdges are heuristic proxies for biological relevance and may not apply in all tissue/metabolic contexts.
- KnownSet database (2.8 million formulae) is derived from HMDB, ChEMBL, PubChem, and KEGG and will not include novel, xenobiotic, or tissue-specific metabolites absent from these repositories.
- Default PPM threshold of 5 is optimized for moderate-resolution MS but may be too strict for older instruments or too lenient for high-resolution Orbitrap/FTMS.
- Multiple linear regression model fit on reference datasets; performance may degrade on tissue types or m/z ranges underrepresented in training.

## Evidence

- [readme] scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values"
- [readme] PPM threshold for formula assignment (Default: 5): "PPM threshold for formula assignment (Default: 5)"
- [intro] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest"
- [intro] accurate annotation of which lags notably behind LC-MS based approaches: "accurate annotation of which lags notably behind LC-MS based approaches"
