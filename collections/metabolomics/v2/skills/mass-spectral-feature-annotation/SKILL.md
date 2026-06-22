---
name: mass-spectral-feature-annotation
description: Use when you have m/z values from spatially-resolved mass spectrometry imaging (e.g., MALDI-MSI, DESI-MSI) and need to assign molecular formulae to thousands of features with higher precision than traditional LC-MS approaches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - SMART
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

# mass-spectral-feature-annotation

## Summary

Assign molecular formulae to mass-to-charge (m/z) features in spatially-resolved mass spectrometry imaging using a machine-learning-guided database search. This skill bridges a critical gap in MSI annotation precision by leveraging a 2.8-million-formula knowledge base interconnected by biochemical evidence to rank formula candidates.

## When to use

You have m/z values from spatially-resolved mass spectrometry imaging (e.g., MALDI-MSI, DESI-MSI) and need to assign molecular formulae to thousands of features with higher precision than traditional LC-MS approaches. Apply this skill when annotation accuracy is critical and you have access to a polarity designation (positive or negative mode) and a target PPM tolerance (typical range 5–10 ppm).

## When NOT to use

- Your input is already a fully annotated feature table (e.g., from a previous LC-MS workflow with high-confidence identifications); re-annotation may introduce noise.
- You lack access to a pre-built SMART database or trained model; the skill requires external data that is large (>1 TB in full form) and must be downloaded separately.
- Your ionization mode or polarity is unknown; the skill requires explicit polarity specification and will rank candidates incorrectly if polarity is misspecified.

## Inputs

- m/z value(s) as floating-point numbers (e.g., 185.9934)
- ionization polarity designation ('+' for positive, '−' for negative, or '0' for both)
- SMART-Database file (smart.db or equivalent)
- trained multiple linear regression model file (e.g., lr_4f.pkl)
- PPM tolerance threshold (numeric; default 5)

## Outputs

- ranked list of candidate molecular formulae with scores
- database source(s) for each formula (H=HMDB, E=ChEMBL, P=PubChem, K=KEGG)
- PPM deviation for each candidate
- structured results file with formula predictions and precision metrics

## How to apply

Load the SMART platform with a KnownSet database comprising 2.8 million formulae cross-linked by DBEdges (from HMDB, ChEMBL, PubChem) and BioEdges (from KEGG). Input your m/z value(s) and specify ionization polarity. SMART applies a multiple linear regression model to extract formula networks associated with each m/z, then scores candidate formulae based on three criteria: (1) linked formulae in the network, (2) presence of DBEdges/BioEdges connecting candidates to known metabolites, and (3) deviation from the observed m/z in parts-per-million (PPM). Select the highest-scoring candidate, verify it falls within your PPM threshold (default 5 ppm), and confirm biochemical plausibility via database source tags. The rationale is that true metabolite formulae are more likely to cluster in well-connected regions of the biochemical reaction network and maintain mass accuracy; spurious candidates typically lack these co-occurrence and edge support.

## Related tools

- **SMART** (open-source platform that integrates the KnownSet database, multiple linear regression model, and scoring logic for formula assignment in mass spectrometry imaging) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0
```

## Evaluation signals

- Predicted formulae match reference annotations on benchmarking datasets with reported precision metrics (as quantified in Cao et al.)
- PPM deviation of top-ranked prediction falls within the specified threshold (e.g., ≤5 ppm)
- Top-ranked candidate appears in at least one of the four database sources (HMDB, ChEMBL, PubChem, KEGG), indicating strong evidence linkage
- For multi-candidate scenarios, candidates with higher DBEdge/BioEdge support rank higher than isolated formulae, confirming network-informed scoring
- Predictions remain stable across repeated runs with identical inputs and parameters

## Limitations

- The full raw SMART database (>1 Terabyte) is not publicly available; users must download a temporary reduced version (HMDB subset) or contact authors for full access.
- Annotation precision is still lower than LC-MS-based approaches in some contexts, indicating that spatially-resolved MSI retains inherent chemical complexity.
- The multiple linear regression model was trained on specific datasets; performance may degrade if input m/z distributions or ionization conditions diverge significantly from training data.
- Formula ranking depends critically on database completeness and edge annotation accuracy; rare or novel metabolites not present in HMDB/ChEMBL/PubChem/KEGG will not be ranked correctly.

## Evidence

- [readme] spatially-resolved metabolomics plays a critical role in unraveling tissue-specific metabolic complexities. Despite significance, this profound technology generates thousands of features, the accurate annotation of which lags notably behind LC-MS based approaches.: "the accurate annotation of which lags notably behind LC-MS based approaches"
- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant pairs.: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [readme] By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values.: "By employing a multiple linear regression model, SMART extracts formula networks associated with the m/z of interest and scores potential candidates based on various criteria, including linked"
- [intro] Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision.: "Benchmarking on reference datasets demonstrates SMART is able to predict the formulae with a desirable precision"
- [readme] Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table (DB: H:HMDB, E:chEMBL, P:PubChem).: "Type m/z values in the left input text(such as 185.9934), and then set up all the parameters in the middle. Click the 'Predict' button and results will be shown in the right table"
