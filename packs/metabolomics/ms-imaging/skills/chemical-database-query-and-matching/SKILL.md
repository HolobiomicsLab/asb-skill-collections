---
name: chemical-database-query-and-matching
description: Use when when you have mass-to-charge (m/z) values from mass spectrometry imaging or other MS experiments and need to assign molecular formulae with high precision, especially in spatially-resolved metabolomics where traditional LC-MS annotation methods are insufficient.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-database-query-and-matching

## Summary

Query a large-scale chemical formula database (2.8M formulae from HMDB, ChEMBL, PubChem, KEGG) and rank candidate formulae for a given m/z value using multiple linear regression and network-based scoring. This skill addresses the precision gap in spatially-resolved metabolomics annotation by leveraging interconnected chemical relationships and mass accuracy constraints.

## When to use

When you have mass-to-charge (m/z) values from mass spectrometry imaging or other MS experiments and need to assign molecular formulae with high precision, especially in spatially-resolved metabolomics where traditional LC-MS annotation methods are insufficient. Use this skill when you have access to a populated chemical formula database and a trained multiple linear regression model, and you need to rank candidates within a PPM tolerance window (typically 5 ppm).

## When NOT to use

- Input is already a fully annotated feature table or metabolite list with confirmed identities—use this skill only for de novo formula assignment from raw m/z values.
- The chemical formulae of interest are not represented in the KnownSet database (HMDB, ChEMBL, PubChem, KEGG), reducing precision and recall for novel or rare compounds.
- PPM measurement error is substantially larger than the default 5 ppm threshold and cannot be reliably adjusted without retraining the model.

## Inputs

- m/z value(s) (single numeric or table format with multiple m/z values)
- Polarity information ('+', '-', or '0' for neutral)
- SMART-Database file (smart.db or equivalent, containing 2.8M formulae and their edges)
- Trained multiple linear regression model file (e.g., lr_4f.pkl)

## Outputs

- Ranked list of candidate molecular formulae per m/z
- Formula annotations with source database (HMDB, ChEMBL, PubChem, KEGG)
- Scoring metrics per candidate (linked formulae count, PPM error, confidence)
- Precision scores when evaluated against reference datasets

## How to apply

Load the KnownSet database (2.8M formulae interconnected by DBEdges and BioEdges) and a trained multiple linear regression model. For each input m/z value, use the MLR model to extract formula networks associated with that m/z. Score all candidate formulae based on three criteria: (1) linked formulae via DBEdges/BioEdges (prior knowledge of biological or chemical plausibility), (2) PPM error between observed and theoretical m/z (filtered by a threshold, typically 5 ppm), and (3) mass accuracy. Output ranked formula predictions with confidence metrics. Evaluate success by comparing predictions against reference datasets and computing precision—the proportion of correct predictions among all predictions made.

## Related tools

- **SMART** (Core platform orchestrating database construction, formula network extraction via multiple linear regression, scoring, and ranking of formula candidates for m/z annotation) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Precision metric on reference benchmark datasets: documented as 'desirable precision' in the paper; compute as (true positives) / (all predictions made).
- PPM error distribution of top-ranked predictions: should cluster tightly around zero within the specified PPM threshold (e.g., ≤5 ppm for 95% of predictions).
- Database source consistency: verify that predicted formulae exist in at least one of HMDB, ChEMBL, PubChem, or KEGG with matching molecular weight and structure.
- Ranking stability: test that replicate runs on the same m/z value and model produce identical ranked lists, confirming reproducibility.
- Edge validation: confirm that high-scoring candidates are connected via documented DBEdges or BioEdges in the KnownSet, not isolated formulae.

## Limitations

- Annotation precision is constrained by the breadth and quality of the underlying chemical databases (HMDB, ChEMBL, PubChem, KEGG); novel or very rare metabolites may not be in the KnownSet.
- The full SMART-database exceeds 1 Terabyte and is not publicly distributed; users must work with temporary subsets (e.g., HMDB-only) available from Figshare or contact the authors for raw data.
- Performance depends critically on the accuracy and PPM calibration of the input mass spectrometer; substantial instrumental drift or miscalibration can degrade precision.
- The trained multiple linear regression model is specific to the feature set and database snapshot used during training; retraining is required if the KnownSet is substantially updated.

## Evidence

- [readme] Database construction and extraction method: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant"
- [readme] Benchmarking and precision evaluation: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision."
- [readme] Command-line interface parameters: "-m PPM, --ppm PPM     PPM threshold for formula assignment (Default: 5)."
- [readme] Problem scope and motivation: "Spatially-resolved metabolomics plays a critical role in unraveling tissue-specific metabolic complexities. Despite significance, this profound technology generates thousands of features, the"
- [readme] Input and output specification: "Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table (DB: H:HMDB,"
