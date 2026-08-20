---
name: multiple-linear-regression-model-application
description: Use when when you have an observed m/z value from mass spectrometry imaging and need to annotate it with a ranked list of candidate chemical formulae. Apply this skill when the KnownSet database (2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
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

# multiple-linear-regression-model-application

## Summary

Apply a multiple linear regression model to extract formula networks from a KnownSet database for a given m/z value and score candidate formulae by combining evidence from linked formulae, DBEdges/BioEdges connectivity, and mass accuracy (PPM). This skill is used in spatially-resolved metabolomics to assign chemical formulae to observed mass-to-charge ratios with quantified confidence.

## When to use

When you have an observed m/z value from mass spectrometry imaging and need to annotate it with a ranked list of candidate chemical formulae. Apply this skill when the KnownSet database (2.8 million formulae interconnected via HMDB, ChEMBL, PubChem DBEdges, and KEGG BioEdges) is available and you require multiple scored candidates rather than a single deterministic assignment. Trigger this skill when annotation precision in spatially-resolved metabolomics exceeds what simpler mass-matching approaches can achieve.

## When NOT to use

- When the KnownSet database is not available or not loaded; the MLR model requires precomputed formula networks and cannot generate them de novo.
- When the input m/z value is derived from techniques other than mass spectrometry imaging (e.g., already-annotated LC-MS feature tables); this skill is designed for raw m/z observations in spatially-resolved contexts.
- When only a single deterministic formula assignment is required and no ranked candidate set is needed; simpler deterministic mass lookup may be more appropriate.

## Inputs

- m/z value (float, e.g. 185.9934)
- Polarity flag ('+', '-', or '0' for neutral)
- SMART-Database file (.db)
- Trained MLR model file (.pkl)
- PPM tolerance threshold (integer, default 5)

## Outputs

- Ranked list of candidate formulae with MLR scores
- Linked formulae connections per candidate
- DBEdges and BioEdges strength metrics
- Mass accuracy (PPM) per candidate
- Confidence metrics (derived from regression predictions)

## How to apply

First, load the pre-constructed KnownSet database and the trained multiple linear regression model file (e.g., lr_4f.pkl). For the input m/z value, extract all candidate formulae within a specified PPM tolerance (default: 5 ppm). For each candidate, compute three scoring features: (1) the count and strength of linked formulae connections within the formula network, (2) the number and type of DBEdges (from chemical repositories) and BioEdges (from KEGG biochemical pairs) associated with that formula, and (3) the observed mass accuracy in PPM relative to the input m/z. Feed these three feature vectors into the fitted multiple linear regression model to produce a continuous score for each candidate. Rank candidates by descending score and return the ranked formula network with confidence metrics derived from model predictions.

## Related tools

- **SMART** (Platform that implements the multiple linear regression model for formula assignment; orchestrates KnownSet database queries, feature extraction, and model inference.) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- All returned candidate formulae fall within the specified PPM tolerance of the input m/z value.
- MLR scores are continuous, monotonic-descending in the ranked output list, and fall within the expected range of the fitted model (e.g., [0, 1] or raw regression predictions).
- Each candidate has non-null counts for linked formulae, DBEdges, and/or BioEdges; candidates with zero connections should have lower scores than connected candidates, all else equal.
- Benchmarking on reference datasets (HMDB, ChEMBL, PubChem) reproduces reported precision metrics; the top-ranked prediction should match the ground-truth formula in a high fraction of cases.
- Re-running the same m/z value with the same model and database produces identical rankings and scores (deterministic repeatability).

## Limitations

- The raw SMART-database exceeds 1 Terabyte in size; a temporary version with HMDB data only is provided for download, limiting access to the full cross-repository formula network.
- Annotation precision depends critically on the quality and coverage of the underlying repositories (HMDB, ChEMBL, PubChem, KEGG); formulae not in these databases cannot be discovered or ranked.
- The multiple linear regression model was trained on a specific set of reference datasets; performance may degrade for novel metabolites or m/z ranges not well-represented in training data.
- PPM tolerance and model parameters are fixed after training; the skill does not adapt to user-specific tuning of polarity or mass accuracy requirements without retraining.

## Evidence

- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked"
- [readme] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table: "Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown"
- [readme] Input file/mz_value for formula assignment (Only table format supported). Polarity information for formula assignment. (Default: +, [-,0]). PPM threshold for formula assignment (Default: 5).: "PPM threshold for formula assignment (Default: 5). Polarity information for formula assignment. (Default: +, [-,0])"
