---
name: formula-assignment-in-mass-spectrometry
description: Use when you have m/z values from mass spectrometry imaging (or similar MSI experiments) and need to assign molecular formulae to them. This is especially valuable when working with spatially-resolved metabolomics data where annotation precision lags behind traditional LC-MS approaches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-assignment-in-mass-spectrometry

## Summary

Assign molecular formulae to mass-to-charge (m/z) values in spatially-resolved mass spectrometry imaging using a regression-based network approach. This skill leverages a curated knowledge base of 2.8 million formulae and their biochemical relationships to predict candidate formulae with high precision on reference benchmarks.

## When to use

You have m/z values from mass spectrometry imaging (or similar MSI experiments) and need to assign molecular formulae to them. This is especially valuable when working with spatially-resolved metabolomics data where annotation precision lags behind traditional LC-MS approaches. Apply this skill when you have access to or can build a formula knowledge base and possess reference datasets for benchmarking precision.

## When NOT to use

- Your m/z values come from targeted LC-MS/MS where standard tandem mass spectrometry libraries and fragmentation patterns are available and sufficient — use those direct spectral matching approaches instead.
- You lack access to or cannot construct a comprehensive formula knowledge base (the 2.8 million formulae baseline is foundational to SMART's performance).
- Your mass accuracy is worse than ~5 ppm or your instrument produces highly scattered mass calibration — formula assignment precision will degrade significantly.

## Inputs

- m/z values (single numeric or table file format)
- Polarity information (+, −, or 0 for neutral)
- SMART-Database file (e.g., smart.db with HMDB/ChEMBL/PubChem/KEGG formulae and edges)
- MLR model file (e.g., lr_4f.pkl, pre-trained multiple linear regression model)
- PPM threshold parameter (default: 5)

## Outputs

- Ranked formula predictions per m/z value
- Formula candidates with scoring metadata (linked formulae, DBEdges/BioEdges support, PPM error)
- Precision metrics computed against reference datasets
- Structured results file with assignments and confidence scores

## How to apply

Load or construct a KnownSet database comprising formulae from public repositories (HMDB, ChEMBL, PubChem, KEGG) linked by database edges (DBEdges) and biochemical reactant pair edges (BioEdges). For each m/z value of interest, employ SMART's multiple linear regression model to extract formula networks and compute candidate scores based on linked formulae, edge connections, and mass accuracy (PPM tolerance, default 5 ppm). Rank candidates and evaluate precision against reference datasets by comparing predictions to ground-truth formula annotations. Select the top-ranked formulae as assignments based on the scoring threshold appropriate to your precision requirements.

## Related tools

- **SMART** (Core platform for formula network extraction, multiple linear regression scoring, and candidate ranking in mass spectrometry imaging) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0
```

## Evaluation signals

- Precision metrics on reference benchmarking datasets meet or exceed reported desirable thresholds (as documented in task_003 findings).
- Formula predictions include supporting evidence from linked DBEdges/BioEdges connections, confirming biological plausibility.
- Mass error (PPM) for top-ranked predictions falls within the specified tolerance (≤5 ppm by default).
- No contradictions between polarity setting and assigned formula ionization state.
- Output file contains all expected structured fields (m/z, predicted formula, score, source database, PPM error) for downstream validation.

## Limitations

- SMART requires a pre-built or curated formula knowledge base; raw database exceeds 1 Terabyte and is not fully public (users must contact authors for full access).
- Performance is contingent on the comprehensiveness and quality of DBEdges and BioEdges from source repositories; gaps in public data will limit candidate coverage.
- Formula assignment precision is tightly coupled to mass accuracy; poor instrument calibration will degrade predictions.
- The multiple linear regression model (lr_4f.pkl) was trained on specific reference datasets; generalization to novel sample types or ionization modes not represented in training data is untested.

## Evidence

- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMBD, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked"
- [readme] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] the accurate annotation of which lags notably behind LC-MS based approaches: "the accurate annotation of which lags notably behind LC-MS based approaches"
- [readme] Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table: "Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table"
- [readme] PPM threshold for formula assignment (Default: 5): "PPM threshold for formula assignment (Default: 5)"
