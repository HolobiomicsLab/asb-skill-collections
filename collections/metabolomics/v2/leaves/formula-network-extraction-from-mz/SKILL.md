---
name: formula-network-extraction-from-mz
description: Use when you have an observed m/z value from spatially-resolved mass
  spectrometry imaging and need to assign one or more plausible molecular formulae
  with confidence metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - SMART
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: restricted
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

# formula-network-extraction-from-mz

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract candidate molecular formulae and their interconnection networks for a given mass-to-charge (m/z) value by querying a precomputed database of 2.8 million formulae linked via chemical and biological edges, then rank them using a multiple linear regression model trained on mass accuracy, database connectivity, and biochemical relationship strength.

## When to use

You have an observed m/z value from spatially-resolved mass spectrometry imaging and need to assign one or more plausible molecular formulae with confidence metrics. This skill is especially useful when LC-MS annotation methods are unavailable or when working with tissue-specific metabolomic features where chemical context (linked compound relationships, biochemical pathways) should inform the ranking.

## When NOT to use

- Your m/z values are already annotated with high-confidence formulae from orthogonal methods (e.g. tandem MS fragmentation or standards); this skill is for de novo or consensus annotation when chemical context is limited.
- You lack calibrated mass accuracy (>10 ppm drift) or your instrument shows systematic m/z bias; the MLR model assumes reliable PPM values and will rank spurious matches if mass calibration is poor.
- Your metabolites are not expected to exist in HMDB, ChEMBL, PubChem, or KEGG (e.g. purely synthetic compounds, very recently discovered metabolites); the formula network relies on these databases.

## Inputs

- m/z value (single numeric or list of m/z values in file format)
- ion polarity (+ / − / 0)
- PPM tolerance threshold (numeric; default 5)
- SMART-Database file (smart.db or equivalent)
- trained multiple linear regression model file (e.g. lr_4f.pkl)

## Outputs

- ranked list of candidate molecular formulae
- formula network graph (linked formulae and edges)
- MLR confidence scores per formula
- source database origin per formula (HMDB/ChEMBL/PubChem)
- PPM deviation and mass accuracy metrics

## How to apply

Load the precomputed SMART-Database (containing 2.8 million formulae with DBEdges from HMDB, ChEMBL, PubChem and BioEdges from KEGG). For each input m/z value, apply a multiple linear regression model to extract all formulae within a user-defined PPM tolerance (default 5 ppm). Score each candidate formula using three criteria: (1) the number and strength of linked formulae connections in the network (DBEdges/BioEdges), (2) biochemical relationship evidence (BioEdges from KEGG reactant pairs), and (3) mass accuracy (PPM deviation). Rank results by regression score and return the formula network with confidence metrics. The PPM threshold and polarity (positive/negative/neutral) are key parameters that must match your instrument calibration and ionization mode.

## Related tools

- **SMART** (primary platform for formula network extraction and multiple linear regression-based formula assignment from m/z values) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Returned formula candidates fall within the specified PPM tolerance of the input m/z value.
- Formulae are chemically plausible (e.g. rational elemental composition, valid valence) and match known metabolite databases (HMDB/ChEMBL/PubChem).
- MLR scores correlate with network density (formulae with many DBEdges/BioEdges receive higher scores when mass accuracy is similar).
- Top-ranked formula can be validated against independent standards, MS/MS fragmentation patterns, or tissue-specific metabolic expectations.
- Formula network includes documented biochemical connections (KEGG BioEdges) that support the annotation in the biological context of the tissue/sample.

## Limitations

- Accuracy of formula assignment is constrained by the completeness and correctness of HMDB, ChEMBL, PubChem, and KEGG databases; novel or very rare metabolites may not be captured.
- MLR model is trained on reference datasets; performance may degrade when m/z values or mass accuracy characteristics differ substantially from the training distribution.
- The full SMART-database exceeds 1 Terabyte; only a temporary HMDB-restricted version is publicly available. Access to the complete database requires contacting the developers.
- PPM tolerance is user-defined; setting it too high increases false positives; too low may miss valid formulae if instrument calibration drifts.
- Formula networks are static and reflect the state of source databases at database construction time; they do not update in real time as new compounds are discovered.

## Evidence

- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked"
- [readme] the accurate annotation of which lags notably behind LC-MS based approaches: "the accurate annotation of which lags notably behind LC-MS based approaches"
- [readme] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us: "Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us"
